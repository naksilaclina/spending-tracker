'use client';

import { useUIStore } from '@/stores/useUIStore';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, startOfWeek, endOfWeek, addMonths, subMonths } from 'date-fns';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { DroppableDayCell } from '@/features/calendar/DroppableDayCell';
import { useDashboardSummary } from '@/lib/api/endpoints';

export function MonthlyView() {
  const { selectedDate, setSelectedDate } = useUIStore();
  const summary = useDashboardSummary('monthly', format(selectedDate, 'yyyy-MM-dd')) as { data?: any };

  const monthStart = startOfMonth(selectedDate);
  const monthEnd = endOfMonth(selectedDate);
  const calendarStart = startOfWeek(monthStart, { weekStartsOn: 1 });
  const calendarEnd = endOfWeek(monthEnd, { weekStartsOn: 1 });
  const daysInGrid = eachDayOfInterval({ start: calendarStart, end: calendarEnd });

  const nextMonth = () => setSelectedDate(addMonths(selectedDate, 1));
  const prevMonth = () => setSelectedDate(subMonths(selectedDate, 1));
  const goToday = () => setSelectedDate(new Date());

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold tracking-tight">{format(selectedDate, 'MMMM yyyy')}</h1>
          <div className="flex items-center rounded-md border p-1 bg-background shadow-sm">
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={prevMonth}><ChevronLeft className="h-4 w-4" /></Button>
            <Button variant="ghost" size="sm" className="h-7 px-3 text-xs" onClick={goToday}>Today</Button>
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={nextMonth}><ChevronRight className="h-4 w-4" /></Button>
          </div>
        </div>
        <div className="rounded-lg border bg-card px-4 py-2 text-sm">
          <div>Income: <span className="font-semibold">{summary.data?.total_income ?? '0.00'}</span></div>
          <div>Expense: <span className="font-semibold">{summary.data?.total_expense ?? '0.00'}</span></div>
          <div>Net: <span className="font-semibold">{summary.data?.net_result ?? '0.00'}</span></div>
        </div>
      </div>

      <div className="grid grid-cols-7 gap-1 flex-1">
        {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day) => (
          <div key={day} className="text-right text-sm font-medium text-muted-foreground p-2">{day}</div>
        ))}
        {daysInGrid.map((date) => (
          <DroppableDayCell key={date.toISOString()} date={date} isMonthlyView>
            <div className="px-1 pb-1 text-[11px] text-muted-foreground">{format(date, 'd')}</div>
          </DroppableDayCell>
        ))}
      </div>
    </div>
  );
}
