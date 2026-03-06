'use client';

import { useUIStore } from '@/stores/useUIStore';
import { cn } from '@/lib/utils';
import { ScrollArea } from '../ui/scroll-area';
import { useCashflow, useRisk } from '@/lib/api/endpoints';
import { format, addDays } from 'date-fns';
import { Loader2 } from 'lucide-react';

export function InsightsPanel() {
  const { isInsightsOpen } = useUIStore();
  const todayStr = format(new Date(), 'yyyy-MM-dd');
  const futureStr = format(addDays(new Date(), 30), 'yyyy-MM-dd');

  const { data: cashflowRes, isLoading } = useCashflow(todayStr, futureStr) as { data?: any; isLoading: boolean };
  const { data: riskRes } = useRisk(todayStr, futureStr) as { data?: any };

  const riskStatus = Number(riskRes?.required_extra_funding ?? 0) > 0 ? 'At Risk' : 'Healthy';
  const safeUntil = riskRes?.next_negative_date || 'Projection remains non-negative';
  const fundingGap = Number(cashflowRes?.funding_gap ?? 0);

  return (
    <div className={cn('flex flex-col w-80 border-l bg-zinc-50 dark:bg-zinc-900/50 transition-all duration-300 hidden md:flex', isInsightsOpen ? 'translate-x-0' : 'translate-x-full w-0 border-0 opacity-0')}>
      <div className="p-4 border-b">
        <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">Cashflow Insights</h2>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-4 space-y-6">
          {isLoading ? (
            <div className="flex items-center justify-center p-8 text-muted-foreground"><Loader2 className="h-6 w-6 animate-spin" /></div>
          ) : (
            <>
              <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-4">
                <h3 className="text-sm font-medium mb-1">Health Status</h3>
                <p className={cn('text-2xl font-bold', riskStatus === 'Healthy' ? 'text-green-600 dark:text-green-500' : 'text-destructive')}>{riskStatus}</p>
                <p className="text-xs text-muted-foreground mt-1">Safe until: {safeUntil}</p>
              </div>
              <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-4">
                <h3 className="text-sm font-medium mb-1">Funding Gap</h3>
                <p className={cn('text-2xl font-bold', fundingGap > 0 ? 'text-destructive' : '')}>${fundingGap.toFixed(2)}</p>
                <p className="text-xs text-muted-foreground mt-1">{fundingGap > 0 ? 'Negative balance projected' : 'No negative balance projected'}</p>
              </div>
            </>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
