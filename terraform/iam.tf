# Create a service account
resource "google_service_account" "cloud_function_sa" {
  account_id   = "${local.resource_prefix}-cf-sa"
  display_name = "Cloud Function Service Account"
}

# Bind the service account to the roles for GCS and Dataflow
resource "google_project_iam_binding" "cf_gcs_access" {
  project = var.gcp_project
  role    = "roles/storage.objectViewer"
  members = [
    "serviceAccount:${google_service_account.cloud_function_sa.email}"
  ]
}

resource "google_project_iam_binding" "cf_dataflow_invoker" {
  project = var.gcp_project
  role    = "roles/dataflow.admin"
  members = [
    "serviceAccount:${google_service_account.cloud_function_sa.email}"
  ]
}

resource "google_project_iam_binding" "cf_sa_user" {
  project = var.gcp_project
  role    = "roles/iam.serviceAccountUser"
  members = [
    "serviceAccount:${google_service_account.cloud_function_sa.email}"
  ]
}


resource "google_service_account" "dataflow_sa" {
  account_id   = "${local.resource_prefix}-dataflow-sa"
  display_name = "Dataflow Service Account"
}

resource "google_project_iam_binding" "df_gcs_access" {
  project = var.gcp_project
  role    = "roles/storage.objectAdmin"
  members = [
    "serviceAccount:${google_service_account.dataflow_sa.email}"
  ]
}

resource "google_project_iam_binding" "df_viewer" {
  project = var.gcp_project
  role    = "roles/viewer"
  members = [
    "serviceAccount:${google_service_account.dataflow_sa.email}"
  ]
}

resource "google_project_iam_binding" "df_worker" {
  project = var.gcp_project
  role    = "roles/dataflow.worker"
  members = [
    "serviceAccount:${google_service_account.dataflow_sa.email}"
  ]
}

resource "google_project_iam_binding" "df_sa_user" {
  project = var.gcp_project
  role    = "roles/iam.serviceAccountUser"
  members = [
    "serviceAccount:${google_service_account.dataflow_sa.email}"
  ]
}
