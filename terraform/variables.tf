variable "aws_region" {
  description = "AWS region where resources will be deployed"
  default     = "ap-southeast-2"
}

variable "app_name" {
  description = "Name of the application"
  default     = "tutor-agent"
}

variable "container_port" {
  description = "Port on which the application container will run"
  default     = 8000
}

variable "fargate_cpu" {
  description = "Fargate CPU units"
  default     = 256
}

variable "fargate_memory" {
  description = "Fargate memory"
  default     = 512
}

variable "app_count" {
  description = "Number of application instances"
  default     = 1
}

variable "gemini_api_key" {
  description = "Gemini API Key for accessing APIs"
  type        = string
}

