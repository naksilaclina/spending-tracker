from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.core.enums import CategoryKind, RecurrenceAppliesTo, RecurrenceFrequency, TemplateType
from apps.core.models import MoneyMixin, OwnedModel, TimeStampedModel, money_validator


class Category(OwnedModel):
    kind = models.CharField(max_length=16, choices=CategoryKind.choices)
    name = models.CharField(max_length=120)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    icon = models.CharField(max_length=64, blank=True)
    color = models.CharField(max_length=32, blank=True)
    is_system = models.BooleanField(default=False)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordering", "name"]
        constraints = [
            models.UniqueConstraint(fields=["user", "kind", "name", "parent"], name="uniq_category_per_user"),
        ]
        indexes = [models.Index(fields=["user", "kind", "ordering"])]


class Template(OwnedModel, MoneyMixin):
    kind = models.CharField(max_length=16, choices=CategoryKind.choices)
    title = models.CharField(max_length=255)
    default_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, validators=[money_validator])
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="templates")
    subcategory = models.CharField(max_length=120, blank=True)
    payment_method = models.CharField(max_length=64, blank=True)
    income_type = models.CharField(max_length=64, blank=True)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    color = models.CharField(max_length=32, blank=True)
    icon = models.CharField(max_length=64, blank=True)
    template_type = models.CharField(max_length=32, choices=TemplateType.choices, default=TemplateType.NORMAL)

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["user", "kind", "template_type"])]


class RecurrenceRule(OwnedModel):
    applies_to = models.CharField(max_length=16, choices=RecurrenceAppliesTo.choices)
    frequency = models.CharField(max_length=16, choices=RecurrenceFrequency.choices)
    interval = models.PositiveIntegerField(default=1)
    by_month_day = models.PositiveSmallIntegerField(null=True, blank=True)
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    is_paused = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["starts_on"]
