import os
import httpx
from fastapi import HTTPException
from src.schemas.models import LoginIn

EXTERNAL_BASE = os.getenv("EXTERNAL_API_BASE", "https://api.mastereducation.kz")


async def forward_login(payload: LoginIn):
    url = f"{EXTERNAL_BASE}/api/Students/login"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                url,
                json=payload.dict(),
                headers={"Accept": "application/json, text/plain, */*", "Content-Type": "application/json"},
                timeout=10.0,
            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Failed to reach external auth service")

    content_type = resp.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            data = resp.json()
        except ValueError:
            raise HTTPException(status_code=502, detail="Malformed JSON from external auth service")

        if resp.status_code >= 400:
            raise HTTPException(status_code=resp.status_code, detail=data)

        token = data.get("token") or data.get("accessToken")
        user = data.get("user") or data.get("student") or data

        response = {"user": user}
        if token:
            response["token"] = token
        return response

    text = resp.text.strip()
    if resp.status_code >= 400:
        raise HTTPException(status_code=400, detail=text)

    return {"message": text}
