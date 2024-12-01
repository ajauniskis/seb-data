terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.12.0"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.region
  # credentials = "../gcp-credentials.json"
  default_labels = {
    service     = var.service
    environment = var.env
  }
  add_terraform_attribution_label = true
}
