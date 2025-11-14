# Ansible Master Node
resource "google_compute_instance" "ansible_master" {
  name         = "ansible-master"
  machine_type = "e2-small"
  zone         = "${var.region}-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
    metadata = {
    enable-oslogin = "TRUE"
  }
  

  metadata_startup_script = file("${path.module}/ansible-i.sh")
  service_account {
    email  = google_service_account.instance_sa.email
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  tags = ["ansible-master"]
}

# # Create GCS bucket ONLY for dynamic inventory
# resource "google_storage_bucket" "ansible_configs" {
#   name          = "${var.project}-ansible-configs-${random_id.bucket_suffix.hex}"
#   location      = var.region
#   force_destroy = true
# }


# resource "random_id" "bucket_suffix" {
#   byte_length = 4
# }

# # Upload ONLY dynamic inventory to GCS
# resource "google_storage_bucket_object" "dynamic_inventory" {
#   name   = "inventory-gcp.py"
#   bucket = google_storage_bucket.ansible_configs.name
#   content = file("${path.module}/ansible/inventory-gcp.py")
# }
 