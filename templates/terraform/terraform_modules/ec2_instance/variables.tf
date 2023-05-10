variable "instance_ami" {
  type        = string
  default     = "ami-0557a15b87f6559cf"
}
variable "instance_key" {
  type        = string
}
variable "instance_type" {
  type        = string
  default     = "t2.micro"
}
variable "security_group_id" {
  type        = string
}
