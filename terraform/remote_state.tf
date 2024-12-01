terraform {
  backend "gcs" {
    bucket = "seb-data-tf-state"
    prefix = "seb-data"
    # credentials = "../gcp-credentials.json"
  }
}
