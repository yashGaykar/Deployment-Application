resource "aws_instance" "my-terraform-instance" {

  ami                    = var.instance_ami
  instance_type          = var.instance_type
  key_name               = var.instance_key
  vpc_security_group_ids = [var.security_group_id]

  tags = {
    Name = var.project_name
  }
}