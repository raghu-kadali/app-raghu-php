terraform {
  backend "gcs" {
    bucket = "pavan-gcs"
    prefix = "terraform"
  }
}
