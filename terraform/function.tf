locals {
  cf_build_file  = "../build/cf.zip"
  cf_source_path = "../cloud_function"
}

data "archive_file" "cf" {
  type        = "zip"
  output_path = local.cf_build_file
  source_dir  = local.cf_source_path
}

resource "google_storage_bucket_object" "cf_artifact" {
  name       = "cf.zip"
  bucket     = google_storage_bucket.artifacts.name
  source     = local.cf_build_file
  depends_on = [data.archive_file.cf]
}

resource "google_cloudfunctions2_function" "bq_ingest" {
  name        = "${local.resource_prefix}-bq-ingest"
  location    = var.region
  description = "Orchestrates GCS file ingestion to BQ"

  build_config {
    runtime     = "python311"
    entry_point = "handler"
    environment_variables = {
      BUILD_CONFIG_TEST = "build_test"
    }
    source {
      storage_source {
        bucket = google_storage_bucket.artifacts.name
        object = google_storage_bucket_object.cf_artifact.name
      }
    }
  }

  service_config {
    max_instance_count               = 3
    min_instance_count               = 1
    available_memory                 = "1Gi"
    timeout_seconds                  = 60
    max_instance_request_concurrency = 80
    available_cpu                    = "1"
    environment_variables = {
      PROJECT_ID        = var.gcp_project
      SERVICE           = var.service
      ENV               = var.env
      DATAFLOW_JOB_NAME = "gcs-to-bq"
      DATAFLOW_BUCKET   = "${google_storage_bucket.artifacts.name}/dataflow"
      REGION            = var.region
      BQ_DATASET_NAME   = google_bigquery_dataset.data.dataset_id
      DATAFLOW_SA       = google_service_account.dataflow_sa.email
    }
    ingress_settings               = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision = true
    service_account_email          = google_service_account.cloud_function_sa.email
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.gcs_put.id
    retry_policy   = var.env == "edge" ? "RETRY_POLICY_DO_NOT_RETRY" : "RETRY_POLICY_RETRY"
  }

  lifecycle {
    replace_triggered_by = [google_storage_bucket_object.cf_artifact]
  }
}
