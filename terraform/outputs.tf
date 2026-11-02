output "instance_id" { value = aws_instance.securevault.id }
output "public_ip" { value = aws_instance.securevault.public_ip }
output "public_dns" { value = aws_instance.securevault.public_dns }
output "instance_type" { value = aws_instance.securevault.instance_type }
output "security_group_id" { value = aws_security_group.securevault_sg.id }
output "iam_role_name" { value = aws_iam_role.ec2_role.name }
output "ami_id" { value = data.aws_ami.ubuntu.id }
