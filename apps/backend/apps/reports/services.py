from calendar import monthrange
from datetime import date, datetime
from decimal import Decimal

from django.db.models import Q, Sum
from django.db.models.functions import Coalesce

from apps.cashflow.services import CashflowService
from apps.credit_cards.models import CreditCardPayment
from apps.expenses.models import ExpenseEntry
from apps.fixed_rules.models import FixedExpenseRule, FixedIncomeRule
from apps.income.models import IncomeEntry
from apps.vehicles.models import VehicleExpense


class ReportingService:
    @staticmethod
    def parse_date_param(value: str | None) -> date:
        if not value:
            raise ValueError("A valid date parameter is required.")
        return datetime.strptime(value, "%Y-%m-%d").date()

    @staticmethod
    def parse_month(month: str) -> tuple[date, date]:
        start = datetime.strptime(month, "%Y-%m").date().replace(day=1)
        end = start.replace(day=monthrange(start.year, start.month)[1])
        return start, end

    @staticmethod
    def parse_year(year: str) -> tuple[date, date]:
        year_int = int(year)
        return date(year_int, 1, 1), date(year_int, 12, 31)

    def _range(self, range_name: str, date_value: str | None) -> tuple[date, date]:
        anchor = self.parse_date_param(date_value)
        if range_name == "daily":
            return anchor, anchor
        if range_name == "yearly":
            return date(anchor.year, 1, 1), date(anchor.year, 12, 31)
        return anchor.replace(day=1), anchor.replace(day=monthrange(anchor.year, anchor.month)[1])

    def _ensure_currency(self, user, start: date, end: date):
        base = user.profile.currency
        if ExpenseEntry.objects.filter(user=user, incurred_on__range=(start, end)).exclude(currency=base).exists():
            raise ValueError("Expense currency mismatch for reporting period.")
        if IncomeEntry.objects.filter(user=user, expected_on__range=(start, end)).exclude(currency=base).exists():
            raise ValueError("Income currency mismatch for reporting period.")

    def dashboard_summary(self, user, range_name: str, date_value: str | None):
        start, end = self._range(range_name, date_value)
        report = self.summary(user, start, end)
        report["range"] = range_name
        return report

    def summary(self, user, start: date, end: date):
        self._ensure_currency(user, start, end)
        expense_qs = ExpenseEntry.objects.filter(user=user, incurred_on__range=(start, end))
        income_qs = IncomeEntry.objects.filter(user=user, expected_on__range=(start, end))
        vehicle_qs = VehicleExpense.objects.filter(user=user, date__range=(start, end))
        card_qs = CreditCardPayment.objects.filter(user=user, due_on__range=(start, end))

        total_income = income_qs.aggregate(total=Coalesce(Sum("amount"), Decimal("0.00")))["total"]
        total_expense = expense_qs.aggregate(total=Coalesce(Sum("amount_total"), Decimal("0.00")))["total"]
        fixed_expense_total = expense_qs.filter(entry_type="fixed").aggregate(total=Coalesce(Sum("amount_total"), Decimal("0.00")))["total"]
        fixed_income_total = income_qs.filter(source_rule__isnull=False).aggregate(total=Coalesce(Sum("amount"), Decimal("0.00")))["total"]
        mandatory_total = expense_qs.filter(is_mandatory=True).aggregate(total=Coalesce(Sum("amount_total"), Decimal("0.00")))["total"]
        optional_total = total_expense - mandatory_total
        interest_paid = expense_qs.aggregate(total=Coalesce(Sum("interest_amount"), Decimal("0.00")))["total"] + card_qs.aggregate(total=Coalesce(Sum("interest_amount"), Decimal("0.00")))["total"]
        principal_paid = expense_qs.aggregate(total=Coalesce(Sum("principal_amount"), Decimal("0.00")))["total"] + card_qs.aggregate(total=Coalesce(Sum("principal_amount"), Decimal("0.00")))["total"]
        fees_paid = expense_qs.aggregate(total=Coalesce(Sum("fee_amount"), Decimal("0.00")))["total"] + card_qs.aggregate(total=Coalesce(Sum("fee_amount"), Decimal("0.00")))["total"]
        vehicle_cost_total = vehicle_qs.aggregate(total=Coalesce(Sum("amount_total"), Decimal("0.00")))["total"]
        overdue_obligations = expense_qs.filter(status="overdue").count() + card_qs.filter(status="overdue").count()
        delayed_incomes = income_qs.filter(status__in=["missed", "delayed"]).count()
        risk = RiskAnalysisService().build(user, start, end)

        return {
            "currency": user.profile.currency,
            "start": start,
            "end": end,
            "total_income": total_income,
            "total_expense": total_expense,
            "net_result": total_income - total_expense,
            "fixed_monthly_expense_total": fixed_expense_total,
            "fixed_monthly_income_total": fixed_income_total,
            "mandatory_commitment_total": mandatory_total,
            "optional_spending_total": optional_total,
            "interest_paid": interest_paid,
            "principal_paid": principal_paid,
            "fees_paid": fees_paid,
            "loan_burden": expense_qs.filter(entry_type="loan_payment").aggregate(total=Coalesce(Sum("amount_total"), Decimal("0.00")))["total"],
            "credit_card_finance_cost": card_qs.aggregate(total=Coalesce(Sum("interest_amount"), Decimal("0.00")))["total"] + card_qs.aggregate(total=Coalesce(Sum("fee_amount"), Decimal("0.00")))["total"],
            "vehicle_cost_total": vehicle_cost_total,
            "overdue_obligations": overdue_obligations,
            "missed_delayed_incomes": delayed_incomes,
            "negative_cashflow_windows": risk["negative_windows"],
            "funding_gap_total": risk["required_extra_funding"],
        }

    def monthly(self, user, month: str):
        start, end = self.parse_month(month)
        return self.summary(user, start, end)

    def yearly(self, user, year: str):
        start, end = self.parse_year(year)
        return self.summary(user, start, end)

    def interest(self, user):
        total = ExpenseEntry.objects.filter(user=user).aggregate(total=Coalesce(Sum("interest_amount"), Decimal("0.00")))["total"]
        total += CreditCardPayment.objects.filter(user=user).aggregate(total=Coalesce(Sum("interest_amount"), Decimal("0.00")))["total"]
        return {"currency": user.profile.currency, "interest_paid": total}

    def principal(self, user):
        total = ExpenseEntry.objects.filter(user=user).aggregate(total=Coalesce(Sum("principal_amount"), Decimal("0.00")))["total"]
        total += CreditCardPayment.objects.filter(user=user).aggregate(total=Coalesce(Sum("principal_amount"), Decimal("0.00")))["total"]
        return {"currency": user.profile.currency, "principal_paid": total}

    def vehicle_costs(self, user):
        total = VehicleExpense.objects.filter(user=user).aggregate(total=Coalesce(Sum("amount_total"), Decimal("0.00")))["total"]
        return {"currency": user.profile.currency, "vehicle_cost_total": total}

    def funding_gaps(self, user, start: date, end: date):
        risk = RiskAnalysisService().build(user, start, end)
        return {
            "currency": user.profile.currency,
            "required_extra_funding": risk["required_extra_funding"],
            "critical_obligations": risk["critical_obligations"],
            "negative_windows": risk["negative_windows"],
        }


class RiskAnalysisService:
    def build(self, user, start: date, end: date):
        cashflow = CashflowService().build(user, start, end)
        next_negative_date = None
        critical_obligations = []
        worst_balance = cashflow["minimum_balance"]

        for row in cashflow["rows"]:
            if row["closing_balance"] < 0 and next_negative_date is None:
                next_negative_date = row["date"]
                critical_obligations = sorted(row["obligations"], key=lambda item: item["amount"], reverse=True)[:5]
                break

        negative_windows = [
            {
                "start": window["start"],
                "end": window["end"],
                "number_of_negative_days": (window["end"] - window["start"]).days + 1,
                "worst_balance": window["worst_balance"],
            }
            for window in cashflow["negative_windows"]
        ]
        return {
            "currency": user.profile.currency,
            "next_negative_date": next_negative_date,
            "negative_windows": negative_windows,
            "number_of_negative_days": sum(window["number_of_negative_days"] for window in negative_windows),
            "worst_balance": worst_balance,
            "required_extra_funding": cashflow["funding_gap"],
            "critical_obligations": critical_obligations,
            "optional_expenses_to_postpone": [item for item in critical_obligations if not item["mandatory"]],
        }
