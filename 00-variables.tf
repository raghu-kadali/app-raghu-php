
variable "project" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Default zone for zonal resources"
  type        = string
  default     = "us-central1-a"
}

variable "image_uri" {
  description = "Full Artifact Registry Docker image URI"
  type        = string
}

variable "gcs_ansible_bucket" {
  description = "GCS bucket where Ansible playbooks are stored"
  type        = string
}

# variable "gcs_ansible_log_bucket" {
#   description = "GCS bucket where startup-script uploads logs"
#   type        = string
# }

variable "instance_count" {
  description = "Initial VM count in the MIG"
  type        = number
  default     = 1
}

variable "min_replicas" {
  description = "Minimum VM count for autoscaler"
  type        = number
  default     = 1
}

variable "max_replicas" {
  description = "Maximum VM count for autoscaler"
  type        = number
  default     = 3
}

variable "machine_type" {
  description = "Compute Engine machine type"
  type        = string
  default     = "e2-medium"
}
