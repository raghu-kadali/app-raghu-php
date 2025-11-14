resource "google_compute_instance_template" "php_template_ubuntu" {
  name_prefix  = "php-ub-template-"
  machine_type = "e2-medium"

  disk {
    boot = true
    auto_delete = true
    source_image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
    disk_size_gb = 10
  }

  # Enable OS Login for SSH access
  metadata = {
    enable-oslogin = "TRUE"
  }

  # Use the same service account as Ansible master
  service_account {
    email = google_service_account.instance_sa.email
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  network_interface {
    network = "default"
    access_config {}
  }

  tags = ["http-server"]

  lifecycle {
    create_before_destroy = true
  }
}