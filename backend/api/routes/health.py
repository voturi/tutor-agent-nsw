"""
TutorAgent MVP Health Check API Routes
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
import asyncio
from datetime import datetime

from services.database import database
from services.redis import redis_client
from core.config import settings
from core.logging import get_logger

logger = get_logger("health")

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    version: str
    environment: str
    services: Dict[str, Any]


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Basic health check endpoint.
    Returns overall application health status.
    """
    timestamp = datetime.utcnow()
    services = {}
    overall_status = "healthy"
    
    # Check database connection
    try:
        await database.fetch_one("SELECT 1 as test")
        services["database"] = {
            "status": "healthy",
            "url": settings.DATABASE_URL.split("@")[1] if "@" in settings.DATABASE_URL else "localhost"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        services["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        overall_status = "unhealthy"
    
    # Check Redis connection
    try:
        await redis_client.redis.ping()
        services["redis"] = {
            "status": "healthy",
            "url": settings.REDIS_URL.split("@")[1] if "@" in settings.REDIS_URL else "localhost"
        }
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        services["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        overall_status = "unhealthy"
    
    # Check LLM API availability (basic check)
    services["llm"] = {
        "status": "configured" if settings.OPENAI_API_KEY else "not_configured",
        "provider": "openai" if settings.OPENAI_API_KEY else "none"
    }
    
    return HealthResponse(
        status=overall_status,
        timestamp=timestamp,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        services=services
    )


@router.get("/ready")
async def readiness_check():
    """
    Kubernetes-style readiness check.
    Returns 200 if the application is ready to serve traffic.
    """
    try:
        # Quick database check
        await database.fetch_one("SELECT 1 as test")
        
        # Quick Redis check
        await redis_client.redis.ping()
        
        return {"status": "ready", "timestamp": datetime.utcnow()}
    
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")


@router.get("/live")
async def liveness_check():
    """
    Kubernetes-style liveness check.
    Returns 200 if the application is alive.
    """
    return {
        "status": "alive", 
        "timestamp": datetime.utcnow(),
        "version": settings.APP_VERSION
    }
