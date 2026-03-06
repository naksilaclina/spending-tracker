from apps.core.views import UserOwnedModelViewSet
from apps.vehicles.models import Vehicle, VehicleExpense
from apps.vehicles.serializers import VehicleExpenseSerializer, VehicleSerializer


class VehicleViewSet(UserOwnedModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleExpenseViewSet(UserOwnedModelViewSet):
    queryset = VehicleExpense.objects.select_related("vehicle")
    serializer_class = VehicleExpenseSerializer
