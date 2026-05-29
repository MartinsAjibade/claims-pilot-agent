variable "project_name" { type = string }
variable "environment" { type = string }
variable "vpc_cidr" { type = string }

resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = { Name = "${var.project_name}-${var.environment}-vpc" }
}

output "vpc_id" { value = aws_vpc.this.id }
