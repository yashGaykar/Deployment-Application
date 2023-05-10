resource "aws_instance" "my-terraform-instance" {

  ami             = var.instance_ami
  instance_type   = var.instance_type
  key_name        = var.instance_key
  security_groups = [var.security_group_id]

  tags = {
    Name = "my-instance-t"
  }
}