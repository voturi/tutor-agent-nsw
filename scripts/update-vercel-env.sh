#!/bin/bash

# Update Vercel Environment Variables for HTTPS Backend
# This script updates the API base URL to use the HTTPS CloudFront distribution

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 Updating Vercel environment variables for HTTPS backend...${NC}"

# CloudFront HTTPS URL
CLOUDFRONT_URL="https://d369ssqqiev2h9.cloudfront.net"

echo -e "${YELLOW}📝 Updating NEXT_PUBLIC_API_BASE_URL to: ${CLOUDFRONT_URL}${NC}"

# Check if Vercel CLI is available
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}⚠️  Vercel CLI not found. Please install it with: npm i -g vercel${NC}"
    echo -e "${YELLOW}📋 Manual instructions:${NC}"
    echo -e "1. Go to https://vercel.com/dashboard"
    echo -e "2. Select your project: tutor-agent-nsw"
    echo -e "3. Go to Settings → Environment Variables"
    echo -e "4. Update NEXT_PUBLIC_API_BASE_URL to: ${CLOUDFRONT_URL}"
    echo -e "5. Redeploy your project"
    exit 1
fi

# Change to frontend directory if we're not there
if [[ $(basename "$PWD") != "frontend" ]]; then
    if [[ -d "frontend" ]]; then
        cd frontend
    else
        echo -e "${YELLOW}⚠️  Please run this script from the project root or frontend directory${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}🔧 Updating environment variable...${NC}"

# Remove existing environment variable and add new one
vercel env rm NEXT_PUBLIC_API_BASE_URL production --yes 2>/dev/null || true
echo "${CLOUDFRONT_URL}" | vercel env add NEXT_PUBLIC_API_BASE_URL production

echo -e "${GREEN}✅ Environment variable updated successfully!${NC}"
echo -e "${YELLOW}🚀 Next steps:${NC}"
echo -e "1. Redeploy your Vercel project to apply changes"
echo -e "2. Test the integration - your frontend should now use HTTPS!"
echo -e "3. The mixed content security issue should be resolved"

echo -e "${GREEN}🎉 Configuration complete!${NC}"
