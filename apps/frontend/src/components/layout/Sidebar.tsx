'use client';

import { useUIStore } from '@/stores/useUIStore';
import { cn } from '@/lib/utils';
import { ScrollArea } from '../ui/scroll-area';
import { DraggableTemplateGroup } from '@/features/board/DraggableTemplateGroup'; // Will create this next

const MOCK_EXPENSE_TEMPLATES = [
  'Rent', 'Grocery', 'Transportation', 'Coffee', 'Internet',
  'Electricity', 'Water Bill', 'Natural Gas', 'Credit Card Payment',
  'Subscription', 'Shopping', 'Health', 'Education', 'Insurance',
  'Phone Bill', 'Building Maintenance Fee', 'Fuel', 'Car Repair',
];

const MOCK_INCOME_TEMPLATES = [
  'Salary', 'Passive Income', 'Freelance Income', 'Bonus',
  'Dividend', 'Rent Income', 'Refund', 'Sale Income',
];

export function Sidebar() {
  const { isSidebarOpen } = useUIStore();

  return (
    <div
      className={cn(
        "flex flex-col w-64 border-r bg-background transition-all duration-300 overflow-hidden",
        isSidebarOpen ? "translate-x-0" : "-translate-x-full w-0 border-0"
      )}
    >
      <div className="p-4 border-b">
        <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">Templates</h2>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-4 space-y-6">
          <DraggableTemplateGroup title="Drag Incomes" items={MOCK_INCOME_TEMPLATES} type="income" />
          <DraggableTemplateGroup title="Drag Expenses" items={MOCK_EXPENSE_TEMPLATES} type="expense" />
        </div>
      </ScrollArea>
    </div>
  );
}
