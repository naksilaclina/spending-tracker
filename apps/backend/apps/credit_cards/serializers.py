from rest_framework import serializers

from apps.credit_cards.models import CreditCardAccount, CreditCardPayment


class CreditCardAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardAccount
        exclude = ["user", "created_at", "updated_at"]


class CreditCardPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardPayment
        exclude = ["user", "created_at", "updated_at"]

    def validate(self, attrs):
        card = attrs.get("credit_card") or getattr(self.instance, "credit_card", None)
        request = self.context.get("request")
        if card and request and card.user_id != request.user.id:
            raise serializers.ValidationError({"credit_card": "Credit card does not belong to the authenticated user."})
        return attrs
