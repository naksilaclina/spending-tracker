from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

from apps.credit_cards.models import CreditCardPayment
from apps.expenses.models import ExpenseEntry
from apps.fixed_rules.services import RuleMaterializationService
from apps.income.models import IncomeEntry
from apps.installments.models import InstallmentPurchaseItem
from apps.loans.models import LoanInstallment
from apps.vehicles.models import VehicleExpense


@dataclass
class Obligation:
    source: str
    reference_id: str
    title: str
    amount: Decimal
    date_value: date
    mandatory: bool


class CashflowService:
    def _ensure_currency(self, user, expenses, incomes):
        base = user.profile.currency
        if expenses.exclude(currency=base).exists() or incomes.exclude(currency=base).exists():
            raise ValueError("Cashflow calculations require all entries to match the user base currency.")

    def build(self, user, start: date, end: date):
        profile = user.profile
        expenses = ExpenseEntry.objects.filter(user=user, incurred_on__lte=end, incurred_on__gte=start)
        incomes = IncomeEntry.objects.filter(user=user, expected_on__lte=end, expected_on__gte=start)
        self._ensure_currency(user, ExpenseEntry.objects.filter(user=user, incurred_on__range=(start, end)), IncomeEntry.objects.filter(user=user, expected_on__range=(start, end)))
        projected = RuleMaterializationService().materialize(user, start, end, persist=False)
        loan_items = LoanInstallment.objects.filter(user=user, due_on__range=(start, end))
        purchase_items = InstallmentPurchaseItem.objects.filter(user=user, due_on__range=(start, end))
        card_payments = CreditCardPayment.objects.filter(user=user, due_on__range=(start, end))
        vehicle_expenses = VehicleExpense.objects.filter(user=user, date__range=(start, end))

        daily = defaultdict(lambda: {"inflows": Decimal("0.00"), "outflows": Decimal("0.00"), "obligations": []})

        for income in incomes:
            if profile.income_projection_mode == "received_only" and income.status != "received":
                continue
            day = income.received_on or income.expected_on
            daily[day]["inflows"] += income.amount

        for payload in projected["incomes"]:
            if profile.income_projection_mode == "received_only":
                continue
            daily[payload["expected_on"]]["inflows"] += payload["amount"]

        mandatory_ids = {str(value) for value in profile.mandatory_category_ids}

        def is_mandatory_expense(expense: ExpenseEntry) -> bool:
            category_id = str(expense.category_id) if expense.category_id else None
            return expense.is_mandatory or (category_id in mandatory_ids if category_id else False)

        def add_obligation(source: str, reference_id: str, title: str, amount: Decimal, when: date, mandatory: bool):
            daily[when]["outflows"] += amount
            daily[when]["obligations"].append(Obligation(source, reference_id, title, amount, when, mandatory))

        for expense in expenses:
            when = expense.paid_on or expense.due_on or expense.incurred_on
            add_obligation("expense", str(expense.id), expense.title, expense.amount_total, when, is_mandatory_expense(expense))

        for payload in projected["expenses"]:
            category_id = str(payload["category"].id) if payload["category"] else None
            mandatory = payload["is_mandatory"] or (category_id in mandatory_ids if category_id else False)
            add_obligation("fixed_expense", str(payload["source_rule"].id), payload["title"], payload["amount_total"], payload["due_on"], mandatory)

        for installment in loan_items:
            add_obligation("loan_installment", str(installment.id), installment.loan.title, installment.amount_total, installment.due_on, True)
        for item in purchase_items:
            add_obligation("installment_purchase", str(item.id), item.installment_purchase.title, item.amount_total, item.due_on, True)
        for payment in card_payments:
            add_obligation("credit_card_payment", str(payment.id), payment.title, payment.amount_total, payment.due_on, True)
        for vehicle_expense in vehicle_expenses:
            add_obligation("vehicle_expense", str(vehicle_expense.id), vehicle_expense.title, vehicle_expense.amount_total, vehicle_expense.date, False)

        opening_balance = profile.opening_balance
        if profile.opening_balance_date and profile.opening_balance_date > start:
            opening_balance = Decimal("0.00")

        rows = []
        cursor = start
        current = opening_balance
        minimum_balance = current
        negative_windows = []
        active_negative = None
        funding_gap = Decimal("0.00")

        while cursor <= end:
            inflows = daily[cursor]["inflows"]
            outflows = daily[cursor]["outflows"]
            opening = current
            closing = opening + inflows - outflows
            minimum_balance = min(minimum_balance, closing)
            if closing < 0 and active_negative is None:
                active_negative = {"start": cursor, "worst_balance": closing}
            if closing < 0 and active_negative is not None:
                active_negative["worst_balance"] = min(active_negative["worst_balance"], closing)
                funding_gap = max(funding_gap, abs(closing))
            if closing >= 0 and active_negative is not None:
                active_negative["end"] = cursor - timedelta(days=1)
                negative_windows.append(active_negative)
                active_negative = None
            rows.append(
                {
                    "date": cursor,
                    "opening_balance": opening,
                    "inflows": inflows,
                    "outflows": outflows,
                    "closing_balance": closing,
                    "obligations": [
                        {
                            "source": item.source,
                            "reference_id": item.reference_id,
                            "title": item.title,
                            "amount": item.amount,
                            "mandatory": item.mandatory,
                        }
                        for item in daily[cursor]["obligations"]
                    ],
                }
            )
            current = closing
            cursor += timedelta(days=1)

        if active_negative is not None:
            active_negative["end"] = end
            negative_windows.append(active_negative)

        return {
            "currency": profile.currency,
            "opening_balance": opening_balance,
            "minimum_balance": minimum_balance,
            "funding_gap": funding_gap,
            "rows": rows,
            "negative_windows": negative_windows,
        }
