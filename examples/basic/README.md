# basic example
A basic example for this repository

## Code
```

module "this" {
  source = "../.."

  name = "test"
}
```

## Applying
```
>  terraform apply

module.this.aws_iam_role.this: Creating...
module.this.aws_cloudwatch_event_rule.this: Creating...
module.this.aws_iam_policy.this: Creating...
module.this.aws_iam_role.this: Creation complete after 0s [id=test20200604145510752600000002]
module.this.aws_iam_role_policy_attachment.execution: Creating...
module.this.aws_lambda_function.this: Creating...
module.this.aws_cloudwatch_event_rule.this: Creation complete after 0s [id=test-daily]
module.this.aws_iam_policy.this: Creation complete after 0s [id=arn:aws:iam::951703363424:policy/test20200604145510749000000001]
module.this.aws_iam_role_policy_attachment.this: Creating...
module.this.aws_iam_role_policy_attachment.execution: Creation complete after 0s [id=test20200604145510752600000002-20200604145511227700000003]
module.this.aws_iam_role_policy_attachment.this: Creation complete after 0s [id=test20200604145510752600000002-20200604145511332200000004]
module.this.aws_lambda_function.this: Still creating... [10s elapsed]
module.this.aws_lambda_function.this: Creation complete after 14s [id=test-cloudflareupdater]
module.this.aws_lambda_permission.this: Creating...
module.this.aws_cloudwatch_event_target.this: Creating...
module.this.aws_lambda_permission.this: Creation complete after 0s [id=terraform-20200604145524937300000005]
module.this.aws_cloudwatch_event_target.this: Creation complete after 0s [id=test-daily-terraform-20200604145524937300000006]

Apply complete! Resources: 8 added, 0 changed, 0 destroyed.
```
