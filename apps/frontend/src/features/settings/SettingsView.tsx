'use client';

import { useEffect, useMemo, useState } from 'react';

import { useAuthMe, useSettings, useUpdateSettings } from '@/lib/api/endpoints';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

type SettingsFormState = {
  display_name: string;
  timezone: string;
  currency: string;
  opening_balance: string;
};

export function SettingsView() {
  const { data: profile, isLoading: isProfileLoading } = useAuthMe() as { data?: Record<string, string>; isLoading: boolean };
  const { data: settings, isLoading: isSettingsLoading } = useSettings() as { data?: Record<string, string>; isLoading: boolean };
  const updateSettings = useUpdateSettings();

  const initial = useMemo<SettingsFormState>(
    () => ({
      display_name: settings?.display_name ?? profile?.display_name ?? '',
      timezone: settings?.timezone ?? 'UTC',
      currency: settings?.currency ?? 'USD',
      opening_balance: settings?.opening_balance ?? '0.00',
    }),
    [profile, settings]
  );

  const [form, setForm] = useState<SettingsFormState>(initial);

  useEffect(() => {
    setForm(initial);
  }, [initial]);

  const isLoading = isProfileLoading || isSettingsLoading;

  async function onSave() {
    try {
      await updateSettings.mutateAsync(form);
    } catch {}
  }

  return (
    <div className="flex flex-col h-full space-y-6">
      <div className="flex items-center justify-between border-b pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
          <p className="text-sm text-muted-foreground">Manage your account settings and preferences.</p>
        </div>
      </div>

      <div className="grid gap-6 max-w-3xl">
        <div className="space-y-4">
          <h3 className="text-lg font-medium">Profile Basics</h3>
          <div className="bg-card p-4 rounded-lg border text-sm space-y-4">
            <div className="space-y-2">
              <span className="text-muted-foreground">Email</span>
              <div className="font-medium">{profile?.email ?? 'Loading...'}</div>
            </div>
            <div className="space-y-2">
              <span className="text-muted-foreground">Display name</span>
              <Input value={form.display_name} disabled={isLoading || updateSettings.isPending} onChange={(event) => setForm((current) => ({ ...current, display_name: event.target.value }))} />
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h3 className="text-lg font-medium">Preferences</h3>
          <div className="bg-card p-4 rounded-lg border text-sm space-y-4">
            <div className="grid gap-2">
              <span className="text-muted-foreground">Currency</span>
              <Input value={form.currency} disabled={isLoading || updateSettings.isPending} onChange={(event) => setForm((current) => ({ ...current, currency: event.target.value.toUpperCase() }))} />
            </div>
            <div className="grid gap-2">
              <span className="text-muted-foreground">Timezone</span>
              <Input value={form.timezone} disabled={isLoading || updateSettings.isPending} onChange={(event) => setForm((current) => ({ ...current, timezone: event.target.value }))} />
            </div>
            <div className="grid gap-2">
              <span className="text-muted-foreground">Opening Balance</span>
              <Input type="number" step="0.01" value={form.opening_balance} disabled={isLoading || updateSettings.isPending} onChange={(event) => setForm((current) => ({ ...current, opening_balance: event.target.value }))} />
            </div>
            <div className="pt-2">
              <Button onClick={onSave} disabled={isLoading || updateSettings.isPending}>{updateSettings.isPending ? 'Saving...' : 'Save Settings'}</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
