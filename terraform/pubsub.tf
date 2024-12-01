resource "google_pubsub_topic" "gcs_put" {
  name = "${local.resource_prefix}-gcs-put"
}

resource "google_pubsub_topic_iam_member" "topic_publisher" {
  topic  = google_pubsub_topic.gcs_put.name
  role   = "roles/pubsub.publisher"
  member = data.google_storage_project_service_account.gcs.member
}
