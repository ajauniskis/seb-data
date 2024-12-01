resource "google_storage_bucket" "data" {
  name     = "${local.resource_prefix}-data"
  location = var.region
  versioning {
    enabled = false
  }
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}

resource "google_storage_notification" "put" {
  bucket         = google_storage_bucket.data.name
  topic          = google_pubsub_topic.gcs_put.id
  payload_format = "JSON_API_V1"

  event_types = ["OBJECT_FINALIZE"] # Trigger on object creation

  # Filter for objects in the "input/" prefix
  object_name_prefix = "input/"
}

resource "google_storage_bucket" "artifacts" {
  name     = "${local.resource_prefix}-artifacts"
  location = var.region
  versioning {
    enabled = false
  }
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}
