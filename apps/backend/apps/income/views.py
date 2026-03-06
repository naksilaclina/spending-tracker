from apps.core.views import UserOwnedModelViewSet
from apps.income.models import IncomeEntry
from apps.income.serializers import IncomeEntrySerializer


class IncomeEntryViewSet(UserOwnedModelViewSet):
    queryset = IncomeEntry.objects.all()
    serializer_class = IncomeEntrySerializer
