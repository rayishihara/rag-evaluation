resource "aws_lambda_function" "backend" {
  function_name = "rag-backend"
  role          = aws_iam_role.lambda_exec.arn
  package_type  = "Image"
  image_uri     = local.image_uri
  architectures = [var.lambda_architecture]
  memory_size   = 1024
  timeout       = 120

  environment {
    variables = {
      SNOWFLAKE_ACCOUNT     = var.snowflake_account
      SNOWFLAKE_PAT         = var.snowflake_pat
      SNOWFLAKE_DATABASE    = var.snowflake_database
      SNOWFLAKE_SCHEMA      = var.snowflake_schema
      HF_MODEL              = var.hf_model
      HF_TOKEN              = var.hf_token
      CORTEX_SEARCH_SERVICE = var.cortex_search_service
    }
  }

  depends_on = [aws_ecr_repository_policy.backend]
}

resource "aws_lambda_function_url" "backend" {
  function_name      = aws_lambda_function.backend.function_name
  authorization_type = "NONE"
}
