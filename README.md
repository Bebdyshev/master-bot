# Master Bot

Student Support Portal with Next.js frontend and FastAPI 

## Quick Start

### 1. Backend (FastAPI)

```bash
# From project root
cd backend
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on: http://localhost:8000

### 2. Frontend (Next.js)

```bash
# From project root (in a new terminal)
cd frontend
npm install
npm run dev
```

Frontend runs on: http://localhost:3000

## Project Structure

```
backend/
  src/
    app.py           # FastAPI application
    routes/          # API endpoints
    services/        # Business logic
    schemas/         # Pydantic models
  main.py            # Entrypoint
  requirements.txt   # Python dependencies

frontend/
  app/               # Next.js pages and API routes
  components/        # React components (shadcn/ui)
  lib/               # Context and utilities
  package.json       # Node dependencies
```

## Features

- 🔐 Student authentication via external API
- 🎨 Modern UI with Tailwind CSS and shadcn/ui
- 🚀 FastAPI backend proxy (avoids CORS)
- 📱 Responsive design

## Environment Variables

### Backend (.env)
- `FRONTEND_ORIGINS` — Allowed CORS origins (default: `http://localhost:3000`)
- `EXTERNAL_API_BASE` — External API base URL (default: `http://localhost:3001`)
### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` — Backend API URL (default: `http://localhost:8000`)

## Development

Both servers support hot-reload:
- Backend: `uvicorn main:app --reload`
- Frontend: `npm run dev`

See individual README files in `backend/` and `frontend/` for more details.

