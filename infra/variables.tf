variable "region" {
  description = "AWS region for OpsBoard infrastructure"
  type        = string
}

variable "ami_id" {
  description = "Ubuntu AMI ID"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "key_name" {
  description = "EC2 key pair name"
  type        = string
}

variable "ssh_cidr" {
  description = "CIDR allowed to SSH into the instance"
  type        = string
}

variable "app_cidr" {
  description = "CIDR allowed to access the app on port 8000"
  type        = string
}

variable "root_volume_size" {
  description = "Root EBS volume size in GiB"
  type        = number
}
