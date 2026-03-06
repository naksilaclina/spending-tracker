from apps.core.views import UserOwnedModelViewSet
from apps.credit_cards.models import CreditCardAccount, CreditCardPayment
from apps.credit_cards.serializers import CreditCardAccountSerializer, CreditCardPaymentSerializer


class CreditCardAccountViewSet(UserOwnedModelViewSet):
    queryset = CreditCardAccount.objects.all()
    serializer_class = CreditCardAccountSerializer


class CreditCardPaymentViewSet(UserOwnedModelViewSet):
    queryset = CreditCardPayment.objects.select_related("credit_card")
    serializer_class = CreditCardPaymentSerializer
