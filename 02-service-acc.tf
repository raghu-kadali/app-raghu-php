# Service account for VMs
resource "google_service_account" "instance_sa" {
  account_id   = "php-instance"
  display_name = "Instance SA for pulling GAR images"
}

# IAM roles for the service account
resource "google_project_iam_member" "artifact_reader" {
  project = var.project
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.instance_sa.email}"
}

resource "google_project_iam_member" "os_login" {
  project = var.project
  role    = "roles/compute.osLogin"
  member  = "serviceAccount:${google_service_account.instance_sa.email}"
}

resource "google_project_iam_member" "instance_sa_compute_admin" {
  project = var.project
  role    = "roles/compute.instanceAdmin.v1"
  member  = "serviceAccount:${google_service_account.instance_sa.email}"
}

# ADD THESE TWO EXTRA ROLES:
resource "google_project_iam_member" "instance_sa_service_account_user" {
  project = var.project
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.instance_sa.email}"
}

resource "google_project_iam_member" "instance_sa_compute_viewer" {
  project = var.project
  role    = "roles/compute.viewer"
  member  = "serviceAccount:${google_service_account.instance_sa.email}"
}