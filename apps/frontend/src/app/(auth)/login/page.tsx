import { LoginForm } from './login-form';

type LoginPageProps = {
  searchParams: Promise<{
    error?: string;
    message?: string;
  }>;
};

export default async function LoginPage({ searchParams }: LoginPageProps) {
  const params = await searchParams;

  return <LoginForm errorMsg={params.error ?? null} infoMsg={params.message ?? null} />;
}
