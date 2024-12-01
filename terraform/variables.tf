variable "service" {
  type        = string
  description = "Name of the service"
}

variable "env" {
  type        = string
  description = "Environment name"
  validation {
    condition     = contains(["prod", "stable", "edge"], var.env)
    error_message = "env must be one of 'prod', 'stable', 'edge'"
  }
}

variable "region" {
  type        = string
  description = "GCP Region for deployment"
}

variable "gcp_project" {
  type        = string
  description = "GCP Project ID"
}
