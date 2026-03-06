'use client';

import { useUIStore } from '@/stores/useUIStore';
import { MonthlyView } from '@/features/calendar/MonthlyView';
import { DailyView } from '@/features/calendar/DailyView';
import { YearlyView } from '@/features/calendar/YearlyView';
import { ReportsView } from '@/features/reports/ReportsView';
import { SettingsView } from '@/features/settings/SettingsView';

export function DashboardScreen() {
  const { activeView } = useUIStore();

  return (
    <div className="h-full">
      {activeView === 'monthly' && <MonthlyView />}
      {activeView === 'daily' && <DailyView />}
      {activeView === 'yearly' && <YearlyView />}
      {activeView === 'reports' && <ReportsView />}
      {activeView === 'settings' && <SettingsView />}
    </div>
  );
}
