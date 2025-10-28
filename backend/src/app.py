import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(title="MasterEducation Auth Proxy")

    frontends = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000")
    origins = [o.strip() for o in frontends.split(",") if o.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(auth_router)

    return app


app = create_app()
