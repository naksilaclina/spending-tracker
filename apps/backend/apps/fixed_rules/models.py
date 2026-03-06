from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.core.models import OwnedModel, money_validator


class FixedExpenseRule(OwnedModel):
    title = models.CharField(max_length=255)
    default_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    category = models.ForeignKey("finance.Category", null=True, blank=True, on_delete=models.SET_NULL, related_name="fixed_expense_rules")
    payment_method = models.CharField(max_length=64, blank=True)
    due_day = models.CharField(max_length=8)
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    auto_generate = models.BooleanField(default=True)
    note = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    is_active = models.BooleanField(default=True)
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["user", "is_active", "starts_on"])]


class FixedIncomeRule(OwnedModel):
    title = models.CharField(max_length=255)
    default_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    income_type = models.CharField(max_length=64, blank=True)
    source = models.CharField(max_length=120, blank=True)
    expected_day = models.CharField(max_length=8)
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    auto_generate = models.BooleanField(default=True)
    note = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    is_active = models.BooleanField(default=True)
    is_guaranteed = models.BooleanField(default=False)

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["user", "is_active", "starts_on"])]
