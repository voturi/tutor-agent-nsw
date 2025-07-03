"""
TutorAgent MVP Redis Service
"""

import json
from typing import Any, Optional, Union
import redis.asyncio as redis
from redis.asyncio import Redis

from core.config import settings
from core.logging import get_logger

logger = get_logger("redis")


class RedisClient:
    """Redis client wrapper for session management and caching."""
    
    def __init__(self):
        self.redis: Optional[Redis] = None
    
    async def initialize(self):
        """Initialize Redis connection."""
        try:
            self.redis = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
                health_check_interval=30
            )
            
            # Test connection
            await self.redis.ping()
            logger.info("✅ Redis connection established")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Redis: {e}")
            raise
    
    async def close(self):
        """Close Redis connection."""
        if self.redis:
            await self.redis.close()
            logger.info("✅ Redis connection closed")
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key."""
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.error(f"❌ Redis GET error for key {key}: {e}")
            return None
    
    async def set(
        self, 
        key: str, 
        value: str, 
        expire: Optional[int] = None
    ) -> bool:
        """Set key-value pair with optional expiration."""
        try:
            return await self.redis.set(key, value, ex=expire)
        except Exception as e:
            logger.error(f"❌ Redis SET error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key."""
        try:
            result = await self.redis.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"❌ Redis DELETE error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        try:
            return await self.redis.exists(key) > 0
        except Exception as e:
            logger.error(f"❌ Redis EXISTS error for key {key}: {e}")
            return False
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for key."""
        try:
            return await self.redis.expire(key, seconds)
        except Exception as e:
            logger.error(f"❌ Redis EXPIRE error for key {key}: {e}")
            return False
    
    async def get_json(self, key: str) -> Optional[dict]:
        """Get JSON value by key."""
        try:
            value = await self.get(key)
            if value:
                return json.loads(value)
            return None
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"❌ Redis GET_JSON error for key {key}: {e}")
            return None
    
    async def set_json(
        self, 
        key: str, 
        value: dict, 
        expire: Optional[int] = None
    ) -> bool:
        """Set JSON value with optional expiration."""
        try:
            json_value = json.dumps(value)
            return await self.set(key, json_value, expire)
        except Exception as e:
            logger.error(f"❌ Redis SET_JSON error for key {key}: {e}")
            return False
    
    async def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment counter."""
        try:
            return await self.redis.incr(key, amount)
        except Exception as e:
            logger.error(f"❌ Redis INCR error for key {key}: {e}")
            return None
    
    async def hash_get(self, key: str, field: str) -> Optional[str]:
        """Get hash field value."""
        try:
            return await self.redis.hget(key, field)
        except Exception as e:
            logger.error(f"❌ Redis HGET error for key {key}, field {field}: {e}")
            return None
    
    async def hash_set(self, key: str, field: str, value: str) -> bool:
        """Set hash field value."""
        try:
            return await self.redis.hset(key, field, value)
        except Exception as e:
            logger.error(f"❌ Redis HSET error for key {key}, field {field}: {e}")
            return False
    
    async def hash_get_all(self, key: str) -> Optional[dict]:
        """Get all hash fields and values."""
        try:
            return await self.redis.hgetall(key)
        except Exception as e:
            logger.error(f"❌ Redis HGETALL error for key {key}: {e}")
            return None


# Create global Redis client instance
redis_client = RedisClient()


# Helper functions for session management
async def get_session(session_id: str) -> Optional[dict]:
    """Get session data."""
    return await redis_client.get_json(f"session:{session_id}")


async def set_session(session_id: str, session_data: dict) -> bool:
    """Set session data with default expiration."""
    return await redis_client.set_json(
        f"session:{session_id}", 
        session_data, 
        expire=settings.SESSION_TIMEOUT
    )


async def delete_session(session_id: str) -> bool:
    """Delete session."""
    return await redis_client.delete(f"session:{session_id}")


async def extend_session(session_id: str) -> bool:
    """Extend session expiration."""
    return await redis_client.expire(f"session:{session_id}", settings.SESSION_TIMEOUT)
