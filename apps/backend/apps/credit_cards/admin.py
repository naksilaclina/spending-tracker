from django.contrib import admin

from apps.credit_cards.models import CreditCardAccount, CreditCardPayment

admin.site.register(CreditCardAccount)
admin.site.register(CreditCardPayment)
