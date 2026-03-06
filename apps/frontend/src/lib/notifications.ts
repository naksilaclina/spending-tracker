'use client';

import { toast } from 'sonner';

type NotificationVariant = 'success' | 'error' | 'info' | 'warning' | 'loading';

type NotificationOptions = {
  title: string;
  description?: string;
  id?: string | number;
};

function show(variant: NotificationVariant, { title, description, id }: NotificationOptions) {
  return toast[variant](title, {
    id,
    description,
  });
}

export const notify = {
  success: (options: NotificationOptions) => show('success', options),
  error: (options: NotificationOptions) => show('error', options),
  info: (options: NotificationOptions) => show('info', options),
  warning: (options: NotificationOptions) => show('warning', options),
  loading: (options: NotificationOptions) => show('loading', options),
  dismiss: (id?: string | number) => toast.dismiss(id),
};

export function normalizeErrorMessage(error: unknown, fallback: string) {
  if (error instanceof Error && error.message.trim()) {
    return error.message;
  }

  if (typeof error === 'string' && error.trim()) {
    return error;
  }

  return fallback;
}
