# Deployment Guide

## Environment Configuration

### For Development
Use `.env` file (never commit with real secrets)

### For Production
**NEVER commit `.env.production` to git!**

Instead, use one of these approaches:

#### Option 1: AWS Systems Manager Parameter Store / Secrets Manager
Store sensitive values in AWS and retrieve them at runtime:

```bash
# Example: Store API keys in AWS Secrets Manager
aws secretsmanager create-secret --name "tutor-agent/openai-key" --secret-string "your-api-key"
```

#### Option 2: Environment Variables in Deployment
Set environment variables directly in your deployment platform:

```bash
# For AWS Lambda
aws lambda update-function-configuration \
  --function-name tutor-agent \
  --environment Variables='{OPENAI_API_KEY=your-key,ENVIRONMENT=production}'

# For ECS/Fargate
# Use task definition with environment variables

# For EC2
# Set in /etc/environment or use systemd environment files
```

#### Option 3: Copy Template and Configure Manually
```bash
# On your production server
cp .env.production.example .env.production
# Edit .env.production with actual values
nano .env.production
```

## Security Best Practices

1. **Use AWS Secrets Manager** for API keys and database passwords
2. **Use IAM roles** instead of access keys when possible
3. **Enable encryption** for all data at rest and in transit
4. **Use VPC** to isolate your resources
5. **Enable CloudTrail** for audit logging
6. **Rotate secrets regularly**

## Deployment Steps

1. Deploy infrastructure with Terraform
2. Configure secrets in AWS Secrets Manager
3. Deploy application code
4. Update DNS and SSL certificates
5. Test all endpoints
6. Monitor logs and metrics

## Frontend Configuration

For the frontend to connect to AWS endpoints, update your frontend build configuration:

```javascript
// In your frontend build process
const config = {
  development: {
    API_URL: 'http://localhost:8000'
  },
  production: {
    API_URL: 'https://your-api-gateway-url.amazonaws.com/prod'
  }
}

export default config[process.env.NODE_ENV || 'development']
```

## Environment Variables Reference

See `.env.production.example` for a complete list of required environment variables for production deployment.
