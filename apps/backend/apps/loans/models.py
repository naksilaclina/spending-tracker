from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.core.enums import InstallmentStatus, LoanStatus
from apps.core.models import OwnedModel, money_validator


class Loan(OwnedModel):
    title = models.CharField(max_length=255)
    lender = models.CharField(max_length=255, blank=True)
    principal_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    repayment_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    interest_total = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    fee_total = models.DecimalField(max_digits=14, decimal_places=2, default="0.00", validators=[money_validator])
    installment_count = models.PositiveIntegerField()
    monthly_payment = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    payment_day = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    first_installment_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=24, choices=LoanStatus.choices, default=LoanStatus.ACTIVE)
    note = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    class Meta:
        ordering = ["-start_date"]
        indexes = [models.Index(fields=["user", "status", "start_date"])]


class LoanInstallment(OwnedModel):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="installments")
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
        constraints = [models.UniqueConstraint(fields=["loan", "installment_number"], name="uniq_loan_installment_number")]
        indexes = [models.Index(fields=["user", "due_on", "status"])]
