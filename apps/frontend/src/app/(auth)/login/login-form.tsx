'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { AlertCircle } from 'lucide-react';

import { login } from '../actions';
import { Button } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

type LoginFormProps = {
  errorMsg?: string | null;
  infoMsg?: string | null;
};

export function LoginForm({ errorMsg, infoMsg }: LoginFormProps) {
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setIsLoading(false);
  }, [errorMsg, infoMsg]);

  const form = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: '', password: '' },
  });

  async function onSubmit(values: z.infer<typeof loginSchema>) {
    setIsLoading(true);
    const formData = new FormData();
    formData.append('email', values.email);
    formData.append('password', values.password);
    await login(formData);
  }

  return (
    <div className="sm:mx-auto sm:w-full sm:max-w-md">
      <Card className="shadow-lg border-0 ring-1 ring-zinc-200 dark:ring-zinc-800">
        <CardHeader className="space-y-1 items-center">
          <CardTitle className="text-2xl font-bold tracking-tight">Sign in</CardTitle>
          <CardDescription className="text-center">Enter your email and password to access your finance OS</CardDescription>
        </CardHeader>
        <CardContent>
          {infoMsg && (
            <div className="mb-4 rounded-md bg-emerald-500/15 p-3 text-sm text-emerald-600 dark:text-emerald-400">
              <p>{infoMsg}</p>
            </div>
          )}
          {errorMsg && (
            <div className="mb-4 flex items-center gap-2 rounded-md bg-destructive/15 p-3 text-sm text-destructive">
              <AlertCircle className="h-4 w-4" />
              <p>{errorMsg}</p>
            </div>
          )}

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField control={form.control} name="email" render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl><Input placeholder="name@example.com" type="email" autoComplete="email" disabled={isLoading} {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />
              <FormField control={form.control} name="password" render={({ field }) => (
                <FormItem>
                  <div className="flex items-center justify-between">
                    <FormLabel>Password</FormLabel>
                    <Link href="/forgot-password" className="text-xs font-medium text-primary hover:underline">
                      Forgot password?
                    </Link>
                  </div>
                  <FormControl><Input type="password" autoComplete="current-password" disabled={isLoading} {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />
              <Button type="submit" className="w-full" disabled={isLoading}>{isLoading ? 'Signing in...' : 'Sign in'}</Button>
            </form>
          </Form>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-muted-foreground">Don&apos;t have an account? <Link href="/register" className="font-semibold text-primary hover:text-primary/90 underline-offset-4 hover:underline">Sign up</Link></p>
        </CardFooter>
      </Card>
    </div>
  );
}
