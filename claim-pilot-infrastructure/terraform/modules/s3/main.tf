variable "project_name" { type = string }
variable "environment" { type = string }

resource "aws_s3_bucket" "policy_docs" {
  bucket = "${var.project_name}-${var.environment}-policy-docs"
}

resource "aws_s3_bucket" "claim_docs" {
  bucket = "${var.project_name}-${var.environment}-claim-docs"
}

output "policy_bucket_name" { value = aws_s3_bucket.policy_docs.bucket }
output "policy_bucket_arn" { value = aws_s3_bucket.policy_docs.arn }
