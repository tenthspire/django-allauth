from django.contrib import admin

# Register your models here.
from .models import DomainPuchase,UpdatedDomainDetail

@admin.register(DomainPuchase)
class DomainPurchaseAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'purchse_date', 'status')

@admin.register(UpdatedDomainDetail)
class DomainUpdateAdmin(admin.ModelAdmin):
    list_display = ('domain_name',  'updated_at')