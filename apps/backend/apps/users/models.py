from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.core.enums import IncomeProjectionMode, OnboardingState
from apps.core.models import TimeStampedModel, money_validator

User = get_user_model()


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    supabase_user_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    display_name = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
    currency = models.CharField(max_length=3, default="USD")
    onboarding_state = models.CharField(
        max_length=32,
        choices=OnboardingState.choices,
        default=OnboardingState.NEW,
    )
    opening_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default="0.00",
        validators=[money_validator],
    )
    opening_balance_date = models.DateField(null=True, blank=True)
    income_projection_mode = models.CharField(
        max_length=32,
        choices=IncomeProjectionMode.choices,
        default=IncomeProjectionMode.EXPECTED,
    )
    mandatory_category_ids = ArrayField(models.UUIDField(), default=list, blank=True)
    preferences = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["created_at"]
