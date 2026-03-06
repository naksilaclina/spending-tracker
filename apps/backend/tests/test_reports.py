from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from apps.expenses.models import ExpenseEntry
from apps.income.models import IncomeEntry
from apps.reports.services import ReportingService
from apps.users.models import UserProfile
from apps.vehicles.models import Vehicle, VehicleExpense

User = get_user_model()


@pytest.mark.django_db
def test_reporting_aggregates_principal_interest_and_vehicle_costs():
    user = User.objects.create(username="report-user")
    UserProfile.objects.create(user=user, supabase_user_id="report-sub", email="report@example.com")
    IncomeEntry.objects.create(user=user, title="Salary", amount=Decimal("5000.00"), currency="USD", expected_on=date(2026, 1, 5), status="received")
    ExpenseEntry.objects.create(user=user, title="Loan Payment", amount_total=Decimal("300.00"), principal_amount=Decimal("250.00"), interest_amount=Decimal("40.00"), fee_amount=Decimal("10.00"), currency="USD", incurred_on=date(2026, 1, 10), due_on=date(2026, 1, 10), status="paid", entry_type="loan_payment", is_mandatory=True)
    vehicle = Vehicle.objects.create(user=user, name="Car")
    VehicleExpense.objects.create(user=user, vehicle=vehicle, title="Fuel", expense_type="fuel", amount_total=Decimal("75.00"), date=date(2026, 1, 12))

    report = ReportingService().monthly(user, "2026-01")

    assert report["total_income"] == Decimal("5000.00")
    assert report["interest_paid"] == Decimal("40.00")
    assert report["principal_paid"] == Decimal("250.00")
    assert report["fees_paid"] == Decimal("10.00")
    assert report["vehicle_cost_total"] == Decimal("75.00")
