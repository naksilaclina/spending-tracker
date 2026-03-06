from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from apps.credit_cards.models import CreditCardAccount
from apps.finance.models import Category
from apps.fixed_rules.models import FixedExpenseRule
from apps.fixed_rules.services import RuleMaterializationService
from apps.installments.models import InstallmentPurchase
from apps.installments.services import InstallmentScheduleService
from apps.loans.models import Loan
from apps.loans.services import LoanScheduleService
from apps.users.models import UserProfile

User = get_user_model()


@pytest.mark.django_db
def test_fixed_rule_materialization_clamps_end_of_month_without_duplicates():
    user = User.objects.create(username="rules-user")
    UserProfile.objects.create(user=user, supabase_user_id="rules-sub", email="rules@example.com")
    category = Category.objects.create(user=user, kind="expense", name="Bills")
    rule = FixedExpenseRule.objects.create(user=user, title="Rent", default_amount=Decimal("100.00"), category=category, due_day="31", starts_on=date(2026, 1, 1))

    service = RuleMaterializationService()
    first = service.materialize(user, date(2026, 2, 1), date(2026, 2, 28), persist=True)
    second = service.materialize(user, date(2026, 2, 1), date(2026, 2, 28), persist=True)

    assert len(first["expenses"]) == 1
    assert first["expenses"][0].due_on == date(2026, 2, 28)
    assert len(second["expenses"]) == 1


@pytest.mark.django_db
def test_loan_schedule_preserves_totals():
    user = User.objects.create(username="loan-user")
    UserProfile.objects.create(user=user, supabase_user_id="loan-sub", email="loan@example.com")
    loan = Loan.objects.create(user=user, title="Car Loan", lender="Bank", principal_total=Decimal("900.00"), repayment_total=Decimal("990.00"), interest_total=Decimal("60.00"), fee_total=Decimal("30.00"), installment_count=3, monthly_payment=Decimal("330.00"), payment_day=15, start_date=date(2026, 1, 1), first_installment_date=date(2026, 1, 15))

    schedule = LoanScheduleService().regenerate(loan)

    assert len(schedule) == 3
    assert sum(item.principal_amount for item in schedule) == Decimal("900.00")
    assert sum(item.interest_amount for item in schedule) == Decimal("60.00")
    assert sum(item.fee_amount for item in schedule) == Decimal("30.00")


@pytest.mark.django_db
def test_installment_schedule_preserves_totals_and_card_link():
    user = User.objects.create(username="installment-user")
    UserProfile.objects.create(user=user, supabase_user_id="installment-sub", email="installment@example.com")
    category = Category.objects.create(user=user, kind="expense", name="Tech")
    card = CreditCardAccount.objects.create(user=user, name="Visa", statement_due_day=10)
    purchase = InstallmentPurchase.objects.create(user=user, title="Laptop", merchant="Store", total_amount=Decimal("1200.00"), principal_total=Decimal("1000.00"), interest_total=Decimal("150.00"), fee_total=Decimal("50.00"), installment_count=4, first_installment_date=date(2026, 1, 10), linked_credit_card=card, category=category)

    schedule = InstallmentScheduleService().regenerate(purchase)

    assert len(schedule) == 4
    assert purchase.linked_credit_card_id == card.id
    assert sum(item.amount_total for item in schedule) == Decimal("1200.00")
