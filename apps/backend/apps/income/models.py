from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.core.enums import IncomeStatus
from apps.core.models import MoneyMixin, OwnedModel, money_validator


class IncomeEntry(OwnedModel, MoneyMixin):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    income_type = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=16, choices=IncomeStatus.choices, default=IncomeStatus.EXPECTED)
    expected_on = models.DateField()
    received_on = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=120, blank=True)
    note = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    source_rule = models.ForeignKey("fixed_rules.FixedIncomeRule", null=True, blank=True, on_delete=models.SET_NULL, related_name="generated_entries")
    is_guaranteed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-expected_on", "-created_at"]
        indexes = [
            models.Index(fields=["user", "expected_on"]),
            models.Index(fields=["user", "status", "received_on"]),
        ]
