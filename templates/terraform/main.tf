variable "app_port" {
  type = string
}
variable "instance_ami" {
  type = string
}
variable "instance_key" {
  type = string
}
variable "instance_type" {
  type = string
}
variable "aws_region" {
  type = string
}
variable "aws_access_key" {
  type = string
}
variable "aws_secret_access_key" {
  type = string
}
variable "project_name" {
  type = string
}


# Configure the AWS Provider
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_access_key
}


# Create a VPC
resource "aws_vpc" "my-vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = var.project_name
  }
}






# Create Internet Gateway
resource "aws_internet_gateway" "my-ig" {
  vpc_id = aws_vpc.my-vpc.id
  tags = {
    Name = var.project_name
  }
}

# Create Route Table
resource "aws_route_table" "my-rt" {
  vpc_id = aws_vpc.my-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my-ig.id
  }

  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.my-ig.id
  }

  tags = {
    Name = var.project_name
  }
}


# Create Subnet
resource "aws_subnet" "my-subnet" {
  vpc_id     = aws_vpc.my-vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = var.project_name
  }
}


#Associate subnet with route table
resource "aws_route_table_association" "my-associate-sub-rt" {
  subnet_id      = aws_subnet.my-subnet.id
  route_table_id = aws_route_table.my-rt.id
}

# Create Security Group
resource "aws_security_group" "my-sg" {
  description = "Works as a firewall"
  vpc_id      = aws_vpc.my-vpc.id
  name        = var.project_name

  ingress {
    description = "TCP PORT"
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.project_name
  }
}




# Create Network Interface
resource "aws_network_interface" "my-ni" {
  subnet_id       = aws_subnet.my-subnet.id
  private_ips     = ["10.0.1.50"]
  security_groups = [aws_security_group.my-sg.id]
}


#Elastic IP
resource "aws_eip" "my-eip" {
  vpc                       = true
  network_interface         = aws_network_interface.my-ni.id
  associate_with_private_ip = "10.0.1.50"
  depends_on                = [aws_internet_gateway.my-ig, aws_instance.my-terraform-instance]
}

output "instance_public_ip" {
  value = aws_eip.my-eip.public_ip
}


# Create Instance
resource "aws_instance" "my-terraform-instance" {

  # config options...
  ami               = var.instance_ami
  instance_type     = var.instance_type
  availability_zone = aws_subnet.my-subnet.availability_zone
  key_name          = var.instance_key

  network_interface {
    device_index         = 0
    network_interface_id = aws_network_interface.my-ni.id
  }


  tags = {
    Name = var.project_name
  }
}





