output "push_role_arn" {
  description = "IAM role ARN for the GitHub Actions push workflow."
  value       = aws_iam_role.gha_push.arn
}

output "ecr_repository_url" {
  description = "ECR repository URL."
  value       = aws_ecr_repository.backend.repository_url
}

output "lambda_function_name" {
  description = "Lambda function name."
  value       = aws_lambda_function.backend.function_name
}

output "function_url" {
  description = "Public Function URL of the app."
  value       = aws_lambda_function_url.backend.function_url
}

output "image_uri" {
  description = "Image URI currently deployed to the Lambda."
  value       = aws_lambda_function.backend.image_uri
}

output "image_tag" {
  description = "Image tag (commit SHA) currently deployed to the Lambda."
  value       = element(split(":", aws_lambda_function.backend.image_uri), length(split(":", aws_lambda_function.backend.image_uri)) - 1)
}
