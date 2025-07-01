#!/usr/bin/env python3
"""
Simple test server to verify the FastAPI setup works
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.config import settings

# Create FastAPI application
app = FastAPI(
    title="TutorAgent MVP - Test Server",
    description="AI-powered Year 7 Mathematics Homework Tutoring System",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to TutorAgent MVP - Year 7 Maths Homework Helper",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    """Simple health check without database dependency."""
    return {
        "status": "healthy",
        "service": "TutorAgent MVP Backend",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }

if __name__ == "__main__":
    uvicorn.run(
        "test_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
