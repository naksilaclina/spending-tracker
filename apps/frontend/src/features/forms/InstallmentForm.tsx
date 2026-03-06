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

const purchaseSchema = z.object({
  title: z.string().min(2, 'Title is required'),
  merchant: z.string().min(1, 'Merchant is required'),
  total_amount: z.coerce.number().positive(),
  installment_count: z.coerce.number().positive().int(),
  first_installment_date: z.string().min(1),
  credit_card_id: z.string().optional(),
  category: z.string().optional(),
  notes: z.string().optional(),
});

type PurchaseFormValues = z.infer<typeof purchaseSchema>;

export function InstallmentForm({ onSubmitSuccess }: { onSubmitSuccess?: () => void }) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<PurchaseFormValues>({
    resolver: zodResolver(purchaseSchema) as any,
    defaultValues: {
      title: '',
      merchant: '',
      total_amount: 0,
      installment_count: 6,
      first_installment_date: format(new Date(), 'yyyy-MM-dd'),
      credit_card_id: '',
      category: '',
      notes: '',
    },
  });

  async function onSubmit(data: PurchaseFormValues) {
    setIsSubmitting(true);
    try {
      console.log('Submitting installment:', data);
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
            <FormItem><FormLabel>Item Title</FormLabel><FormControl><Input placeholder="e.g. MacBook Pro" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
          <FormField control={form.control} name="merchant" render={({ field }) => (
            <FormItem><FormLabel>Merchant</FormLabel><FormControl><Input placeholder="e.g. Apple Store" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField control={form.control} name="total_amount" render={({ field }) => (
            <FormItem><FormLabel>Total Amount</FormLabel><FormControl><Input type="number" step="0.01" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
          <FormField control={form.control} name="installment_count" render={({ field }) => (
            <FormItem><FormLabel>Number of Months</FormLabel><FormControl><Input type="number" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField control={form.control} name="first_installment_date" render={({ field }) => (
            <FormItem><FormLabel>First Installment Date</FormLabel><FormControl><Input type="date" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
          <FormField control={form.control} name="category" render={({ field }) => (
            <FormItem><FormLabel>Category</FormLabel><FormControl><Input placeholder="e.g. Electronics" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
        </div>

        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? 'Saving...' : 'Create Installment Plan'}
        </Button>
      </form>
    </Form>
  );
}
