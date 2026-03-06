from rest_framework import serializers

from apps.users.models import UserProfile


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "display_name",
            "timezone",
            "currency",
            "onboarding_state",
            "opening_balance",
            "opening_balance_date",
            "income_projection_mode",
            "mandatory_category_ids",
            "preferences",
        ]
