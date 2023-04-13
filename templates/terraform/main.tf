variable "aws_region" {
  type        = string
}

variable "aws_access_key" {
  type        = string
}

variable "aws_secret_access_key" {
  type        = string
}

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





# Configure the AWS Provider
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_access_key
}

# Create Security Group
resource "aws_security_group" "my-sg" {
  description = "Works as a firewall"

  ingress {
    description      = "TCP PORT"
    from_port        = var.app_port
    to_port          = var.app_port
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

    ingress {
    description      = "SSH"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "my-sg-t"
  }
}

output "instance_public_ip" {
    value = aws_instance.my-terraform-instance.public_ip
}


# Create Instance
resource "aws_instance" "my-terraform-instance" {

  # config options...
  ami                =  var.instance_ami
  instance_type      =  var.instance_type
  # availability_zone  =  "us-east-1a"
  key_name           =  var.instance_key

  tags = {
    Name = "my-instance-t"
  }
}





