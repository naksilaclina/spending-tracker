'use client';

import { useState } from 'react';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { format } from 'date-fns';

import { Button } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';

const vehicleExpenseSchema = z.object({
  vehicle_name: z.string().min(1, 'Vehicle is required'),
  expense_type: z.string().min(1, 'Type is required'),
  amount: z.coerce.number().positive(),
  date: z.string().min(1),
  odometer: z.coerce.number().optional(),
  liters: z.coerce.number().optional(),
  notes: z.string().optional(),
});

export function VehicleExpenseForm({ onSubmitSuccess }: { onSubmitSuccess?: () => void }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const form = useForm<z.infer<typeof vehicleExpenseSchema>>({
    resolver: zodResolver(vehicleExpenseSchema) as any,
    defaultValues: { vehicle_name: '', expense_type: 'Fuel', amount: 0, date: format(new Date(), 'yyyy-MM-dd') }
  });

  async function onSubmit(data: z.infer<typeof vehicleExpenseSchema>) {
    setIsSubmitting(true);
    console.log('Vehicle Expense:', data);
    if(onSubmitSuccess){ onSubmitSuccess();}
    setIsSubmitting(false);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <FormField control={form.control} name="vehicle_name" render={({ field }) => (
            <FormItem><FormLabel>Vehicle Name</FormLabel><FormControl><Input placeholder="e.g. Daily Driver" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
          <FormField control={form.control} name="expense_type" render={({ field }) => (
            <FormItem><FormLabel>Expense Type</FormLabel><FormControl><Input placeholder="e.g. Fuel, Maintenance" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
        </div>
        <div className="grid grid-cols-2 gap-4">
           <FormField control={form.control} name="amount" render={({ field }) => (
            <FormItem><FormLabel>Amount</FormLabel><FormControl><Input type="number" step="0.01" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
           <FormField control={form.control} name="date" render={({ field }) => (
            <FormItem><FormLabel>Date</FormLabel><FormControl><Input type="date" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
        </div>
        <div className="grid grid-cols-2 gap-4">
           <FormField control={form.control} name="odometer" render={({ field }) => (
            <FormItem><FormLabel>Odometer (optional)</FormLabel><FormControl><Input type="number" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
           <FormField control={form.control} name="liters" render={({ field }) => (
            <FormItem><FormLabel>Liters (for fuel)</FormLabel><FormControl><Input type="number" step="0.1" {...field} /></FormControl><FormMessage /></FormItem>
          )} />
        </div>
        <Button type="submit" className="w-full" disabled={isSubmitting}>Log Vehicle Expense</Button>
      </form>
    </Form>
  )
}
