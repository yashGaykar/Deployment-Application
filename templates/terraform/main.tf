variable "app_port" {
  type        = string
}
variable "instance_ami" {
  type        = string
}
variable "instance_key" {
  type        = string
}
variable "instance_type" {
  type        = string
}
variable "aws_region" {
  type        = string
}
variable "aws_access_key" {
  type        = string
}
variable "aws_secret_access_key" {
  type        = string
}



# Configure the AWS Provider
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_access_key
}

module "instance" {
  source = "../../templates/terraform/modules/ec2_instance"
  # source = "yashGaykar/ec2-instance/aws"
  # version  = "1.0.0"
  instance_ami      = var.instance_ami
  instance_key      = var.instance_key
  instance_type     = var.instance_type
  security_group_id = module.security_group.security_group_id
}

module "security_group" {
  source = "../../templates/terraform/modules/ec2_security_group"
  # source = "yashGaykar/ec2-security-group/aws"
  # version  = "1.0.0"
  app_port = var.app_port
}


output "public_ip" {
  value = module.instance.public_ip
}