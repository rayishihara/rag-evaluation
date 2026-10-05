resource "aws_lambda_function" "backend" {
  function_name                  = "rag-backend"
  role                           = aws_iam_role.lambda_exec.arn
  package_type                   = "Image"
  image_uri                      = local.image_uri
  architectures                  = [var.lambda_architecture]
  memory_size                    = 1024
  timeout                        = 120
  reserved_concurrent_executions = 1

  environment {
    variables = {
      SNOWFLAKE_ACCOUNT     = var.snowflake_account
      SNOWFLAKE_PAT         = var.snowflake_pat
      SNOWFLAKE_DATABASE    = var.snowflake_database
      SNOWFLAKE_SCHEMA      = var.snowflake_schema
      BEDROCK_MODEL_ID      = var.bedrock_model_id
      CORTEX_SEARCH_SERVICE = var.cortex_search_service
    }
  }

  depends_on = [aws_ecr_repository_policy.backend]
}

resource "aws_lambda_function_url" "backend" {
  function_name      = aws_lambda_function.backend.function_name
  authorization_type = "NONE"
}

resource "aws_lambda_permission" "url_invoke_function_url" {
  statement_id           = "FunctionURLAllowPublicAccess"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.backend.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}

resource "aws_lambda_permission" "url_invoke_function" {
  statement_id             = "FunctionURLInvokeAllowPublicAccess"
  action                   = "lambda:InvokeFunction"
  function_name            = aws_lambda_function.backend.function_name
  principal                = "*"
  invoked_via_function_url = true
}
