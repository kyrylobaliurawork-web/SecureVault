variable "project_name" {
  type        = string
  default     = "securevault"
  description = "Project name"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environment"
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region"
}

variable "instance_type" {
  type        = string
  default     = "t3.small"
  description = "EC2 instance type"
}

variable "root_volume_size" {
  type        = number
  default     = 20
  description = "EC2 root volume size in GB"

  validation {
    condition     = var.root_volume_size >= 8
    error_message = "Root volume must be at least 8 GB."
  }
}

variable "db_instance_class" {
  type        = string
  default     = "db.t3.micro"
  description = "RDS instance class"
}

variable "db_name" {
  type        = string
  default     = "securevault"
  description = "PostgreSQL database name"
}

variable "db_username" {
  type        = string
  default     = "securevault_admin"
  description = "RDS master username"
}