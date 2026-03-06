'use client';

import { useState } from 'react';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { format } from 'date-fns';

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

const loanSchema = z.object({
  title: z.string().min(2, 'Title is required'),
  lender: z.string().min(1, 'Lender is required'),
  principal: z.coerce.number().positive(),
  interest_total: z.coerce.number().min(0),
  installment_count: z.coerce.number().positive().int(),
  payment_day: z.coerce.number().min(1).max(31),
  first_installment_date: z.string().min(1),
  notes: z.string().optional(),
});

type LoanFormValues = z.infer<typeof loanSchema>;

export function LoanForm({ onSubmitSuccess }: { onSubmitSuccess?: () => void }) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<LoanFormValues>({
    resolver: zodResolver(loanSchema) as any,
    defaultValues: {
      title: '',
      lender: '',
      principal: 0,
      interest_total: 0,
      installment_count: 12,
      payment_day: 1,
      first_installment_date: format(new Date(), 'yyyy-MM-dd'),
      notes: '',
    },
  });

  async function onSubmit(data: LoanFormValues) {
    setIsSubmitting(true);
    try {
      console.log('Submitting loan:', data);
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
        <div className="grid grid-cols-2 gap-4">
          <FormField control={form.control} name="title" render={({ field }) => (
            <FormItem><FormLabel>Loan Title</FormLabel><FormControl><Input placeholder="e.g. Car Loan" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
          <FormField control={form.control} name="lender" render={({ field }) => (
            <FormItem><FormLabel>Lender / Bank</FormLabel><FormControl><Input placeholder="e.g. Chase" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField control={form.control} name="principal" render={({ field }) => (
            <FormItem><FormLabel>Principal Amount</FormLabel><FormControl><Input type="number" step="0.01" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
          <FormField control={form.control} name="interest_total" render={({ field }) => (
            <FormItem><FormLabel>Total Interest</FormLabel><FormControl><Input type="number" step="0.01" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField control={form.control} name="installment_count" render={({ field }) => (
            <FormItem><FormLabel>Number of Months</FormLabel><FormControl><Input type="number" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
          <FormField control={form.control} name="payment_day" render={({ field }) => (
            <FormItem><FormLabel>Payment Day (1-31)</FormLabel><FormControl><Input type="number" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
        </div>

        <FormField control={form.control} name="first_installment_date" render={({ field }) => (
          <FormItem><FormLabel>First Installment Date</FormLabel><FormControl><Input type="date" {...field} /></FormControl><FormMessage /></FormItem>
        )} />

        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? 'Saving...' : 'Generate Loan Plan'}
        </Button>
      </form>
    </Form>
  );
}
