from django.contrib import admin

from apps.vehicles.models import Vehicle, VehicleExpense

admin.site.register(Vehicle)
admin.site.register(VehicleExpense)
