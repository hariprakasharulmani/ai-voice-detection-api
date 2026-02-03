"""API key authentication middleware."""
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
    """
    Verify API key from Authorization header.
    
    Args:
        credentials: HTTPBearer credentials containing the token
        
    Returns:
        True if API key is valid
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    token = credentials.credentials
    
    if not token:
        logger.warning("Missing API key in request")
        raise HTTPException(
            status_code=401,
            detail="Missing API key"
        )
    
    if token != settings.API_KEY:
        logger.warning(f"Invalid API key attempt: {token[:10]}...")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return True

