terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.80"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source       = "../../modules/vpc"
  project_name = var.project_name
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr
}

module "ecr" {
  source       = "../../modules/ecr"
  project_name = var.project_name
  repositories = ["backend", "mcp-server", "worker"]
}

module "s3" {
  source       = "../../modules/s3"
  project_name = var.project_name
  environment  = var.environment
}

module "bedrock" {
  source            = "../../modules/bedrock"
  project_name      = var.project_name
  environment       = var.environment
  policy_bucket_arn = module.s3.policy_bucket_arn
}
