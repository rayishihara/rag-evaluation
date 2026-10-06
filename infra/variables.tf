variable "aws_region" {
  description = "AWS region for all resources; must match the AWS_REGION GitHub repository variable."
  type        = string
}

variable "snowflake_account" {
  description = "Snowflake account identifier in orgname-accountname form."
  type        = string
}

variable "snowflake_database" {
  description = "Snowflake database holding the Cortex Search service."
  type        = string
}

variable "snowflake_schema" {
  description = "Snowflake schema holding the Cortex Search service."
  type        = string
}

variable "snowflake_warehouse" {
  description = "Snowflake warehouse that runs the Cortex COMPLETE query."
  type        = string
}

variable "cortex_search_service" {
  description = "Cortex Search service name."
  type        = string
  default     = "docs_search_service"
}

variable "cortex_model" {
  description = "Snowflake Cortex model for answer generation, e.g. llama3.1-70b."
  type        = string
}

variable "snowflake_pat" {
  description = "Snowflake programmatic access token; supply only via TF_VAR_snowflake_pat."
  type        = string
  sensitive   = true
}

variable "image_tag" {
  description = "Full 40-character commit SHA of the image to deploy."
  type        = string

  validation {
    condition     = can(regex("^[0-9a-f]{40}$", var.image_tag))
    error_message = "image_tag must be a full 40-character lowercase commit SHA."
  }
}

variable "github_repo" {
  description = "GitHub repository (owner/name) allowed to push images."
  type        = string
  default     = "rayishihara/rag-evaluation"
}

variable "github_owner_id" {
  description = "Numeric GitHub owner ID in the immutable OIDC subject claim; see gh api repos/<owner>/<repo>/actions/oidc/customization/sub."
  type        = number
  default     = 248240394
}

variable "github_repo_id" {
  description = "Numeric GitHub repository ID in the immutable OIDC subject claim; see gh api repos/<owner>/<repo>/actions/oidc/customization/sub."
  type        = number
  default     = 1404895213
}

variable "github_branch" {
  description = "Branch allowed to push images; the workflow's branch trigger must match."
  type        = string
  default     = "main"
}

variable "lambda_architecture" {
  description = "Lambda architecture; the workflow's platforms and runs-on must match (arm64 = linux/arm64 on ubuntu-24.04-arm, x86_64 = linux/amd64 on an x86 runner)."
  type        = string
  default     = "arm64"

  validation {
    condition     = contains(["x86_64", "arm64"], var.lambda_architecture)
    error_message = "lambda_architecture must be x86_64 or arm64."
  }
}

variable "create_github_oidc_provider" {
  description = "Create the GitHub OIDC provider; set false to look up an existing one, since an account allows only one per URL."
  type        = bool
  default     = true
}
