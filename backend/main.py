"""
TutorAgent MVP - Main FastAPI Application
Year 7 Mathematics Homework Tutoring System
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.config import settings
from core.logging import setup_logging
from api.routes import health, upload, session, agents, chat, pdf_chat
from services.database import database
from services.redis import redis_client

# Setup logging
logger = setup_logging()

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Year 7 Mathematics Homework Tutoring System",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
)


@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    logger.info("🚀 Starting TutorAgent MVP...")
    
    try:
        # Initialize database connection (optional)
        try:
            await database.connect()
            logger.info("✅ Database connected")
        except Exception as e:
            logger.warning(f"⚠️  Database not available: {e}")
            logger.info("💡 Chat functionality will work without database")
        
        # Initialize Redis connection (optional)
        try:
            await redis_client.initialize()
            logger.info("✅ Redis connected")
        except Exception as e:
            logger.warning(f"⚠️  Redis not available: {e}")
            logger.info("💡 Sessions will use memory storage")
        
        # Initialize agents (placeholder for now)
        logger.info("✅ Agents initialized")
        
        logger.info("🎉 TutorAgent MVP started successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("🛑 Shutting down TutorAgent MVP...")
    
    try:
        await database.disconnect()
        await redis_client.close()
        logger.info("✅ Cleanup completed")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")


@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )


# Include API routes
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(session.router, prefix="/api/v1/session", tags=["Session"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(pdf_chat.router, prefix="/api/v1/pdf-chat", tags=["PDF Chat"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to TutorAgent MVP - Year 7 Maths Homework Helper",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs" if settings.ENVIRONMENT == "development" else "disabled"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.RELOAD,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )
