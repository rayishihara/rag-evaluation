#!/usr/bin/env bash
# Destroy only the Lambda and its Function URL, keeping ECR and the IAM roles
TF_VAR_snowflake_pat=placeholder exec terraform -chdir=infra destroy \
    -var image_tag=0000000000000000000000000000000000000000 \
    -target='aws_lambda_function.backend'
