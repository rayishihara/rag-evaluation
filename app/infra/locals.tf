data "aws_caller_identity" "current" {}

data "aws_partition" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  partition  = data.aws_partition.current.partition

  function_arn    = "arn:${local.partition}:lambda:${var.aws_region}:${local.account_id}:function:rag-backend"
  github_owner    = split("/", var.github_repo)[0]
  github_name     = split("/", var.github_repo)[1]
  github_oidc_sub = "repo:${local.github_owner}@${var.github_owner_id}/${local.github_name}@${var.github_repo_id}:ref:refs/heads/${var.github_branch}"

  image_uri = "${aws_ecr_repository.backend.repository_url}:${var.image_tag}"

  github_oidc_provider_arn = var.create_github_oidc_provider ? aws_iam_openid_connect_provider.github[0].arn : data.aws_iam_openid_connect_provider.github[0].arn
}
