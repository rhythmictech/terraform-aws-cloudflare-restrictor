########################################
# General Vars
########################################

variable "allowed_ports" {
  default     = [443]
  description = "Ports to allow traffic from CloudFlare on (recommended to only use 443)"
  type        = list(number)
}

variable "execution_expression" {
  default     = "rate(1 day)"
  description = "cron expression for how frequently rules should be updated"
  type        = string
}

variable "name" {
  default     = "cloudflare-restrictor"
  description = "Moniker to apply to all resources in the module"
  type        = string
}

variable "tag_key" {
  default     = "CLOUDFLARE_MANAGED"
  description = "Tag key to expect on security groups that will be managed by this module"
  type        = string
}

variable "tag_value" {
  default     = "true"
  description = "Tag value to expect on security groups that will be managed by this module"
  type        = string
}

variable "tags" {
  default     = {}
  description = "User-Defined tags"
  type        = map(string)
}
