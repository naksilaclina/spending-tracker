import { addDays, format, isBefore, isEqual } from 'date-fns';
import type { ExpenseEntry, IncomeEntry, CashflowPoint, CashflowRiskWindow } from '@/lib/api/types';

interface CashflowInput {
  startDate: Date;
  endDate: Date;
  startingBalance: number;
  expenses: ExpenseEntry[];
  incomes: IncomeEntry[];
}

interface CashflowResult {
  points: CashflowPoint[];
  riskWindows: CashflowRiskWindow[];
  endingBalance: number;
  safeUntilDate: string | null;
  healthStatus: 'healthy' | 'warning' | 'critical';
}

export function calculateCashflow({
  startDate,
  endDate,
  startingBalance,
  expenses,
  incomes,
}: CashflowInput): CashflowResult {
  let currentBalance = startingBalance;
  const points: CashflowPoint[] = [];
  let currentRiskWindow: CashflowRiskWindow | null = null;
  const riskWindows: CashflowRiskWindow[] = [];
  let safeUntilDate: string | null = null;
  let minBalanceAcrossPeriod = startingBalance;

  let currentDate = startDate;
  
  while (isBefore(currentDate, endDate) || isEqual(currentDate, endDate)) {
    const dateStr = format(currentDate, 'yyyy-MM-dd');
    
    // Sum incomes expected/received on this day
    const dayIncomes = incomes.filter(inc => 
      (inc.expected_date === dateStr || inc.received_date === dateStr)
      // Treat missed as still expected for conservative projection, or filter it depending on risk settings
    );
    const dayIncomeTotal = dayIncomes.reduce((sum, inc) => sum + inc.amount, 0);
    
    // Sum expenses planned/due/paid on this day
    const dayExpenses = expenses.filter(exp => 
      (exp.date === dateStr || exp.due_date === dateStr) &&
      exp.status !== 'cancelled' && exp.status !== 'skipped'
    );
    const dayExpenseTotal = dayExpenses.reduce((sum, exp) => sum + exp.amount, 0);

    const net = dayIncomeTotal - dayExpenseTotal;
    currentBalance += net;

    if (currentBalance < minBalanceAcrossPeriod) {
      minBalanceAcrossPeriod = currentBalance;
    }

    points.push({
      date: dateStr,
      income: dayIncomeTotal,
      expense: dayExpenseTotal,
      net,
      running_balance: currentBalance,
    });

    // Risk Window Tracking
    if (currentBalance < 0) {
      if (!safeUntilDate && riskWindows.length === 0) {
        // The day before we went negative
        safeUntilDate = format(subDays(currentDate, 1), 'yyyy-MM-dd'); 
      }
      
      if (!currentRiskWindow) {
        currentRiskWindow = {
          start_date: dateStr,
          end_date: dateStr,
          consecutive_days: 1,
          min_balance: currentBalance,
          funding_gap: Math.abs(currentBalance),
          critical_obligations: [...dayExpenses],
        };
      } else {
        currentRiskWindow.end_date = dateStr;
        currentRiskWindow.consecutive_days += 1;
        if (currentBalance < currentRiskWindow.min_balance) {
          currentRiskWindow.min_balance = currentBalance;
          currentRiskWindow.funding_gap = Math.abs(currentBalance);
        }
        currentRiskWindow.critical_obligations.push(...dayExpenses); // In real app, deduplicate or refine
      }
    } else {
      if (currentRiskWindow) {
        riskWindows.push(currentRiskWindow);
        currentRiskWindow = null;
      }
    }

    currentDate = addDays(currentDate, 1);
  }

  // If period ends while still in a risk window
  if (currentRiskWindow) {
    riskWindows.push(currentRiskWindow);
  }

  let healthStatus: 'healthy' | 'warning' | 'critical' = 'healthy';
  if (riskWindows.length > 0) {
    healthStatus = minBalanceAcrossPeriod < -1000 ? 'critical' : 'warning';
  }

  return {
    points,
    riskWindows,
    endingBalance: currentBalance,
    safeUntilDate,
    healthStatus,
  };
}

function subDays(date: Date, amount: number): Date {
  const result = new Date(date);
  result.setDate(result.getDate() - amount);
  return result;
}
