'use client';

import { useDroppable } from '@dnd-kit/core';
import { cn } from '@/lib/utils';
import { format, isToday } from 'date-fns';

interface DroppableDayCellProps {
  date: Date;
  children?: React.ReactNode;
  isMonthlyView?: boolean;
}

export function DroppableDayCell({ date, children, isMonthlyView }: DroppableDayCellProps) {
  const dateStr = format(date, 'yyyy-MM-dd');
  const today = isToday(date);
  
  const { isOver, setNodeRef } = useDroppable({
    id: `day-${dateStr}`,
    data: {
      type: 'day',
      date: dateStr,
    },
  });

  return (
    <div
      ref={setNodeRef}
      className={cn(
        "flex flex-col border rounded-md min-h-[120px] transition-colors bg-card",
        isOver && "ring-2 ring-primary ring-inset bg-primary/5",
        today && "border-primary/50",
        isMonthlyView ? "p-2" : "p-4"
      )}
    >
      <div className="flex items-center justify-between mb-2">
        <span className={cn(
          "text-sm font-medium",
          today ? "text-primary" : "text-muted-foreground"
        )}>
          {isMonthlyView ? format(date, 'd') : format(date, 'EEEE, MMMM d')}
        </span>
      </div>
      
      <div className="flex-1 flex flex-col gap-1">
        {children}
      </div>
    </div>
  );
}
