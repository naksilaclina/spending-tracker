from datetime import date

from apps.core.utils import clamp_day, month_sequence
from apps.expenses.models import ExpenseEntry
from apps.fixed_rules.models import FixedExpenseRule, FixedIncomeRule
from apps.income.models import IncomeEntry


class RuleMaterializationService:
    def materialize(self, user, start: date, end: date, persist: bool = False):
        expenses = []
        incomes = []
        months = month_sequence(start, end)

        expense_rules = FixedExpenseRule.objects.filter(user=user, is_active=True, auto_generate=True)
        income_rules = FixedIncomeRule.objects.filter(user=user, is_active=True, auto_generate=True)

        for month_start in months:
            for rule in expense_rules:
                if rule.starts_on > end or (rule.ends_on and rule.ends_on < start):
                    continue
                due_on = date(month_start.year, month_start.month, clamp_day(month_start.year, month_start.month, rule.due_day))
                if due_on < rule.starts_on or (rule.ends_on and due_on > rule.ends_on) or due_on < start or due_on > end:
                    continue
                payload = {
                    "user": user,
                    "title": rule.title,
                    "amount_total": rule.default_amount,
                    "principal_amount": rule.default_amount,
                    "interest_amount": 0,
                    "fee_amount": 0,
                    "currency": user.profile.currency,
                    "category": rule.category,
                    "payment_method": rule.payment_method,
                    "status": "planned",
                    "entry_type": "fixed",
                    "incurred_on": due_on,
                    "due_on": due_on,
                    "note": rule.note,
                    "tags": rule.tags,
                    "source_rule": rule,
                    "is_mandatory": rule.is_mandatory,
                }
                if persist:
                    instance, _ = ExpenseEntry.objects.get_or_create(user=user, source_rule=rule, due_on=due_on, defaults=payload)
                    expenses.append(instance)
                else:
                    expenses.append(payload)

            for rule in income_rules:
                if rule.starts_on > end or (rule.ends_on and rule.ends_on < start):
                    continue
                expected_on = date(month_start.year, month_start.month, clamp_day(month_start.year, month_start.month, rule.expected_day))
                if expected_on < rule.starts_on or (rule.ends_on and expected_on > rule.ends_on) or expected_on < start or expected_on > end:
                    continue
                payload = {
                    "user": user,
                    "title": rule.title,
                    "amount": rule.default_amount,
                    "currency": user.profile.currency,
                    "income_type": rule.income_type,
                    "status": "expected",
                    "expected_on": expected_on,
                    "source": rule.source,
                    "note": rule.note,
                    "tags": rule.tags,
                    "source_rule": rule,
                    "is_guaranteed": rule.is_guaranteed,
                }
                if persist:
                    instance, _ = IncomeEntry.objects.get_or_create(user=user, source_rule=rule, expected_on=expected_on, defaults=payload)
                    incomes.append(instance)
                else:
                    incomes.append(payload)

        return {"expenses": expenses, "incomes": incomes}
