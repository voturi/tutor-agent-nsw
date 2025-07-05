# TutorAgent AWS Architecture Design

## Overview
TutorAgent is a full-stack AI-powered tutoring system for Year 7 mathematics homework. The application consists of a FastAPI backend, Next.js React frontend, and uses multiple AI services for tutoring capabilities.

## Application Structure Analysis

### Backend Components (Python FastAPI)
- **Main Application**: FastAPI with CORS and trusted host middleware
- **Database**: PostgreSQL for persistent data storage
- **Cache**: Redis for session management and caching
- **AI Agents**: 
  - Gemini AI integration for tutoring
  - OCR capabilities for document processing
  - Assessment and adaptation logic
- **API Routes**:
  - Health check endpoints
  - File upload handling
  - Session management
  - Chat/tutoring interactions
  - PDF processing workflows
- **Services**:
  - File storage management
  - LLM integrations (OpenAI, Google Gemini)
  - PDF text extraction and OCR

### Frontend Components (Next.js React)
- **Pages**: 
  - Landing page with file upload
  - PDF chat interface
  - Tutoring interface
  - Session management
- **Components**:
  - PDF viewers (simple and advanced)
  - Chat interfaces
  - File upload components
- **Features**:
  - Drag & drop file uploads
  - Real-time chat with AI tutor
  - PDF document display
  - Session persistence
  - Progress tracking

### Key Dependencies
- **Backend**: FastAPI, SQLAlchemy, Redis, OpenAI, Google Gemini, OCR libraries
- **Frontend**: Next.js 15, React 19, TypeScript, TailwindCSS, PDF.js
- **Infrastructure**: PostgreSQL, Redis, File storage

## AWS Architecture Design

### Core Services

#### 1. **Amazon ECS Fargate** - Container Orchestration
- **Backend Service**: FastAPI application
  - Auto-scaling based on CPU/memory usage
  - Health checks and rolling deployments
  - Environment-specific configurations
- **Frontend Service**: Next.js application
  - Static assets served via CloudFront
  - Server-side rendering capabilities

#### 2. **Amazon RDS PostgreSQL** - Primary Database
- Multi-AZ deployment for high availability
- Automated backups and point-in-time recovery
- Performance Insights enabled
- Security groups for controlled access

#### 3. **Amazon ElastiCache (Redis)** - Session & Caching
- Cluster mode for scalability
- In-transit and at-rest encryption
- Automatic failover capabilities
- Session storage and API response caching

#### 4. **Amazon S3** - File Storage
- **Homework Files Bucket**: PDF uploads with lifecycle policies
- **Processed Documents Bucket**: OCR results and extracted text
- **Static Assets Bucket**: Frontend build artifacts
- Versioning enabled with intelligent tiering

#### 5. **Amazon CloudFront** - Content Delivery Network
- Global distribution of static assets
- API Gateway caching
- Custom domain support
- SSL/TLS termination

#### 6. **AWS Application Load Balancer** - Traffic Distribution
- HTTPS termination
- Path-based routing to backend services
- Health checks and failover
- Web Application Firewall integration

#### 7. **Amazon Bedrock** - AI/ML Services
- Integration with Claude/Titan models as backup to Gemini
- Secure API access to foundation models
- Cost optimization through on-demand usage

#### 8. **AWS Lambda** - Serverless Functions
- **File Processing**: OCR and text extraction
- **Background Tasks**: Async document processing
- **API Webhooks**: Integration endpoints
- **Scheduled Tasks**: Cleanup and maintenance

#### 9. **Amazon Textract** - Document Analysis
- OCR capabilities for homework documents
- Form and table extraction
- Mathematical expression recognition

#### 10. **AWS Secrets Manager** - Configuration Management
- API keys for external services (OpenAI, Gemini)
- Database credentials
- Encryption keys and certificates
- Automatic rotation policies

### Network Architecture

#### **VPC Configuration**
- **Public Subnets**: Load balancers and NAT gateways
- **Private Subnets**: ECS services, RDS, ElastiCache
- **Availability Zones**: Multi-AZ deployment across ap-southeast-2

#### **Security Groups**
- **Web Tier**: Allow HTTPS (443) and HTTP (80) from CloudFront
- **Application Tier**: Allow traffic from ALB on port 8000
- **Database Tier**: Allow traffic from application tier on PostgreSQL port
- **Cache Tier**: Allow traffic from application tier on Redis port

### Monitoring and Observability

#### **Amazon CloudWatch**
- Custom metrics for application performance
- Log aggregation from ECS containers
- Alerting for critical thresholds
- Dashboard for operational visibility

#### **AWS X-Ray** - Distributed Tracing
- Request tracing across services
- Performance bottleneck identification
- Error analysis and debugging

