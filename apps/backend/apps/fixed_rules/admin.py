from django.contrib import admin

from apps.fixed_rules.models import FixedExpenseRule, FixedIncomeRule

admin.site.register(FixedExpenseRule)
admin.site.register(FixedIncomeRule)
