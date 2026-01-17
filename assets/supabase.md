# Supabase Integration (Flask backend)

This project uses Supabase as a persistence layer for repair requests.

## Required environment variables

Set these in your `.env` for the **flask_backend** container (see `.env.example`):

- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` — Supabase service role key (server-side only)
- `ADMIN_USERNAME` — admin username used by `/api/admin/login`
- `ADMIN_PASSWORD` — admin password used by `/api/admin/login`
- `FRONTEND_ORIGIN` — allowed origin for CORS (default `http://localhost:3000`)

## Required database table

Create a table in Supabase named:

### `repairs`

Suggested columns (minimum):

- `id` (uuid or bigint, primary key, default)
- `created_at` (timestamp, default now())
- `name` (text, not null)
- `phone` (text, not null)
- `email` (text, nullable)
- `device_type` (text, not null)
- `issue_description` (text, not null)
- `preferred_contact_method` (text, nullable)

> The backend will insert rows with these fields and will query `select("*")` when the admin lists repairs.

## Backend usage

- Submit repair request (public): `POST /api/repairs`
- Admin login: `POST /api/admin/login` (returns bearer token)
- Admin list repairs (protected): `GET /api/repairs` with header `Authorization: Bearer <token>`