#### **AWS CloudTrail** - Audit Logging
- API call logging
- Resource access tracking
- Compliance and security monitoring

### Security Implementation

#### **AWS WAF** - Web Application Firewall
- Protection against common attacks
- Rate limiting and IP filtering
- Custom rules for API protection

#### **AWS IAM** - Identity and Access Management
- Least privilege access policies
- Service-specific roles
- Cross-service permissions

#### **Amazon Certificate Manager** - SSL/TLS
- Automatic certificate provisioning
- Domain validation
- Renewal automation

### CI/CD Pipeline

#### **AWS CodePipeline** - Orchestration
- Source stage: GitHub integration
- Build stage: CodeBuild for containerization
- Deploy stage: ECS service updates

#### **AWS CodeBuild** - Build Automation
- Docker image creation
- Automated testing
- Security scanning

#### **Amazon ECR** - Container Registry
- Docker image storage
- Vulnerability scanning
- Lifecycle policies

### Auto-Scaling Configuration

#### **ECS Service Auto Scaling**
- Target tracking scaling policies
- CPU and memory utilization metrics
- Predictive scaling for known patterns

#### **RDS Auto Scaling**
- Storage auto-scaling
- Read replica scaling
- Performance-based adjustments

#### **ElastiCache Scaling**
- Node group scaling
- Memory optimization
- Regional replication

### Backup and Disaster Recovery

#### **Automated Backups**
- RDS automated backups with 7-day retention
- S3 cross-region replication
- ElastiCache backup scheduling

#### **Disaster Recovery**
- Multi-AZ deployments
- Cross-region data replication
- Recovery time objective (RTO): 1 hour
- Recovery point objective (RPO): 15 minutes

### Cost Optimization

#### **Reserved Instances**
- RDS reserved instances for predictable workloads
- ElastiCache reserved nodes

#### **Spot Instances**
- ECS Spot instances for non-critical workloads
- Cost savings up to 70%

#### **S3 Intelligent Tiering**
- Automatic cost optimization
- Lifecycle policies for old documents

#### **CloudWatch Cost Monitoring**
- Budget alerts and cost tracking
- Resource utilization optimization

### Environment Configuration

#### **Development Environment**
- Smaller instance sizes
- Single AZ deployment
- Reduced backup retention
- Development-specific secrets

#### **Production Environment**
- Multi-AZ high availability
- Enhanced monitoring
- Extended backup retention
- Production security policies

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
1. VPC and networking setup
2. RDS PostgreSQL deployment
3. ElastiCache Redis cluster
4. S3 buckets and IAM roles
5. Secrets Manager configuration

### Phase 2: Application Deployment (Week 3-4)
1. ECR repository creation
2. ECS cluster and service setup
3. ALB and target group configuration
4. CloudFront distribution
5. Initial application deployment

### Phase 3: AI/ML Integration (Week 5-6)
1. Lambda functions for document processing
2. Textract integration
3. Bedrock model configuration
4. API Gateway for external integrations

### Phase 4: Monitoring and Security (Week 7-8)
1. CloudWatch dashboards and alarms
2. X-Ray tracing implementation
3. WAF rules and security policies
4. CloudTrail audit logging

### Phase 5: CI/CD and Optimization (Week 9-10)
1. CodePipeline setup
2. Auto-scaling policies
3. Performance optimization
4. Cost monitoring and alerts

## Application Composer Template Structure

```yaml
# Key components for AWS Application Composer:

Resources:
  # Networking
  - VPC with public/private subnets
  - Internet Gateway and NAT Gateway
  - Route tables and security groups
  
  # Compute
  - ECS Fargate cluster
  - ECS services (backend/frontend)
  - Application Load Balancer
  
  # Storage
  - RDS PostgreSQL instance
  - ElastiCache Redis cluster
  - S3 buckets (uploads, processed, static)
  
  # CDN and Security
  - CloudFront distribution
  - AWS WAF web ACL
  - Certificate Manager certificates
  
  # AI/ML
  - Lambda functions
  - Textract service integration
  - Bedrock model access
  
  # Monitoring
  - CloudWatch log groups
  - X-Ray tracing
  - CloudWatch alarms
  
  # Security
  - IAM roles and policies
  - Secrets Manager secrets
  - Security groups and NACLs
```

This architecture provides a scalable, secure, and cost-effective solution for the TutorAgent application, leveraging AWS best practices and the user's preferred ap-southeast-2 region.

## Next Steps

1. Open AWS Application Composer
2. Create a new template
3. Add the components following the phase implementation plan
4. Configure connections and dependencies
5. Export CloudFormation template
6. Deploy using AWS CDK or CloudFormation

The architecture is designed to handle the specific needs of an AI tutoring application with file uploads, real-time chat, and document processing capabilities while maintaining high availability and security standards.
