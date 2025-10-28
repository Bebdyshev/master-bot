from fastapi import APIRouter, HTTPException
from src.schemas.models import LoginIn
from src.services.auth_service import forward_login
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/auth/login")
async def login(payload: LoginIn):
    """Login using external MasterEducation API"""
    try:
        logger.info(f"Attempting login for student ID: {payload.studentId}")
        result = await forward_login(payload)
        logger.info(f"Login successful for student ID: {payload.studentId}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in login: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

