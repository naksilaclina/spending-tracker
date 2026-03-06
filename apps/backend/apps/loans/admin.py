from django.contrib import admin

from apps.loans.models import Loan, LoanInstallment

admin.site.register(Loan)
admin.site.register(LoanInstallment)
