data "aws_caller_identity" "current" {}

data "aws_partition" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  partition  = data.aws_partition.current.partition

  function_arn      = "arn:${local.partition}:lambda:${var.aws_region}:${local.account_id}:function:rag-backend"
  bedrock_model_arn = "arn:${local.partition}:bedrock:${var.aws_region}::foundation-model/${var.bedrock_model_id}"
  github_oidc_sub   = "repo:${var.github_repo}:ref:refs/heads/${var.github_branch}"

  image_uri = "${aws_ecr_repository.backend.repository_url}:${var.image_tag}"
}
