output "region" {
  value = var.region
}
output "instance_id" {
  value = aws_instance.opsboard.id
}
output "public_ip" {
  value = aws_instance.opsboard.public_ip
}

output "public_dns" {
  value = aws_instance.opsboard.public_dns
}