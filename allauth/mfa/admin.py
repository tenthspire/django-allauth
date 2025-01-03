from django.contrib import admin

from allauth.mfa.models import Authenticator

# from .models import CustomUser
# # Register your models here.
# admin.site.register(CustomUser)
@admin.register(Authenticator)
class AuthenticatorAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_display = ("user", "type", "created_at", "last_used_at")
    list_filter = ("type", "created_at", "last_used_at")
