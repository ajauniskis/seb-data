locals {
  image_name = "dataflow"
  image_path = "${var.region}-docker.pkg.dev/${var.gcp_project}/${google_artifact_registry_repository.dataflow.repository_id}/${local.image_name}"

}

resource "google_artifact_registry_repository" "dataflow" {
  repository_id = "${local.resource_prefix}-dataflow"
  description   = "Docker Repository for Dataflow"
  format        = "DOCKER"
}

resource "null_resource" "build_and_push_docker" {
  triggers = {
    hash = sha1(join("", [for f in fileset("../dataflow", "*") : filesha1("../dataflow/${f}")]))

  }
  provisioner "local-exec" {
    command = <<EOT
      gcloud auth configure-docker ${var.region}-docker.pkg.dev
      docker build -t ${local.image_path}:latest ../dataflow
      docker push ${local.image_path}:latest
    EOT
  }
}
