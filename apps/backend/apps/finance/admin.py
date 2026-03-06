from django.contrib import admin

from apps.finance.models import Category, RecurrenceRule, Template

admin.site.register(Category)
admin.site.register(Template)
admin.site.register(RecurrenceRule)
