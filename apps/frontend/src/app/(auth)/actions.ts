'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'

function encodeMessage(message: string) {
  return encodeURIComponent(message)
}

export async function login(formData: FormData) {
  const supabase = await createClient()

  // type-casting here for convenience
  // in production, use zod to validate parsed values
  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  const { error } = await supabase.auth.signInWithPassword(data)

  if (error) {
    const message =
      error.message.toLowerCase().includes('email not confirmed')
        ? 'Please confirm your email before signing in.'
        : error.message || 'Could not authenticate user'
    return redirect(`/login?error=${encodeMessage(message)}`)
  }

  revalidatePath('/dashboard', 'layout')
  redirect(`/dashboard?success=${encodeMessage('Signed in successfully.')}`)
}

export async function signup(formData: FormData) {
  const supabase = await createClient()

  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  const { data: authData, error } = await supabase.auth.signUp(data)

  if (error) {
    return redirect(`/register?error=${encodeMessage(error.message || 'Could not create user')}`)
  }

  if (!authData.session) {
    return redirect(
      `/login?message=${encodeMessage('Account created. Please confirm your email before signing in.')}`
    )
  }

  revalidatePath('/dashboard', 'layout')
  redirect(`/dashboard?success=${encodeMessage('Account created successfully.')}`)
}
