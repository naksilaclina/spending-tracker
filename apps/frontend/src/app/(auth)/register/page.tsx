import { RegisterForm } from './register-form';

type RegisterPageProps = {
  searchParams: Promise<{
    error?: string;
  }>;
};

export default async function RegisterPage({ searchParams }: RegisterPageProps) {
  const params = await searchParams;

  return <RegisterForm errorMsg={params.error ?? null} />;
}
