from django.contrib import admin
from .models import Location, TextComment, Money,OrderBill
from .forms import LocationForm

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    form = LocationForm

admin.site.register(Location, LocationAdmin)
admin.site.register(TextComment)
admin.site.register(Money)
admin.site.register(OrderBill)
