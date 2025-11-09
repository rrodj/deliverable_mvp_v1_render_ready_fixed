variable "project_name" {
  type    = string
  default = "inventory-guardian"
}

variable "region" {
  type    = string
  default = "us-west-2"
}

variable "desired_count" {
  type    = number
  default = 1
}

variable "cpu_backend" {
  type    = number
  default = 256
}

variable "memory_backend" {
  type    = number
  default = 512
}

variable "cpu_frontend" {
  type    = number
  default = 256
}

variable "memory_frontend" {
  type    = number
  default = 512
}

variable "container_image_backend" {
  type = string
}

variable "container_image_frontend" {
  type = string
}
