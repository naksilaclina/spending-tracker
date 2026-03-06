'use client';

import { useUIStore } from '@/stores/useUIStore';
import { Menu, Search, User } from 'lucide-react';
import { Button } from '../ui/button';

export function Header() {
  const { toggleSidebar, toggleInsights } = useUIStore();

  return (
    <header className="sticky top-0 z-30 flex h-16 shrink-0 items-center justify-between border-b bg-background px-4 shadow-sm">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={toggleSidebar}>
          <Menu className="h-5 w-5" />
          <span className="sr-only">Toggle Sidebar</span>
        </Button>
        <span className="font-semibold text-lg tracking-tight shadow-sm">Finance OS</span>
      </div>

      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon">
          <Search className="h-5 w-5" />
          <span className="sr-only">Search</span>
        </Button>
        <Button variant="ghost" size="icon" onClick={toggleInsights} className="md:hidden">
          {/* Mobile insight toggle */}
          <span className="sr-only">Toggle Insights</span>
        </Button>
        <div className="h-8 w-8 rounded-full bg-secondary flex items-center justify-center">
          <User className="h-4 w-4" />
        </div>
      </div>
    </header>
  );
}
