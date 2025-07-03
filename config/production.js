// Production configuration - safe to commit to git
// No secrets or sensitive data should be in this file

export const productionConfig = {
  // API endpoints
  API_BASE_URL: 'http://tutor-agent-alb-2115439324.ap-southeast-2.elb.amazonaws.com',
  
  // Frontend settings
  ENVIRONMENT: 'production',
  DEBUG: false,
  
  // CORS settings for production
  CORS_ORIGINS: [
    'https://your-frontend-domain.com',
    'https://www.your-frontend-domain.com'
  ],
  
  // Rate limiting for production
  RATE_LIMIT_REQUESTS: 1000,
  RATE_LIMIT_WINDOW: 60,
  
  // File upload limits
  MAX_FILE_SIZE: 10485760, // 10MB
  ALLOWED_EXTENSIONS: ['pdf', 'png', 'jpg', 'jpeg'],
  
  // Session settings
  SESSION_TIMEOUT: 3600,
  MAX_QUESTIONS_PER_SESSION: 20,
  
  // Logging
  LOG_LEVEL: 'INFO',
  LOG_FORMAT: 'json'
};
