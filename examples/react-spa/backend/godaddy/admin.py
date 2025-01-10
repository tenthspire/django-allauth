from django.contrib import admin

# Register your models here.
from .models import DomainPuchase

@admin.register(DomainPuchase)
class DomainPurchaseAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'purchse_date', 'status')
