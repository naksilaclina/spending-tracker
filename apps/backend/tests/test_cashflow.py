from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from apps.cashflow.services import CashflowService
from apps.expenses.models import ExpenseEntry
from apps.income.models import IncomeEntry
from apps.reports.services import RiskAnalysisService
from apps.users.models import UserProfile

User = get_user_model()


@pytest.mark.django_db
def test_cashflow_detects_negative_window_and_funding_gap():
    user = User.objects.create(username="cashflow-user")
    UserProfile.objects.create(user=user, supabase_user_id="cashflow-sub", email="cash@example.com", opening_balance=Decimal("50.00"), opening_balance_date=date(2026, 1, 1))
    IncomeEntry.objects.create(user=user, title="Salary", amount=Decimal("100.00"), currency="USD", expected_on=date(2026, 1, 5), status="expected")
    ExpenseEntry.objects.create(user=user, title="Rent", amount_total=Decimal("120.00"), principal_amount=Decimal("120.00"), interest_amount=Decimal("0.00"), fee_amount=Decimal("0.00"), currency="USD", incurred_on=date(2026, 1, 2), due_on=date(2026, 1, 2), status="planned", entry_type="fixed")
    ExpenseEntry.objects.create(user=user, title="Utilities", amount_total=Decimal("80.00"), principal_amount=Decimal("80.00"), interest_amount=Decimal("0.00"), fee_amount=Decimal("0.00"), currency="USD", incurred_on=date(2026, 1, 3), due_on=date(2026, 1, 3), status="planned", entry_type="one_time")

    result = CashflowService().build(user, date(2026, 1, 1), date(2026, 1, 7))

    assert result["funding_gap"] == Decimal("150.00")
    assert result["negative_windows"][0]["start"] == date(2026, 1, 2)


@pytest.mark.django_db
def test_risk_analysis_identifies_next_negative_date():
    user = User.objects.create(username="risk-user")
    UserProfile.objects.create(user=user, supabase_user_id="risk-sub", email="risk@example.com", opening_balance=Decimal("0.00"), opening_balance_date=date(2026, 1, 1))
    ExpenseEntry.objects.create(user=user, title="Loan", amount_total=Decimal("10.00"), principal_amount=Decimal("10.00"), interest_amount=Decimal("0.00"), fee_amount=Decimal("0.00"), currency="USD", incurred_on=date(2026, 1, 2), due_on=date(2026, 1, 2), status="planned", entry_type="loan_payment", is_mandatory=True)

    result = RiskAnalysisService().build(user, date(2026, 1, 1), date(2026, 1, 3))

    assert result["next_negative_date"] == date(2026, 1, 2)
    assert result["required_extra_funding"] == Decimal("10.00")
