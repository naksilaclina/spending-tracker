import type { Metadata } from 'next';
import { Suspense } from 'react';
import './globals.css';
import { Providers } from '@/components/providers';
import { Toaster } from '@/components/ui/sonner';
import { NotificationCenter } from '@/components/notifications/notification-center';

export const metadata: Metadata = {
  title: 'Personal Finance OS',
  description: 'Premium personal finance operating system',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased selection:bg-primary/20 font-sans">
        <Providers>
          <Suspense fallback={null}>
            <NotificationCenter />
          </Suspense>
          {children}
          <Toaster position="top-right" richColors />
        </Providers>
      </body>
    </html>
  );
}
