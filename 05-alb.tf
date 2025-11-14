#backend
resource "google_compute_backend_service" "php_backend" {
  name            = "php-backend"
  load_balancing_scheme = "EXTERNAL"
  protocol        = "HTTP"

  # Connect to health check
  health_checks = [google_compute_health_check.php_health_check.id]

  # Connect to MIG
  backend {
    group           = google_compute_region_instance_group_manager.php_mig.instance_group
    balancing_mode  = "UTILIZATION"
  }
}


#url map
resource "google_compute_url_map" "php_url_map" {
  name            = "php-url-map"
  default_service = google_compute_backend_service.php_backend.id
}

#http proxy
resource "google_compute_target_http_proxy" "php_http_proxy" {
  name    = "php-http-proxy"
  url_map = google_compute_url_map.php_url_map.id
}

#global forwarding rule
resource "google_compute_global_forwarding_rule" "php_forwarding_rule" {
  name       = "php-forwarding-rule"
  target     = google_compute_target_http_proxy.php_http_proxy.id
  port_range = "80"
  ip_protocol = "TCP"
}

