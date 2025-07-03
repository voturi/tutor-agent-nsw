# Vercel Environment Setup

## Required Environment Variables for Vercel

Add these environment variables in your Vercel project settings:

### Production Environment Variables

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add the following:

```bash
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://tutor-agent-alb-2115439324.ap-southeast-2.elb.amazonaws.com
NEXT_PUBLIC_ENVIRONMENT=production

# Optional: Analytics and monitoring
NEXT_PUBLIC_ANALYTICS_ENABLED=true
```

### Command Line Setup (Alternative)

You can also set these via Vercel CLI:

```bash
# Install Vercel CLI if not installed
npm i -g vercel

# Login to Vercel
vercel login

# Set environment variables
vercel env add NEXT_PUBLIC_API_BASE_URL production
# Enter: http://tutor-agent-alb-2115439324.ap-southeast-2.elb.amazonaws.com

vercel env add NEXT_PUBLIC_ENVIRONMENT production
# Enter: production

# Redeploy to apply changes
vercel --prod
```

## Important Notes

⚠️ **HTTPS/HTTP Issue**: Your backend is currently on HTTP while Vercel serves HTTPS. Modern browsers may block mixed content (HTTPS frontend calling HTTP backend).

### Solutions:
1. **Recommended**: Set up HTTPS for your AWS backend using:
   - AWS Application Load Balancer with SSL certificate
   - CloudFront distribution
   - API Gateway with custom domain

2. **Temporary**: Test locally first, then implement HTTPS

### Next Steps After Environment Setup:
1. Set the environment variables in Vercel
2. Redeploy your frontend
3. Test the integration
4. If CORS errors persist, ensure backend is redeployed with updated CORS settings
