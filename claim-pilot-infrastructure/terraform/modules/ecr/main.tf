variable "project_name" { type = string }
variable "repositories" { type = list(string) }

resource "aws_ecr_repository" "this" {
  for_each = toset(var.repositories)
  name     = "${var.project_name}/${each.value}"
  image_scanning_configuration { scan_on_push = true }
}

output "repository_urls" {
  value = { for k, repo in aws_ecr_repository.this : k => repo.repository_url }
}
