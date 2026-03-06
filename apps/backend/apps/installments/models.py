from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.core.enums import InstallmentStatus
from apps.core.models import OwnedModel, money_validator


class InstallmentPurchase(OwnedModel):
    title = models.CharField(max_length=255)
    merchant = models.CharField(max_length=255, blank=True)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    cash_price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, validators=[money_validator])
    repayment_total = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, validators=[money_validator])
    principal_total = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, validators=[money_validator])
    interest_total = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, validators=[money_validator])
    fee_total = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, validators=[money_validator])
    installment_count = models.PositiveIntegerField()
    first_installment_date = models.DateField()
    linked_credit_card = models.ForeignKey("credit_cards.CreditCardAccount", null=True, blank=True, on_delete=models.SET_NULL, related_name="installment_purchases")
    category = models.ForeignKey("finance.Category", null=True, blank=True, on_delete=models.SET_NULL, related_name="installment_purchases")
    status = models.CharField(max_length=24, choices=InstallmentStatus.choices, default=InstallmentStatus.SCHEDULED)
    note = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    class Meta:
        ordering = ["-first_installment_date"]
        indexes = [models.Index(fields=["user", "status", "first_installment_date"])]


class InstallmentPurchaseItem(OwnedModel):
    installment_purchase = models.ForeignKey(InstallmentPurchase, on_delete=models.CASCADE, related_name="items")
    installment_number = models.PositiveIntegerField()
    due_on = models.DateField()
    amount_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    principal_amount = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    interest_amount = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    fee_amount = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    status = models.CharField(max_length=16, choices=InstallmentStatus.choices, default=InstallmentStatus.SCHEDULED)
    paid_on = models.DateField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)

    class Meta:
        ordering = ["installment_number"]
        constraints = [models.UniqueConstraint(fields=["installment_purchase", "installment_number"], name="uniq_purchase_installment_number")]
        indexes = [models.Index(fields=["user", "due_on", "status"])]
