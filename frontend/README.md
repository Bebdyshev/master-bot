# Master Bot Frontend

Next.js frontend for the Student Support Portal.

## Setup

1. Install dependencies:

```bash
npm install
```

2. Configure environment variables:

Create a `.env.local` file (already created) with:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start the development server:

```bash
npm run dev
```

The app will run on [http://localhost:3000](http://localhost:3000).

## Backend Connection

This frontend connects to the FastAPI backend proxy running on port 8000. Make sure the backend is running before using the login feature.

See `../backend/README.md` for backend setup instructions.

## Project Structure

- `app/` — Next.js app router pages and API routes
- `components/` — Reusable UI components (shadcn/ui)
- `lib/` — Context providers and utilities
- `public/` — Static assets
