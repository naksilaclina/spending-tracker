from rest_framework import serializers

from apps.expenses.models import ExpenseEntry


class ExpenseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseEntry
        exclude = ["user", "created_at", "updated_at"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        category = attrs.get("category") or getattr(self.instance, "category", None)
        request = self.context.get("request")
        if category and request and category.user_id != request.user.id:
            raise serializers.ValidationError({"category": "Category does not belong to the authenticated user."})
        return attrs
