from django.db import models

from apps.core.enums import CreditCardPaymentStatus
from apps.core.models import OwnedModel, money_validator


class CreditCardAccount(OwnedModel):
    name = models.CharField(max_length=120)
    issuer = models.CharField(max_length=120, blank=True)
    last4 = models.CharField(max_length=4, blank=True)
    statement_due_day = models.PositiveSmallIntegerField()
    statement_close_day = models.PositiveSmallIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["user", "is_active"])]


class CreditCardPayment(OwnedModel):
    credit_card = models.ForeignKey(CreditCardAccount, on_delete=models.CASCADE, related_name="payments")
    title = models.CharField(max_length=255)
    amount_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    principal_amount = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    interest_amount = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    fee_amount = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    due_on = models.DateField()
    paid_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=CreditCardPaymentStatus.choices, default=CreditCardPaymentStatus.PLANNED)
    minimum_payment = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, validators=[money_validator])
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-due_on"]
        indexes = [models.Index(fields=["user", "status", "due_on"])]
