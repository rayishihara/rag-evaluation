data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name               = "rag-backend-lambda-exec"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:${local.partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_bedrock_inference_profile" "model" {
  inference_profile_id = var.bedrock_model_id
}

# Allow the inference profile and every regional model it routes to
data "aws_iam_policy_document" "lambda_bedrock" {
  statement {
    actions   = ["bedrock:InvokeModel"]
    resources = concat([data.aws_bedrock_inference_profile.model.inference_profile_arn], data.aws_bedrock_inference_profile.model.models[*].model_arn)
  }
}

resource "aws_iam_role_policy" "lambda_bedrock" {
  name   = "bedrock-invoke"
  role   = aws_iam_role.lambda_exec.id
  policy = data.aws_iam_policy_document.lambda_bedrock.json
}
