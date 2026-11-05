output "vpc_id" {
  value = aws_vpc.securevault.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "private_subnet_ids" {
  value = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]
}

output "instance_id" {
  value = aws_instance.securevault.id
}

output "public_ip" {
  value = aws_instance.securevault.public_ip
}

output "public_dns" {
  value = aws_instance.securevault.public_dns
}

output "instance_type" {
  value = aws_instance.securevault.instance_type
}

output "ec2_security_group_id" {
  value = aws_security_group.ec2.id
}

output "rds_security_group_id" {
  value = aws_security_group.rds.id
}

output "iam_role_name" {
  value = aws_iam_role.ec2_role.name
}

output "s3_bucket_name" {
  value = aws_s3_bucket.files.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.securevault.address
}

output "rds_port" {
  value = aws_db_instance.securevault.port
}

output "rds_database_name" {
  value = aws_db_instance.securevault.db_name
}

output "rds_username" {
  value = aws_db_instance.securevault.username
}

output "rds_master_secret_arn" {
  value     = aws_db_instance.securevault.master_user_secret[0].secret_arn
  sensitive = true
}

output "app_secret_name" {
  value = aws_secretsmanager_secret.app.name
}

output "ghcr_secret_name" {
  value = aws_secretsmanager_secret.ghcr.name
}