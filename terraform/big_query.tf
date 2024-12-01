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

resource "google_bigquery_job" "analysis" {
  job_id = "analysis"
  query {
    query = <<EOT
SELECT EXTRACT(YEAR FROM t.tpep_pickup_datetime)as year, EXTRACT(WEEK(MONDAY) FROM t.tpep_pickup_datetime) as week, count(*) as c
FROM `${var.gcp_project}.${google_bigquery_dataset.data.dataset_id}.yellowwtrip` t
WHERE t.DOLocationID = (
  SELECT LocationID FROM `${var.gcp_project}.${google_bigquery_dataset.data.dataset_id}.taxi_zone` WHERE Zone = 'Outside of NYC'
)
GROUP BY 1, 2
LIMIT 1000
EOT
    destination_table {
      project_id = google_bigquery_table.analysis.project
      dataset_id = google_bigquery_table.analysis.dataset_id
      table_id   = google_bigquery_table.analysis.table_id
    }
  }
}
