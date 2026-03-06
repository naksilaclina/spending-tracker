from rest_framework import serializers

from apps.vehicles.models import Vehicle, VehicleExpense


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        exclude = ["user", "created_at", "updated_at"]


class VehicleExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleExpense
        exclude = ["user", "created_at", "updated_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        vehicle = attrs.get("vehicle") or getattr(self.instance, "vehicle", None)
        if vehicle and request and vehicle.user_id != request.user.id:
            raise serializers.ValidationError({"vehicle": "Vehicle does not belong to the authenticated user."})
        return attrs
