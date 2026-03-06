'use client';

import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { InsightsPanel } from '@/components/layout/InsightsPanel';
import { BoardDndContext } from '@/features/board/BoardDndContext';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen flex-col overflow-hidden bg-background">
      <Header />
      <BoardDndContext>
        <div className="flex flex-1 overflow-hidden">
          <Sidebar />
          <main className="flex-1 overflow-auto bg-zinc-50 p-4 dark:bg-zinc-950">
            {children}
          </main>
          <InsightsPanel />
        </div>
      </BoardDndContext>
    </div>
  );
}
