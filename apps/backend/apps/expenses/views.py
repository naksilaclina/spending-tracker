from apps.core.views import UserOwnedModelViewSet
from apps.expenses.models import ExpenseEntry
from apps.expenses.serializers import ExpenseEntrySerializer


class ExpenseEntryViewSet(UserOwnedModelViewSet):
    queryset = ExpenseEntry.objects.select_related("category", "loan", "installment_purchase", "credit_card", "vehicle")
    serializer_class = ExpenseEntrySerializer
