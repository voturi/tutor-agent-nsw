output "load_balancer_url" {
  description = "URL of the load balancer"
  value       = "http://${aws_lb.main.dns_name}"
}

output "cloudfront_domain_name" {
  description = "CloudFront distribution domain name (HTTPS)"
  value       = "https://${aws_cloudfront_distribution.main.domain_name}"
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = aws_cloudfront_distribution.main.id
}

output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.app.repository_url
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.main.name
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "region" {
  description = "AWS region"
  value       = var.aws_region
}

output "redis_endpoint" {
  description = "Redis primary endpoint"
  value       = aws_elasticache_replication_group.main.primary_endpoint_address
}

output "bastion_public_ip" {
  description = "Public IP address of the bastion host"
  value       = aws_instance.bastion.public_ip
}

output "bastion_ssh_command" {
  description = "SSH command to connect to bastion host"
  value       = "ssh -i ~/.ssh/tutor-agent-bastion.pem ec2-user@${aws_instance.bastion.public_ip}"
}

output "postgres_tunnel_command" {
  description = "SSH tunnel command for PostgreSQL"
  value       = "ssh -i ~/.ssh/tutor-agent-bastion.pem -L 5432:${aws_db_instance.main.address}:5432 ec2-user@${aws_instance.bastion.public_ip}"
}

output "redis_tunnel_command" {
  description = "SSH tunnel command for Redis"
  value       = "ssh -i ~/.ssh/tutor-agent-bastion.pem -L 6379:${aws_elasticache_replication_group.main.primary_endpoint_address}:6379 ec2-user@${aws_instance.bastion.public_ip}"
}

output "postgres_endpoint" {
  description = "PostgreSQL database endpoint"
  value       = aws_db_instance.main.address
}

output "database_url" {
  description = "Complete database URL"
  value       = "postgresql://tutor_user:${var.db_password}@${aws_db_instance.main.address}:5432/tutor_agent_db"
  sensitive   = true
}
