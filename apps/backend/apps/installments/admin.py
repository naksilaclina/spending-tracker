from django.contrib import admin

from apps.installments.models import InstallmentPurchase, InstallmentPurchaseItem

admin.site.register(InstallmentPurchase)
admin.site.register(InstallmentPurchaseItem)
