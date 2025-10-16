# terraform-aws-cloudflare-restrictor [![](https://github.com/rhythmictech/terraform-aws-cloudflare-restrictor/workflows/pre-commit-check/badge.svg)](https://github.com/rhythmictech/terraform-aws-cloudflare-restrictor/actions) <a href="https://twitter.com/intent/follow?screen_name=RhythmicTech"><img src="https://img.shields.io/twitter/follow/RhythmicTech?style=social&logo=RhythmicTech" alt="follow on Twitter"></a>

This module will automatically manage the ingress rules for any security groups that are appropriately tagged, only permitting CloudFlare IP addresses. The module will create a Lambda that runs once per day, using the public CloudFlare API for known IP addresses to pull the latest IPs and merge them into the security group.

By default, the Lambda will update any security group with the tag key `CLOUDFLARE_MANAGED` set to `true`,
though this can be customized. Any existing ingress rules will be removed when this tag key/value match. Since the Lambda only runs once per day, it is recommended that it be manually triggered whenever a new security group is added.

## Example
Here's what using the module will look like:

```
module "cloudflare-restrictor" {
  source = "rhythmictech/terraform-aws-cloudflare-restrictor"
}
```

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.12.19 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | n/a |
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_event_rule.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_iam_policy.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.execution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [archive_file.this](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_iam_policy_document.assume](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allowed_ports"></a> [allowed\_ports](#input\_allowed\_ports) | Ports to allow traffic from CloudFlare on (recommended to only use 443) | `list(number)` | <pre>[<br>  443<br>]</pre> | no |
| <a name="input_execution_expression"></a> [execution\_expression](#input\_execution\_expression) | cron expression for how frequently rules should be updated | `string` | `"rate(1 day)"` | no |
| <a name="input_name"></a> [name](#input\_name) | Moniker to apply to all resources in the module | `string` | `"cloudflare-restrictor"` | no |
| <a name="input_tag_key"></a> [tag\_key](#input\_tag\_key) | Tag key to expect on security groups that will be managed by this module | `string` | `"CLOUDFLARE_MANAGED"` | no |
| <a name="input_tag_value"></a> [tag\_value](#input\_tag\_value) | Tag value to expect on security groups that will be managed by this module | `string` | `"true"` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | User-Defined tags | `map(string)` | `{}` | no |

## Outputs

No outputs.
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
