# MasterEducation Auth Proxy (FastAPI)

This FastAPI app provides a local endpoint `/api/auth/login` that forwards login requests to the external MasterEducation Students/login API. Use this to avoid CORS issues and centralize error handling.

## Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
pip install -r backend/requirements.txt
```

2. (Optional) Configure environment variables in `backend/.env` or export them:

- `FRONTEND_ORIGINS` — comma-separated origins allowed by CORS (default: `http://localhost:3000`)
- `EXTERNAL_API_BASE` — base URL of the external API (default: `https://api.mastereducation.kz`)

# MasterEducation Auth Proxy (FastAPI)

This FastAPI app provides a proxy endpoint for student authentication via the external MasterEducation Students/login API. This avoids CORS issues and centralizes error handling.

## Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
pip install -r requirements.txt
```

2. (Optional) Configure environment variables:

Copy `.env.example` to `.env` and update if needed:

```bash
cp .env.example .env
```

Key variables:
- `FRONTEND_ORIGINS` — Allowed CORS origins (default: `http://localhost:3000`)
- `EXTERNAL_API_BASE` — External Students/login API URL (default: `https://api.mastereducation.kz`)

3. Run the app locally:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Or from the backend directory:

```bash
uvicorn src.app:app --reload
```

The backend will run on [http://localhost:8000](http://localhost:8000).

## API Endpoints

### Authentication

- `POST /api/auth/login` — Student login via external API
  - Request: `{ "studentId": "string", "password": "string" }`
  - Response: `{ "user": {...}, "token": "..." }` (normalized from external API)

## Frontend Connection

The Next.js frontend at `../frontend` is configured to call this backend. Make sure this server is running when using the login feature.

See `../frontend/README.md` for frontend setup instructions.

## Project Structure

```
backend/
  src/
    app.py              # FastAPI application factory
    routes/
      auth.py           # Authentication endpoint
    services/
      auth_service.py   # Business logic (external API forwarding)
    schemas/
      models.py         # Pydantic models
  main.py               # Entrypoint
  requirements.txt      # Python dependencies
  .env.example          # Environment variables template
```

## Notes

- This is a simple proxy service without a database
- All authentication is handled by the external MasterEducation API
- Tokens and user data are returned from the external API and forwarded to the frontend
- The frontend stores tokens in localStorage



## Frontend Connection

The Next.js frontend at `../frontend` is configured to call this  Make sure this server is running when using the login feature.

See `../frontend/README.md` for frontend setup instructions.

## Project Structure

- `backend/main.py` — Entrypoint (imports app from src package)
- `backend/src/app.py` — FastAPI application factory
- `backend/src/routes/` — API route handlers
- `backend/src/services/` — Business logic (auth forwarding)
- `backend/src/schemas/` — Pydantic models

## Notes
- This proxy forwards the request and attempts to normalize common response shapes (token/user). Adjust parsing depending on the actual successful response your external API returns.
- Keep production credentials and tokens server-side; do not commit secrets.

