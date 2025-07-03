#!/bin/bash

# TutorAgent Backend Deployment Script
# This script builds the Docker image and pushes it to ECR

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="tutor-agent"
AWS_REGION="ap-southeast-2"
DOCKERFILE_PATH="backend/Dockerfile"
BUILD_CONTEXT="backend"

echo -e "${GREEN}🚀 Starting TutorAgent Deployment...${NC}"

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${RED}❌ AWS CLI not configured. Please run 'aws configure'${NC}"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop${NC}"
    exit 1
fi

# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}✅ AWS Account ID: ${AWS_ACCOUNT_ID}${NC}"

# ECR repository URL
ECR_REPO_URL="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${APP_NAME}"

echo -e "${YELLOW}📦 Building Docker image...${NC}"

# Build the Docker image
docker build -t ${APP_NAME}:latest -f ${DOCKERFILE_PATH} ${BUILD_CONTEXT}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
fi

echo -e "${YELLOW}🔐 Logging into ECR...${NC}"

# Login to ECR
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO_URL}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Successfully logged into ECR${NC}"
else
    echo -e "${RED}❌ ECR login failed${NC}"
    exit 1
fi

echo -e "${YELLOW}🏷️ Tagging image for ECR...${NC}"

# Tag the image for ECR
docker tag ${APP_NAME}:latest ${ECR_REPO_URL}:latest

echo -e "${YELLOW}⬆️ Pushing image to ECR...${NC}"

# Push the image to ECR
docker push ${ECR_REPO_URL}:latest

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Image pushed successfully to ECR${NC}"
    echo -e "${GREEN}📍 Image URL: ${ECR_REPO_URL}:latest${NC}"
else
    echo -e "${RED}❌ Image push failed${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Deployment preparation complete!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. Update terraform/terraform.tfvars with your Gemini API key"
echo -e "2. Run 'cd terraform && terraform init'"
echo -e "3. Run 'terraform plan' to review changes"
echo -e "4. Run 'terraform apply' to deploy infrastructure"
