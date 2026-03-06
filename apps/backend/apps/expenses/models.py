from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F, Q

from apps.core.enums import ExpenseEntryType, ExpenseStatus
from apps.core.models import MoneyMixin, OwnedModel, money_validator


class ExpenseEntry(OwnedModel, MoneyMixin):
    title = models.CharField(max_length=255)
    amount_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    principal_amount = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    interest_amount = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    fee_amount = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    category = models.ForeignKey("finance.Category", null=True, blank=True, on_delete=models.SET_NULL, related_name="expense_entries")
    subcategory = models.CharField(max_length=120, blank=True)
    payment_method = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=16, choices=ExpenseStatus.choices, default=ExpenseStatus.PLANNED)
    entry_type = models.CharField(max_length=32, choices=ExpenseEntryType.choices, default=ExpenseEntryType.ONE_TIME)
    incurred_on = models.DateField()
    due_on = models.DateField(null=True, blank=True)
    paid_on = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    source_rule = models.ForeignKey("fixed_rules.FixedExpenseRule", null=True, blank=True, on_delete=models.SET_NULL, related_name="generated_entries")
    loan = models.ForeignKey("loans.Loan", null=True, blank=True, on_delete=models.SET_NULL, related_name="expense_entries")
    installment_purchase = models.ForeignKey("installments.InstallmentPurchase", null=True, blank=True, on_delete=models.SET_NULL, related_name="expense_entries")
    credit_card = models.ForeignKey("credit_cards.CreditCardAccount", null=True, blank=True, on_delete=models.SET_NULL, related_name="expense_entries")
    vehicle = models.ForeignKey("vehicles.Vehicle", null=True, blank=True, on_delete=models.SET_NULL, related_name="expense_entries")
    is_mandatory = models.BooleanField(default=False)

    class Meta:
        ordering = ["-incurred_on", "-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(amount_total=F("principal_amount") + F("interest_amount") + F("fee_amount")) | Q(principal_amount=0, interest_amount=0, fee_amount=0),
                name="expense_split_matches_total_or_zero",
            )
        ]
        indexes = [
            models.Index(fields=["user", "incurred_on"]),
            models.Index(fields=["user", "status", "due_on"]),
            models.Index(fields=["user", "entry_type"]),
        ]
