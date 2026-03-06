from rest_framework import serializers


class StringDecimalField(serializers.DecimalField):
    def to_representation(self, value):
        value = super().to_representation(value)
        return str(value)
