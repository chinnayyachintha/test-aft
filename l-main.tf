data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = var.source_file
  output_path = var.output_zip
}
 
resource "aws_lambda_function" "this" {
  function_name = var.function_name
  role          = var.role_arn
  handler       = var.handler
  runtime       = var.runtime
  timeout       = var.timeout
 
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}

output "lambda_arn" {
  value = aws_lambda_function.this.arn
}
 
output "lambda_name" {
  value = aws_lambda_function.this.function_name
}

variable "function_name" {
  type = string
}
 
variable "handler" {
  type = string
}
 
variable "runtime" {
  type    = string
  default = "python3.11"
}
 
variable "timeout" {
  type    = number
  default = 600
}
 
variable "role_arn" {
  type = string
}
 
variable "source_file" {
  type = string
}
 
variable "output_zip" {
  type = string
}
