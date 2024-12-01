import functions_framework
from cloudevents.http import CloudEvent

# from gcs_to_bq import GcsToBigQueryPipeline
from google.cloud import dataflow_v1beta3
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_id: str
    service: str
    env: str
    dataflow_job_name: str
    dataflow_bucket: str
    region: str
    bq_dataset_name: str
    dataflow_sa: str

    @property
    def dataflow_temp_path(self) -> str:
        return f"gs://{self.dataflow_bucket}/temp/"

    @property
    def dataflow_stage_path(self) -> str:
        return f"gs://{self.dataflow_bucket}/stage/"

    @property
    def job_name(self) -> str:
        return f"{self.service}-{self.env}-{self.dataflow_job_name}"


@functions_framework.cloud_event
def handler(cloud_event: CloudEvent):
    settings = Settings()  # pyright: ignore reportCallIssue
    data = cloud_event.data
    attrs = data["message"]["attributes"]

    bucket: str = attrs["bucketId"]
    file: str = attrs["objectId"]
    table_name = file.split("/")[1].replace("-", "_")

    invoke_dataflow(
        settings,
        f"gs://{bucket}/{file}",
        f"{settings.service}:{settings.bq_dataset_name}.{table_name}",
    )

    # invoke_dataflow(
    #     settings,
    #     bucket,
    #     file,
    #     settings.bq_dataset_name,
    #     table_name,
    # )


# def invoke_dataflow(
#     settings: Settings,
#     bucket: str,
#     file: str,
#     bq_dataset_name: str,
#     bq_table_name: str,
# ):
#     pipe = GcsToBigQueryPipeline(
#         input_file=f"gs://{bucket}/{file}",
#         output_bq_table=f"{settings.project_id}:{bq_dataset_name}.{bq_table_name}",
#         project_id=settings.project_id,
#         temp_path=settings.dataflow_temp_path,
#         staging_path=settings.dataflow_stage_path,
#         region=settings.region,
#         job_name=settings.dataflow_job_name,
#     )
#     pipe.run()


def invoke_dataflow(settings: Settings, source_file: str, target_table: str):
    client = dataflow_v1beta3.FlexTemplatesServiceClient()
    request = dataflow_v1beta3.LaunchFlexTemplateRequest(
        project_id="seb-data",
        launch_parameter={
            "job_name": settings.job_name,
            "container_spec_gcs_path": "gs://seb-data-edge-artifacts/dataflow/gcs-to-bq-tpl.json",
            "parameters": {
                "input_file": source_file,
                "output_bq_table": target_table,
                "project_id": settings.project_id,
            },
            "environment": {
                "temp_location": settings.dataflow_temp_path,
                "staging_location": settings.dataflow_stage_path,
                "service_account_email": settings.dataflow_sa,
            },
        },
    )

    client.launch_flex_template(request=request)