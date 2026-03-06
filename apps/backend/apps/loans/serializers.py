from rest_framework import serializers

from apps.loans.models import Loan, LoanInstallment


class LoanInstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanInstallment
        exclude = ["user", "created_at", "updated_at"]


class LoanSerializer(serializers.ModelSerializer):
    installments = LoanInstallmentSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        exclude = ["user", "created_at", "updated_at"]
        read_only_fields = ["id", "end_date"]
