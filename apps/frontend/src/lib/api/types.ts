export type AppUser = {
  id: string; // Supabase UUID
  email: string;
  first_name?: string;
  last_name?: string;
  currency_preference: string;
  created_at: string;
  updated_at: string;
};

export type Category = string;
export type Subcategory = string;

export type ExpenseType = 'one-time' | 'recurring' | 'fixed-monthly' | 'installment' | 'loan-payment' | 'credit-card-payment' | 'vehicle';
export type IncomeType = 'one-time' | 'recurring' | 'fixed-monthly';

export type ExpenseStatus = 'planned' | 'paid' | 'overdue' | 'skipped' | 'cancelled';
export type IncomeStatus = 'expected' | 'received' | 'missed' | 'delayed';

export type ExpenseEntry = {
  id: string;
  user_id: string;
  title: string;
  amount: number;
  date: string; // YYYY-MM-DD
  due_date?: string; // YYYY-MM-DD
  paid_date?: string; // YYYY-MM-DD
  category: Category;
  subcategory?: Subcategory;
  payment_method?: string;
  notes?: string;
  tags: string[];
  status: ExpenseStatus;
  expense_type: ExpenseType;
  
  // Optional relations depending on the expense type
  fixed_rule_id?: string;
  installment_id?: string;
  loan_id?: string;
  credit_card_id?: string;
  vehicle_id?: string;
  
  // Additional cost breakdowns if relevant
  principal_amount?: number;
  interest_amount?: number;
  fee_amount?: number;

  created_at: string;
  updated_at: string;
};

export type IncomeEntry = {
  id: string;
  user_id: string;
  title: string;
  amount: number;
  expected_date: string; // YYYY-MM-DD
  received_date?: string; // YYYY-MM-DD
  source: string;
  income_type: IncomeType;
  status: IncomeStatus;
  notes?: string;
  tags: string[];
  
  fixed_rule_id?: string;

  created_at: string;
  updated_at: string;
};

export type Template = {
  id: string;
  user_id: string;
  title: string;
  default_amount?: number;
  category: Category;
  subcategory?: Subcategory;
  template_type: 'expense' | 'income';
  icon?: string;
  color?: string;
  created_at: string;
};

export type FixedExpenseRule = {
  id: string;
  user_id: string;
  title: string;
  amount: number;
  day_of_month: number;
  category: Category;
  subcategory?: Subcategory;
  is_active: boolean;
  notes?: string;
  created_at: string;
  updated_at: string;
};

export type FixedIncomeRule = {
  id: string;
  user_id: string;
  title: string;
  amount: number;
  day_of_month: number;
  source: string;
  is_active: boolean;
  notes?: string;
  created_at: string;
  updated_at: string;
};

export type Loan = {
  id: string;
  user_id: string;
  title: string;
  lender: string;
  principal: number;
  total_repayment: number;
  interest_total: number;
  fee_total: number;
  installment_count: number;
  monthly_payment: number;
  first_installment_date: string; // YYYY-MM-DD
  payment_day: number;
  start_date: string; // YYYY-MM-DD
  end_date: string; // YYYY-MM-DD
  notes?: string;
  created_at: string;
  updated_at: string;
};

export type LoanInstallment = {
  id: string;
  loan_id: string;
  installment_number: number;
  due_date: string; // YYYY-MM-DD
  principal_amount: number;
  interest_amount: number;
  fee_amount: number;
  total_amount: number;
  status: 'pending' | 'paid' | 'overdue';
  paid_date?: string; // YYYY-MM-DD
};

export type InstallmentPurchase = {
  id: string;
  user_id: string;
  title: string;
  merchant: string;
  total_amount: number;
  cash_price?: number;
  installment_count: number;
  monthly_payment: number;
  first_installment_date: string; // YYYY-MM-DD
  linked_credit_card_id?: string;
  principal?: number;
  interest?: number;
  fee?: number;
  category: Category;
  notes?: string;
  created_at: string;
  updated_at: string;
};

export type InstallmentPurchaseItem = {
  id: string;
  purchase_id: string;
  installment_number: number;
  due_date: string; // YYYY-MM-DD
  amount: number;
  status: 'pending' | 'paid' | 'overdue';
  paid_date?: string; // YYYY-MM-DD
};

export type CreditCardAccount = {
  id: string;
  user_id: string;
  name: string;
  bank_name: string;
  limit: number;
  statement_day: number;
  due_day: number;
  created_at: string;
  updated_at: string;
};

export type CreditCardPayment = {
  id: string;
  credit_card_id: string;
  statement_date: string; // YYYY-MM
  due_date: string; // YYYY-MM-DD
  minimum_amount: number;
  statement_amount: number;
  paid_amount: number;
  status: 'pending' | 'partially-paid' | 'paid' | 'overdue';
  paid_date?: string; // YYYY-MM-DD
};

export type Vehicle = {
  id: string;
  user_id: string;
  name: string;
  type: string;
  license_plate?: string;
  created_at: string;
  updated_at: string;
};

export type VehicleExpense = {
  id: string;
  vehicle_id: string;
  amount: number;
  date: string; // YYYY-MM-DD
  expense_type: 'fuel' | 'service' | 'tax' | 'insurance' | 'repair' | 'other';
  odometer?: number;
  liters?: number;
  notes?: string;
  status: ExpenseStatus;
  is_recurring: boolean;
  created_at: string;
  updated_at: string;
};

export type CashflowPoint = {
  date: string; // YYYY-MM-DD
  income: number;
  expense: number;
  net: number;
  running_balance: number;
};

export type CashflowRiskWindow = {
  start_date: string; // YYYY-MM-DD
  end_date: string; // YYYY-MM-DD
  consecutive_days: number;
  min_balance: number;
  funding_gap: number;
  critical_obligations: ExpenseEntry[];
};

export type DashboardSummary = {
  period: 'daily' | 'monthly' | 'yearly';
  start_date: string; // YYYY-MM-DD
  end_date: string; // YYYY-MM-DD
  total_income: number;
  total_expense: number;
  net_cashflow: number;
  starting_balance: number;
  ending_balance: number;
  safe_until_date: string | null;
  health_status: 'healthy' | 'warning' | 'critical';
};

export type MonthlyReport = {
  month: string; // YYYY-MM
  total_income: number;
  total_expense: number;
  net_cashflow: number;
  fixed_commitments_total: number;
  interest_cost_total: number;
  worst_projected_balance: number;
  category_breakdown: Record<Category, number>;
};

export type YearlyReport = {
  year: number;
  months: MonthlyReport[];
  total_income: number;
  total_expense: number;
  net_cashflow: number;
};

export type Settings = {
  user_id: string;
  currency: string;
  date_format: string;
  week_start: 0 | 1 | 2 | 3 | 4 | 5 | 6; // 0 = Sunday
  theme: 'light' | 'dark' | 'system';
  opening_balance_defaults: Record<string, number>;
  risk_calculation_preferences: {
    include_planned_expenses: boolean;
    include_expected_incomes: boolean;
    warning_threshold_amount: number;
  };
};
