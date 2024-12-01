from unittest import TestCase
from unittest.mock import Mock, patch

from cloudevents.http import CloudEvent
from google.cloud import dataflow_v1beta3
from main import handler, invoke_dataflow

from tests.conftest import mock_cf_settings


class TestIngestToBq(TestCase):
    @patch("main.Settings", return_value=mock_cf_settings)
    @patch("main.invoke_dataflow")
    def test__handler(
        self,
        mock_invoke_dataflow: Mock,
        mock_settings: Mock,
    ):
        cloud_event = CloudEvent(
            {
                "type": "google.cloud.pubsub.topic.v1.messagePublished",
                "source": "//pubsub.googleapis.com/projects/"
                "sample-project/topics/gcs-events",
            },
            {
                "message": {
                    "attributes": {
                        "bucketId": "sample-bucket",
                        "objectId": "input/table/file.csv",
                    }
                }
            },
        )

        handler(cloud_event)

        mock_invoke_dataflow.assert_called_once_with(
            mock_settings.return_value,
            "gs://sample-bucket/input/table/file.csv",
            "test-service:test-dataset.table",
        )

    @patch("main.dataflow_v1beta3.FlexTemplatesServiceClient")
    def test_invoke_dataflow(self, mock_client_class: Mock):
        mock_client = mock_client_class.return_value
        mock_settings = mock_cf_settings

        source_file = "gs://sample-bucket/input/table/file.csv"
        target_table = "test-service:test-dataset.table"

        invoke_dataflow(mock_settings, source_file, target_table)

        expected_request = dataflow_v1beta3.LaunchFlexTemplateRequest(
            project_id="seb-data",
            launch_parameter={
                "job_name": mock_settings.job_name,
                "container_spec_gcs_path": "gs://seb-data-edge-artifacts/"
                "dataflow/gcs-to-bq-tpl.json",
                "parameters": {
                    "input_file": source_file,
                    "output_bq_table": target_table,
                    "project_id": mock_settings.project_id,
                },
                "environment": {
                    "temp_location": mock_settings.dataflow_temp_path,
                    "staging_location": mock_settings.dataflow_stage_path,
                    "service_account_email": mock_settings.dataflow_sa,
                },
            },
        )

        mock_client.launch_flex_template.assert_called_once_with(
            request=expected_request
        )


class TestSettings(TestCase):
    def test__dataflow_temp_path(self):
        settings = mock_cf_settings
        assert settings.dataflow_temp_path == "gs://test-bucket/temp/"

    def test__dataflow_stage_path(self):
        settings = mock_cf_settings
        assert settings.dataflow_stage_path == "gs://test-bucket/stage/"

    def test__job_name(self):
        settings = mock_cf_settings
        assert settings.job_name == "test-service-test-env-test-job"
