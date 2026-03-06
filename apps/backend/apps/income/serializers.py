from rest_framework import serializers

from apps.income.models import IncomeEntry


class IncomeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeEntry
        exclude = ["user", "created_at", "updated_at"]
        read_only_fields = ["id"]
