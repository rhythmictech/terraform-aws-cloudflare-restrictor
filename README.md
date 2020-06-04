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
| terraform | >= 0.12.19 |

## Providers

| Name | Version |
|------|---------|
| archive | n/a |
| aws | n/a |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| allowed\_ports | Ports to allow traffic from CloudFlare on (recommended to only use 443) | `list(number)` | <pre>[<br>  443<br>]</pre> | no |
| execution\_expression | cron expression for how frequently rules should be updated | `string` | `"rate(1 day)"` | no |
| name | Moniker to apply to all resources in the module | `string` | `"cloudflare-restrictor"` | no |
| tag\_key | Tag key to expect on security groups that will be managed by this module | `string` | `"CLOUDFLARE_MANAGED"` | no |
| tag\_value | Tag value to expect on security groups that will be managed by this module | `string` | `"true"` | no |
| tags | User-Defined tags | `map(string)` | `{}` | no |

## Outputs

No output.

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
