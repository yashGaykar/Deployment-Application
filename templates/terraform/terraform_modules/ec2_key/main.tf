resource "tls_private_key" "pk" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Creates key On AWS
resource "aws_key_pair" "kp" {
  key_name   = var.project_name 
  public_key = tls_private_key.pk.public_key_openssh


  #get key.pem on the local machine
  provisioner "local-exec" { 
    command = "echo '${tls_private_key.pk.private_key_pem}' > ./${var.project_name}.pem"
  }
  
  # update permissions
  provisioner "local-exec" {
    command = "chmod 400 ${var.project_name}.pem"
  }

}