resource "google_compute_instance_template" "php_template_ubuntu" {
  name_prefix  = "php-ub-template-"
  machine_type = "e2-medium"

  disk {
    boot = true
    auto_delete = true
    source_image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
    disk_size_gb = 10
  }

  metadata = {
    enable-oslogin = "TRUE"
    startup-script = <<-EOF
      #!/bin/bash
      # Install Docker
      apt update -y
      apt install docker.io -y
      systemctl enable docker
      systemctl start docker
      
      # Authenticate Docker with Artifact Registry
      gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
      
      # Pull and run PHP application container
      docker pull us-central1-docker.pkg.dev/siva-477505/php-app/php-app:v1
      docker run -d --name php-app -p 80:80 --restart unless-stopped us-central1-docker.pkg.dev/siva-477505/php-app/php-app:v1
      
      echo "PHP application deployed successfully"
    EOF
  }

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
