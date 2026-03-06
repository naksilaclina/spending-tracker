from datetime import date

from rest_framework import serializers

from apps.fixed_rules.models import FixedExpenseRule, FixedIncomeRule


class FixedExpenseRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedExpenseRule
        exclude = ["user", "created_at", "updated_at"]
        read_only_fields = ["id"]


class FixedIncomeRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedIncomeRule
        exclude = ["user", "created_at", "updated_at"]
        read_only_fields = ["id"]
