from rest_framework import serializers

from apps.installments.models import InstallmentPurchase, InstallmentPurchaseItem


class InstallmentPurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentPurchaseItem
        exclude = ["user", "created_at", "updated_at"]


class InstallmentPurchaseSerializer(serializers.ModelSerializer):
    items = InstallmentPurchaseItemSerializer(many=True, read_only=True)

    class Meta:
        model = InstallmentPurchase
        exclude = ["user", "created_at", "updated_at"]
        read_only_fields = ["id"]
