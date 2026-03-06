from apps.core.views import UserOwnedModelViewSet
from apps.fixed_rules.models import FixedExpenseRule, FixedIncomeRule
from apps.fixed_rules.serializers import FixedExpenseRuleSerializer, FixedIncomeRuleSerializer


class FixedExpenseRuleViewSet(UserOwnedModelViewSet):
    queryset = FixedExpenseRule.objects.select_related("category")
    serializer_class = FixedExpenseRuleSerializer


class FixedIncomeRuleViewSet(UserOwnedModelViewSet):
    queryset = FixedIncomeRule.objects.all()
    serializer_class = FixedIncomeRuleSerializer
