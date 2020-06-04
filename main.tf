data "archive_file" "this" {
  type        = "zip"
  source_file = "${path.module}/cloudflareupdater.py"
  output_path = "${path.module}/tmp/cloudflareupdater.zip"
}

data "aws_iam_policy_document" "assume" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "this" {
  name_prefix        = "${var.name}-"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

resource "aws_iam_role_policy_attachment" "execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.this.name
}

data "aws_iam_policy_document" "this" {
  statement {
    actions = [
      "ec2:AuthorizeSecurityGroupIngress",
      "ec2:RevokeSecurityGroupIngress"
    ]

    resources = ["*"]

    condition {
      test     = "StringEquals"
      variable = "ec2:ResourceTag/${var.tag_key}"
      values   = [var.tag_value]
    }
  }

  statement {
    actions   = ["ec2:DescribeSecurityGroups"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "this" {
  name_prefix = "${var.name}-"
  policy      = data.aws_iam_policy_document.this.json
}

resource "aws_iam_role_policy_attachment" "this" {
  policy_arn = aws_iam_policy.this.arn
  role       = aws_iam_role.this.name
}

resource "aws_lambda_function" "this" {
  filename         = data.archive_file.this.output_path
  function_name    = "${var.name}-cloudflareupdater"
  handler          = "cloudflareupdater.lambda_handler"
  role             = aws_iam_role.this.arn
  runtime          = "python3.7"
  source_code_hash = data.archive_file.this.output_base64sha256
  tags             = var.tags
  timeout          = 180

  environment {
    variables = {
      PORTS_LIST = join(",", var.allowed_ports)
      TAG_KEY    = var.tag_key
      TAG_VALUE  = var.tag_value
    }
  }

  lifecycle {
    ignore_changes = [
      filename,
      last_modified,
    ]
  }
}

resource "aws_cloudwatch_event_rule" "this" {
  name_prefix         = "${var.name}-scheduled-rule"
  schedule_expression = var.execution_expression

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_cloudwatch_event_target" "this" {
  arn  = aws_lambda_function.this.arn
  rule = aws_cloudwatch_event_rule.this.name

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_permission" "this" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.this.arn

  lifecycle {
    create_before_destroy = true
  }
}
