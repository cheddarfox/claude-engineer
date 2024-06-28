# Terraform Variable Values for AI Self-Enhancement System

# AWS Region
aws_region = "us-west-2"

# Environment
environment = "dev"

# VPC Configuration
vpc_cidr = "10.0.0.0/16"

# Subnet Configuration
public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
availability_zones   = ["us-west-2a", "us-west-2b"]

# ECS Configuration
ecs_cluster_name             = "ai-self-enhancement-cluster-dev"
ecs_task_execution_role_name = "AIEnhancementEcsTaskExecutionRole-Dev"
ecs_task_role_name           = "AIEnhancementEcsTaskRole-Dev"

# ECR Configuration
ecr_repository_name = "ai-self-enhancement-repo-dev"

# S3 Configuration
s3_bucket_name = "ai-self-enhancement-data-dev"

# CloudWatch Configuration
cloudwatch_log_group_name = "/ecs/ai-self-enhancement-dev"

# Add more variable values as needed for future resources