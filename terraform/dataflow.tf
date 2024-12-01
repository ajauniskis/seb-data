resource "google_storage_bucket_object" "gcs_to_bq_dataflow_flex_template" {
  depends_on = [null_resource.build_and_push_docker]
  name       = "dataflow/gcs-to-bq-tpl.json"
  bucket     = google_storage_bucket.artifacts.name
  content = templatefile("dataflow-tpl.json", {
    image = "${local.image_path}:latest"
  })
}

# resource "google_dataflow_flex_template_job" "gcs_to_bq" {
#   provider                     = google-beta
#   project                      = var.gcp_project
#   name                         = "${local.resource_prefix}-gcs-t-bq"
#   region                       = var.region
#   container_spec_gcs_path      = "gs://${google_storage_bucket.artifacts.name}/${google_storage_bucket_object.gcs_to_bq_dataflow_flex_template.name}"
#   skip_wait_on_job_termination = true
#   temp_location                = "gs://${google_storage_bucket.artifacts.name}/temp/"
#   staging_location             = "gs://${google_storage_bucket.artifacts.name}/stage/"
#   #   sdk_container_image          = "${local.image_path}:latest"
#   parameters = {
#     input_file = "messages"
#   }
# }
