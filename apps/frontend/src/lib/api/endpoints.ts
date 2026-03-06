import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient, unwrapList } from './client';

export function useAuthMe() {
  return useQuery({
    queryKey: ['auth-me'],
    queryFn: () => apiClient.get<any>('/auth/me'),
  });
}

export function useDashboardSummary(range: 'daily' | 'monthly' | 'yearly', date: string) {
  return useQuery({
    queryKey: ['dashboardSummary', range, date],
    queryFn: () => apiClient.get<any>(`/dashboard/summary?range=${range}&date=${date}`),
  });
}

export function useCashflow(start: string, end: string) {
  return useQuery({
    queryKey: ['cashflow', start, end],
    queryFn: () => apiClient.get<any>(`/dashboard/cashflow?start=${start}&end=${end}`),
  });
}

export function useRisk(start: string, end: string) {
  return useQuery({
    queryKey: ['risk', start, end],
    queryFn: () => apiClient.get<any>(`/dashboard/risk?start=${start}&end=${end}`),
  });
}

export function useExpenses() {
  return useQuery({
    queryKey: ['expenses'],
    queryFn: async () => unwrapList<any>(await apiClient.get<any>('/expenses')),
  });
}

export function useCreateExpense() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (newExpense: Record<string, unknown>) => apiClient.post<any>('/expenses', newExpense),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      queryClient.invalidateQueries({ queryKey: ['cashflow'] });
      queryClient.invalidateQueries({ queryKey: ['dashboardSummary'] });
      queryClient.invalidateQueries({ queryKey: ['risk'] });
    },
  });
}

export function useIncomes() {
  return useQuery({
    queryKey: ['incomes'],
    queryFn: async () => unwrapList<any>(await apiClient.get<any>('/incomes')),
  });
}

export function useCreateIncome() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (newIncome: Record<string, unknown>) => apiClient.post<any>('/incomes', newIncome),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['incomes'] });
      queryClient.invalidateQueries({ queryKey: ['cashflow'] });
      queryClient.invalidateQueries({ queryKey: ['dashboardSummary'] });
      queryClient.invalidateQueries({ queryKey: ['risk'] });
    },
  });
}

export function useTemplates() {
  return useQuery({
    queryKey: ['templates'],
    queryFn: async () => unwrapList<any>(await apiClient.get<any>('/templates')),
  });
}

export function useFixedExpenseRules() {
  return useQuery({
    queryKey: ['fixedExpenseRules'],
    queryFn: async () => unwrapList<any>(await apiClient.get<any>('/fixed-expense-rules')),
  });
}

export function useFixedIncomeRules() {
  return useQuery({
    queryKey: ['fixedIncomeRules'],
    queryFn: async () => unwrapList<any>(await apiClient.get<any>('/fixed-income-rules')),
  });
}

export function useLoans() {
  return useQuery({
    queryKey: ['loans'],
    queryFn: async () => unwrapList<any>(await apiClient.get<any>('/loans')),
  });
}

export function useInstallmentPurchases() {
  return useQuery({
    queryKey: ['installmentPurchases'],
    queryFn: async () => unwrapList<any>(await apiClient.get<any>('/installment-purchases')),
  });
}

export function useVehicles() {
  return useQuery({
    queryKey: ['vehicles'],
    queryFn: async () => unwrapList<any>(await apiClient.get<any>('/vehicles')),
  });
}

export function useSettings() {
  return useQuery({
    queryKey: ['settings'],
    queryFn: () => apiClient.get<any>('/settings'),
  });
}

export function useUpdateSettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: Record<string, unknown>) => apiClient.patch<any>('/settings', payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] });
      queryClient.invalidateQueries({ queryKey: ['auth-me'] });
      queryClient.invalidateQueries({ queryKey: ['cashflow'] });
      queryClient.invalidateQueries({ queryKey: ['risk'] });
      queryClient.invalidateQueries({ queryKey: ['dashboardSummary'] });
    },
  });
}

export function useMonthlyReport(month: string) {
  return useQuery({
    queryKey: ['monthly-report', month],
    queryFn: () => apiClient.get<any>(`/reports/monthly?month=${month}`),
  });
}

export function useYearlyReport(year: string) {
  return useQuery({
    queryKey: ['yearly-report', year],
    queryFn: () => apiClient.get<any>(`/reports/yearly?year=${year}`),
  });
}

export function useFundingGaps(start: string, end: string) {
  return useQuery({
    queryKey: ['funding-gaps', start, end],
    queryFn: () => apiClient.get<any>(`/reports/funding-gaps?start=${start}&end=${end}`),
  });
}

export function useVehicleCostsReport() {
  return useQuery({
    queryKey: ['vehicle-costs'],
    queryFn: () => apiClient.get<any>('/reports/vehicle-costs'),
  });
}
