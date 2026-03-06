'use client';

import { create } from 'zustand';

type ViewMode = 'daily' | 'monthly' | 'yearly' | 'reports' | 'settings';

interface UIStore {
  isSidebarOpen: boolean;
  isInsightsOpen: boolean;
  toggleSidebar: () => void;
  toggleInsights: () => void;
  activeView: ViewMode;
  setActiveView: (view: ViewMode) => void;
  selectedDate: Date;
  setSelectedDate: (date: Date) => void;
}

export const useUIStore = create<UIStore>((set) => ({
  isSidebarOpen: true,
  isInsightsOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  toggleInsights: () => set((state) => ({ isInsightsOpen: !state.isInsightsOpen })),
  activeView: 'monthly',
  setActiveView: (view) => set({ activeView: view }),
  selectedDate: new Date(),
  setSelectedDate: (date) => set({ selectedDate: date }),
}));
