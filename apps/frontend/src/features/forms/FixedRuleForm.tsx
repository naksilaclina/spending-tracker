'use client';

import { useState } from 'react';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';

const fixedRuleSchema = z.object({
  title: z.string().min(2, 'Title is required'),
  amount: z.coerce.number().positive(),
  day_of_month: z.coerce.number().min(1).max(31),
  category_or_source: z.string().min(1, 'Category/Source is required'),
});

type FixedRuleFormValues = z.infer<typeof fixedRuleSchema>;

export function FixedRuleForm({ type, onSubmitSuccess }: { type: 'expense' | 'income', onSubmitSuccess?: () => void }) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<FixedRuleFormValues>({
    resolver: zodResolver(fixedRuleSchema) as any,
    defaultValues: {
      title: '',
      amount: 0,
      day_of_month: 1,
      category_or_source: '',
    },
  });

  async function onSubmit(data: FixedRuleFormValues) {
    setIsSubmitting(true);
    try {
      console.log(`Submitting fixed hidden ${type} rule:`, data);
      if (onSubmitSuccess) onSubmitSuccess();
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField control={form.control} name="title" render={({ field }) => (
          <FormItem><FormLabel>Rule Title</FormLabel><FormControl><Input placeholder={type === 'expense' ? 'e.g. Netflix Subscription' : 'e.g. Base Salary'} {...field} /></FormControl><FormMessage /></FormItem>
        )} />

        <div className="grid grid-cols-2 gap-4">
          <FormField control={form.control} name="amount" render={({ field }) => (
            <FormItem><FormLabel>Amount</FormLabel><FormControl><Input type="number" step="0.01" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
          <FormField control={form.control} name="day_of_month" render={({ field }) => (
            <FormItem><FormLabel>Day of Month (1-31)</FormLabel><FormControl><Input type="number" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
        </div>

        <FormField control={form.control} name="category_or_source" render={({ field }) => (
          <FormItem><FormLabel>{type === 'expense' ? 'Category' : 'Source'}</FormLabel><FormControl><Input placeholder={type === 'expense' ? 'e.g. Subscription' : 'e.g. Employer'} {...field} /></FormControl><FormMessage /></FormItem>
        )} />

        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? 'Saving...' : `Create Fixed ${type === 'expense' ? 'Expense' : 'Income'}`}
        </Button>
      </form>
    </Form>
  );
}
