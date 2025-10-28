from pydantic import BaseModel
from typing import Optional, Any, Dict


# Pydantic models for API
class LoginIn(BaseModel):
    studentId: str
    password: str


class UserOut(BaseModel):
    id: Optional[str] = None
    studentId: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None

