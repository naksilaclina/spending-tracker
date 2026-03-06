'use client';

import { format } from 'date-fns';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useFundingGaps, useMonthlyReport, useVehicleCostsReport, useYearlyReport } from '@/lib/api/endpoints';

export function ReportsView() {
  const now = new Date();
  const month = format(now, 'yyyy-MM');
  const year = format(now, 'yyyy');
  const start = `${year}-01-01`;
  const end = `${year}-12-31`;

  const { data: monthly } = useMonthlyReport(month) as { data?: any };
  const { data: yearly } = useYearlyReport(year) as { data?: any };
  const { data: funding } = useFundingGaps(start, end) as { data?: any };
  const { data: vehicleCosts } = useVehicleCostsReport() as { data?: any };

  return (
    <div className="flex flex-col h-full space-y-6">
      <div className="flex items-center justify-between border-b pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Reports & Analytics</h1>
          <p className="text-sm text-muted-foreground">Comprehensive insights into your financial health.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <Card>
          <CardHeader><CardTitle className="text-sm font-medium text-muted-foreground">Total Income (This Month)</CardTitle></CardHeader>
          <CardContent><div className="text-2xl font-bold text-green-600 dark:text-green-500">{monthly?.total_income ?? '0.00'}</div></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-sm font-medium text-muted-foreground">Total Expenses (This Month)</CardTitle></CardHeader>
          <CardContent><div className="text-2xl font-bold">{monthly?.total_expense ?? '0.00'}</div></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-sm font-medium text-muted-foreground">Funding Gaps Detected</CardTitle></CardHeader>
          <CardContent><div className="text-2xl font-bold text-destructive">{funding?.negative_windows?.length ?? 0}</div></CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1">
        <Card className="flex flex-col">
          <CardHeader><CardTitle className="text-base">Yearly Net Result</CardTitle></CardHeader>
          <CardContent className="flex-1 border-t p-6 text-sm">
            <div className="font-semibold text-lg">{yearly?.net_result ?? '0.00'}</div>
            <div className="text-muted-foreground mt-2">Year: {year}</div>
          </CardContent>
        </Card>
        <Card className="flex flex-col">
          <CardHeader><CardTitle className="text-base">Loan vs Interest Burden</CardTitle></CardHeader>
          <CardContent className="flex-1 border-t p-6 text-sm space-y-2">
            <div>Loan burden: <span className="font-semibold">{monthly?.loan_burden ?? '0.00'}</span></div>
            <div>Interest paid: <span className="font-semibold">{monthly?.interest_paid ?? '0.00'}</span></div>
            <div>Fees paid: <span className="font-semibold">{monthly?.fees_paid ?? '0.00'}</span></div>
          </CardContent>
        </Card>
        <Card className="flex flex-col">
          <CardHeader><CardTitle className="text-base">Vehicle Costs Breakdown</CardTitle></CardHeader>
          <CardContent className="flex-1 border-t p-6 text-sm">
            <div className="font-semibold text-lg">{vehicleCosts?.vehicle_cost_total ?? '0.00'}</div>
          </CardContent>
        </Card>
        <Card className="flex flex-col">
          <CardHeader><CardTitle className="text-base">Negative Cashflow Periods</CardTitle></CardHeader>
          <CardContent className="flex-1 border-t p-6 text-sm space-y-2">
            {(funding?.negative_windows ?? []).length === 0 ? (
              <div className="text-muted-foreground">No negative window detected.</div>
            ) : (
              (funding?.negative_windows ?? []).map((window: { start: string; end: string; worst_balance: string }, index: number) => (
                <div key={`${window.start}-${index}`} className="rounded border p-3">
                  <div>{window.start} - {window.end}</div>
                  <div className="text-muted-foreground">Worst balance: {window.worst_balance}</div>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
