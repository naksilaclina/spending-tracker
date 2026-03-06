'use client';

import { useUIStore } from '@/stores/useUIStore';
import { format, addDays, subDays } from 'date-fns';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { DroppableDayCell } from '@/features/calendar/DroppableDayCell';

export function DailyView() {
  const { selectedDate, setSelectedDate } = useUIStore();

  const nextDay = () => setSelectedDate(addDays(selectedDate, 1));
  const prevDay = () => setSelectedDate(subDays(selectedDate, 1));
  const goToday = () => setSelectedDate(new Date());

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold tracking-tight">
            {format(selectedDate, 'MMMM d, yyyy')}
          </h1>
          <div className="flex items-center rounded-md border p-1 bg-background shadow-sm">
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={prevDay}>
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="h-7 px-3 text-xs" onClick={goToday}>
              Today
            </Button>
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={nextDay}>
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      <div className="flex-1">
        <DroppableDayCell date={selectedDate} isMonthlyView={false}>
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <p className="text-sm">Drag expenses or incomes here</p>
          </div>
        </DroppableDayCell>
      </div>
    </div>
  );
}
