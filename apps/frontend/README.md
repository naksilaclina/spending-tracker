# Personal Finance OS - Frontend

This is the premium frontend client for the Personal Finance OS, built with Next.js 15 (App Router), TypeScript, Tailwind CSS, shadcn/ui, and Zustand.

## Architecture

The frontend is designed to be completely decoupled from the backend domain data, acting as a presentation layer bridging Supabase (for Auth) with a Django REST API (for Data).

- **Auth Layer:** Uses `@supabase/ssr` directly on the frontend for login, signup, and session management.
- **Data Layer:** The customized `apiClient` (`src/lib/api/client.ts`) automatically retrieves the Supabase JWT token and embeds it as a `Bearer` token in all requests to the Django backend.
- **State Management:** `TanStack Query` for server state (caching/mutations) and `Zustand` (`src/stores/useUIStore.ts`) for transient UI state (sidebar, modals, selected dates).
- **Drag & Drop:** Powered by `@dnd-kit/core` seamlessly integrated into the monthly calendar and daily board views.

## Environment Variables

Create a local `.env.local` file at the root of `apps/frontend`:

```env
# Supabase Project settings
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# Django Backend settings
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## Running the app

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
3. Open [http://localhost:3000](http://localhost:3000)

## Features Included

- Premium responsive UI (Dark/Light mode support).
- Auth Flow (Login, Signup, Protected Routes via Next.js Middleware).
- Drag and Drop calendar planning context.
- Zod-validated data entry forms for Expenses, Incomes, Loans, and Fixed Rules.
- Pure-function Cashflow projections engine for predicting negative balance periods based on expected incomes and planned expenses.

## API Integration Note

To test without the Django backend running, the API requests to `/api/v1/...` will fail gracefully. Wire up `tanstack/react-query` mutations into the UI components using the definitions found in `src/lib/api/endpoints.ts`.
