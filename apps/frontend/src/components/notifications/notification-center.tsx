'use client';

import { useEffect, useRef } from 'react';
import { usePathname, useRouter, useSearchParams } from 'next/navigation';

import { notify } from '@/lib/notifications';

const TOAST_PARAM_KEYS = ['success', 'error', 'info', 'warning', 'message'] as const;

export function NotificationCenter() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const handledKeyRef = useRef<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(searchParams.toString());
    const key = `${pathname}?${params.toString()}`;

    if (handledKeyRef.current === key) {
      return;
    }

    let didShowToast = false;

    for (const param of TOAST_PARAM_KEYS) {
      const value = params.get(param);
      if (!value) {
        continue;
      }

      if (param === 'message') {
        notify.info({ title: value });
      } else {
        notify[param]({ title: value });
      }
      params.delete(param);
      didShowToast = true;
    }

    handledKeyRef.current = key;

    if (!didShowToast) {
      return;
    }

    const nextUrl = params.toString() ? `${pathname}?${params.toString()}` : pathname;
    router.replace(nextUrl, { scroll: false });
  }, [pathname, router, searchParams]);

  return null;
}
