variable "project_name" { type = string }
variable "environment" { type = string }
variable "policy_bucket_arn" { type = string }

# This module is intentionally skeletal.
# Next steps:
# 1. Add IAM role for Bedrock Knowledge Base.
# 2. Add OpenSearch Serverless collection for vector storage.
# 3. Add aws_bedrockagent_knowledge_base.
# 4. Add aws_bedrockagent_data_source for the S3 policy bucket.

resource "aws_iam_role" "bedrock_kb_role" {
  name = "${var.project_name}-${var.environment}-bedrock-kb-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "bedrock.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

output "bedrock_kb_role_arn" { value = aws_iam_role.bedrock_kb_role.arn }
