from fastapi import APIRouter, HTTPException, Response
from src.schemas.models import LoginIn
from src.services.auth_service import forward_login
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/auth/login")
async def login(payload: LoginIn, response: Response):
    """Login using external MasterEducation API"""
    try:
        logger.info(f"Attempting login for student ID: {payload.studentId}")
        result = await forward_login(payload)
        logger.info(f"Login successful for student ID: {payload.studentId}")
        
        # Extract token from result
        token = result.get("token")
        if token:
            # Set token in httpOnly cookie (more secure than localStorage)
            response.set_cookie(
                key="token",
                value=token,
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite="lax",
                max_age=7 * 24 * 60 * 60  # 7 days
            )
            # Remove token from response body (it's now in cookie)
            result = {"user": result.get("user")}
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in login: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/auth/logout")
async def logout(response: Response):
    """Logout by clearing the token cookie"""
    response.delete_cookie(key="token")
    return {"detail": "Logged out successfully"}


