from rest_framework import serializers

from apps.finance.models import Category, RecurrenceRule, Template


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "kind", "name", "parent", "icon", "color", "is_system", "ordering"]
        read_only_fields = ["id", "is_system"]


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        exclude = ["user", "created_at", "updated_at"]
        read_only_fields = ["id"]


class RecurrenceRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurrenceRule
        exclude = ["user", "created_at", "updated_at"]
