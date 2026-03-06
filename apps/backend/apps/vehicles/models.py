from django.db import models

from apps.core.enums import VehicleExpenseType
from apps.core.models import OwnedModel, money_validator


class Vehicle(OwnedModel):
    name = models.CharField(max_length=120)
    make = models.CharField(max_length=120, blank=True)
    model = models.CharField(max_length=120, blank=True)
    plate = models.CharField(max_length=32, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["user", "is_active"])]


class VehicleExpense(OwnedModel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle_expenses")
    title = models.CharField(max_length=255)
    expense_type = models.CharField(max_length=24, choices=VehicleExpenseType.choices)
    amount_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[money_validator])
    date = models.DateField()
    odometer = models.PositiveIntegerField(null=True, blank=True)
    liters = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[money_validator])
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=["user", "date", "expense_type"])]
