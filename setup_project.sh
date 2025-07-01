#!/bin/bash

# TutorAgent MVP Development Environment Setup
echo "🚀 Setting up TutorAgent MVP Development Environment..."

# Create main project structure
mkdir -p backend/{agents,api,core,models,services,tests,config}
mkdir -p frontend/{src,public,components,pages,utils}
mkdir -p shared/{schemas,types,constants}
mkdir -p data/{uploads,samples,processed}
mkdir -p docs/{api,architecture,deployment}
mkdir -p scripts/{dev,deploy,data}
mkdir -p tests/{integration,unit,e2e}

# Create agent-specific directories
mkdir -p backend/agents/{document_parser,assessment,tutor}
mkdir -p backend/agents/document_parser/{ocr,parsing,classification}
mkdir -p backend/agents/assessment/{skill_detection,adaptation,analytics}
mkdir -p backend/agents/tutor/{socratic,hints,response_generation}

# Create API route directories
mkdir -p backend/api/{routes,middleware,dependencies}
mkdir -p backend/api/routes/{upload,session,agents,health}

# Create service directories
mkdir -p backend/services/{file_storage,database,redis,llm}

# Create test directories for each component
mkdir -p backend/tests/{agents,api,services,integration}
mkdir -p frontend/tests/{components,pages,utils}

echo "✅ Project structure created successfully!"
echo "📁 Directory structure:"
tree -I 'node_modules|venv|__pycache__|.git' -L 3
