from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.views import UserOwnedModelViewSet
from apps.installments.models import InstallmentPurchase
from apps.installments.serializers import InstallmentPurchaseItemSerializer, InstallmentPurchaseSerializer
from apps.installments.services import InstallmentScheduleService


class InstallmentPurchaseViewSet(UserOwnedModelViewSet):
    queryset = InstallmentPurchase.objects.prefetch_related("items")
    serializer_class = InstallmentPurchaseSerializer

    def perform_create(self, serializer):
        purchase = serializer.save(user=self.request.user)
        InstallmentScheduleService().regenerate(purchase)

    @action(detail=True, methods=["get"], url_path="schedule")
    def schedule(self, request, pk=None):
        purchase = self.get_object()
        return Response({
            "purchase": InstallmentPurchaseSerializer(purchase, context=self.get_serializer_context()).data,
            "schedule": InstallmentPurchaseItemSerializer(purchase.items.all(), many=True).data,
        })
