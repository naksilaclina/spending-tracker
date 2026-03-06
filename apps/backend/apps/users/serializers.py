from rest_framework import serializers

from apps.core.serializers import StringDecimalField
from apps.users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    opening_balance = StringDecimalField(max_digits=14, decimal_places=2)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "supabase_user_id",
            "email",
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
