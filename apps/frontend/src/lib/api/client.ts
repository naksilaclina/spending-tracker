import { createClient } from '../supabase/client';

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1').replace(/\/$/, '');

export type ApiListResponse<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

function isApiListResponse<T>(value: unknown): value is ApiListResponse<T> {
  return Boolean(
    value &&
      typeof value === 'object' &&
      'results' in (value as Record<string, unknown>) &&
      Array.isArray((value as Record<string, unknown>).results)
  );
}

export function unwrapList<T>(value: ApiListResponse<T> | T[]): T[] {
  return isApiListResponse<T>(value) ? value.results : value;
}

async function fetchWithAuth<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const supabase = createClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...((options.headers as Record<string, string>) || {}),
  };

  if (session?.access_token) {
    headers.Authorization = `Bearer ${session.access_token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: 'include',
  });

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      await supabase.auth.signOut();
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }

    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || errorData?.message || `API Error: ${response.status} ${response.statusText}`);
  }

  if (response.status === 204) {
    return null as T;
  }

  return response.json() as Promise<T>;
}

export const apiClient = {
  get: <T>(endpoint: string) => fetchWithAuth<T>(endpoint),
  post: <T>(endpoint: string, body: Record<string, unknown> | unknown[]) =>
    fetchWithAuth<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  patch: <T>(endpoint: string, body: Record<string, unknown>) =>
    fetchWithAuth<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(body),
    }),
  delete: <T>(endpoint: string) =>
    fetchWithAuth<T>(endpoint, {
      method: 'DELETE',
    }),
};
