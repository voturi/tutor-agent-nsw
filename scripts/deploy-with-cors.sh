#!/bin/bash

# TutorAgent Backend Deployment Script with CORS Configuration
# This script builds, pushes to ECR, and deploys with updated CORS settings

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="tutor-agent"
AWS_REGION="ap-southeast-2"
DOCKERFILE_PATH="backend/Dockerfile"
BUILD_CONTEXT="backend"

echo -e "${GREEN}🚀 Starting TutorAgent Deployment with CORS Configuration...${NC}"

# Check if we're in the right directory
if [ ! -f "backend/main.py" ] || [ ! -f "terraform/main.tf" ]; then
    echo -e "${RED}❌ Please run this script from the TutorAgent project root directory${NC}"
    exit 1
fi

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

echo -e "${YELLOW}📦 Building Docker image with latest code...${NC}"

# Build the Docker image for AMD64 platform (required for AWS Fargate)
docker build --platform linux/amd64 -t ${APP_NAME}:latest -f ${DOCKERFILE_PATH} ${BUILD_CONTEXT}

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

echo -e "${BLUE}🏗️ Deploying infrastructure with updated CORS configuration...${NC}"

# Change to terraform directory
cd terraform

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo -e "${RED}❌ terraform.tfvars not found. Please create it with your API keys${NC}"
    echo -e "${YELLOW}Example terraform.tfvars:${NC}"
    echo -e "gemini_api_key = \"your-gemini-api-key-here\""
    exit 1
fi

# Initialize Terraform if needed
if [ ! -d ".terraform" ]; then
    echo -e "${YELLOW}🔧 Initializing Terraform...${NC}"
    terraform init
fi

# Plan the deployment
echo -e "${YELLOW}📋 Planning Terraform deployment...${NC}"
terraform plan

# Ask for confirmation
echo -e "${YELLOW}❓ Do you want to apply these changes? (y/N)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${BLUE}🚀 Applying Terraform configuration...${NC}"
    terraform apply -auto-approve
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Infrastructure deployed successfully${NC}"
        
        # Get the load balancer URL
        ALB_URL=$(terraform output -raw load_balancer_url 2>/dev/null || echo "Check AWS Console for ALB URL")
        echo -e "${GREEN}🌐 Backend URL: ${ALB_URL}${NC}"
        
        echo -e "${GREEN}🎉 Deployment complete!${NC}"
        echo -e "${YELLOW}CORS Configuration Applied:${NC}"
        echo -e "  ✅ Vercel frontend URL: https://tutor-agent-nsw-git-main-voturi-gmailcoms-projects.vercel.app"
        echo -e "  ✅ Production domain: https://tutor-agent-nsw.vercel.app"
        echo -e "  ✅ All Vercel preview deployments: https://*.vercel.app"
        
        echo -e "${BLUE}Next Steps:${NC}"
        echo -e "1. Set environment variables in Vercel:"
        echo -e "   NEXT_PUBLIC_API_BASE_URL=${ALB_URL}"
        echo -e "   NEXT_PUBLIC_ENVIRONMENT=production"
        echo -e "2. Redeploy your Vercel frontend"
        echo -e "3. Test the integration"
        
    else
        echo -e "${RED}❌ Terraform apply failed${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⏸️ Deployment cancelled${NC}"
fi

cd ..

echo -e "${GREEN}🏁 Script completed!${NC}"
