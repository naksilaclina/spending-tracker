from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.views import UserOwnedModelViewSet
from apps.loans.models import Loan
from apps.loans.serializers import LoanInstallmentSerializer, LoanSerializer
from apps.loans.services import LoanScheduleService


class LoanViewSet(UserOwnedModelViewSet):
    queryset = Loan.objects.prefetch_related("installments")
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        loan = serializer.save(user=self.request.user)
        LoanScheduleService().regenerate(loan)

    @action(detail=True, methods=["get"], url_path="schedule")
    def schedule(self, request, pk=None):
        loan = self.get_object()
        return Response({
            "loan": LoanSerializer(loan, context=self.get_serializer_context()).data,
            "schedule": LoanInstallmentSerializer(loan.installments.all(), many=True).data,
        })

    @action(detail=True, methods=["post"], url_path="regenerate-schedule")
    def regenerate_schedule(self, request, pk=None):
        loan = self.get_object()
        schedule = LoanScheduleService().regenerate(loan)
        return Response(LoanInstallmentSerializer(schedule, many=True).data)
