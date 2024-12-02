resource "google_storage_bucket_object" "gcs_to_bq_dataflow_flex_template" {
  depends_on = [null_resource.build_and_push_docker]
  name       = "dataflow/gcs-to-bq-tpl.json"
  bucket     = google_storage_bucket.artifacts.name
  content = templatefile("dataflow-tpl.json", {
    image = "${local.image_path}:latest"
  })
}
