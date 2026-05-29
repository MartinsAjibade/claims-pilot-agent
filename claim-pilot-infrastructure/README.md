# Claim Pilot Infrastructure

Terraform IaC for deploying Claim Pilot services on AWS.

## Architecture

![Claim Pilot platform architecture](docs/arch.png)

Infrastructure in this repository implements the AWS layout above: networking, ECS Fargate services (backend, AI orchestrator, MCP server, workers), load balancing, RDS, Redis/ElastiCache, S3, OpenSearch or vector storage, Bedrock IAM, and observability (CloudWatch, etc.).

## AWS Services

- **VPC** — Custom networking
- **ECR** — Container registries (backend, ai, mcp-server)
- **ECS Fargate** — Container orchestration
- **RDS** — PostgreSQL database
- **Redis** — ElastiCache for caching
- **OpenSearch** — Vector storage for embeddings
- **S3** — Policy document storage
- **Bedrock** — IAM roles for LLM access
- **CloudWatch** — Logging and monitoring

## Usage

```bash
cd terraform/environments/dev
terraform init
terraform plan
terraform apply
```

## Requirements

- Terraform >= 1.6.0
- AWS Provider >= 5.80
- AWS credentials configured

## Maintainer

**Martins Ajibade**

This repository is maintained for the **Claim Pilot** platform (Blue Lambda University).

- **Email:** [martinsajibade3@gmail.com]

For professional inquiries, security-sensitive reports, or questions about this component, please reach out via the address above.
