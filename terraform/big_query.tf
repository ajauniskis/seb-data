resource "google_bigquery_dataset" "data" {
  dataset_id    = "data"
  friendly_name = "Data"
  description   = "Data from GCS"
}

resource "google_bigquery_table" "analysis" {
  deletion_protection = false
  dataset_id          = google_bigquery_dataset.data.dataset_id
  table_id            = "analysis"
}
