resource "google_compute_region_instance_group_manager" "php_mig" {
  name               = "php-mig"
  base_instance_name = "php-instance"
  region             = "us-central1"

  version {
    instance_template = google_compute_instance_template.php_template_ubuntu.id
  }

  target_size = 1

  update_policy {
    type                         = "PROACTIVE"
    minimal_action               = "REPLACE"
    max_surge_fixed              = 1
    max_unavailable_fixed        = 0
    replacement_method           = "RECREATE"
  }

  named_port {
    name = "http"
    port = 80
  }
}

resource "google_compute_region_autoscaler" "php_autoscaler" {
  name   = "php-autoscaler"
  region = var.region


  target = google_compute_region_instance_group_manager.php_mig.id

  autoscaling_policy {
    min_replicas = var.min_replicas
    max_replicas = var.max_replicas

    cpu_utilization {
      target = 0.6
    }
    
  }
}

resource "google_compute_health_check" "php_health_check" {
  name               = "php-health-check"
  check_interval_sec = 10
  timeout_sec        = 5
  healthy_threshold  = 2
  unhealthy_threshold = 3

  http_health_check {
    port         = 80
    request_path = "/"
  }
}









