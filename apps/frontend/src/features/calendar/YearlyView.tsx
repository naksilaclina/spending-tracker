'use client';

import { useUIStore } from '@/stores/useUIStore';
import { format, addYears, subYears } from 'date-fns';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { useYearlyReport } from '@/lib/api/endpoints';

export function YearlyView() {
  const { selectedDate, setSelectedDate } = useUIStore();
  const currentYear = selectedDate.getFullYear();
  const months = Array.from({ length: 12 }, (_, i) => new Date(currentYear, i, 1));
  const report = useYearlyReport(String(currentYear)) as { data?: any };

  const nextYear = () => setSelectedDate(addYears(selectedDate, 1));
  const prevYear = () => setSelectedDate(subYears(selectedDate, 1));
  const goThisYear = () => setSelectedDate(new Date());

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold tracking-tight">{currentYear} Overview</h1>
          <div className="flex items-center rounded-md border p-1 bg-background shadow-sm">
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={prevYear}><ChevronLeft className="h-4 w-4" /></Button>
            <Button variant="ghost" size="sm" className="h-7 px-3 text-xs" onClick={goThisYear}>Current</Button>
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={nextYear}><ChevronRight className="h-4 w-4" /></Button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 flex-1 overflow-auto pb-4">
        {months.map((month) => (
          <Card key={month.toISOString()} className="flex flex-col">
            <CardHeader className="py-3 px-4 border-b bg-muted/30">
              <CardTitle className="text-base font-semibold">{format(month, 'MMMM')}</CardTitle>
            </CardHeader>
            <CardContent className="p-4 flex-1 space-y-3">
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Income</span>
                <span className="font-medium text-green-600 dark:text-green-500">{report.data?.total_income ?? '0.00'}</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Expense</span>
                <span className="font-medium">{report.data?.total_expense ?? '0.00'}</span>
              </div>
              <div className="pt-2 border-t flex justify-between items-center text-sm font-semibold">
                <span>Net</span>
                <span>{report.data?.net_result ?? '0.00'}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
