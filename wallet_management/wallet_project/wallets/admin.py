from django.contrib import admin
from .models import Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'account_scheme', 'owner', 'created_at']
    list_filter = ['type', 'account_scheme', 'created_at']
    search_fields = ['name', 'owner', 'account_number']
    readonly_fields = ['created_at']
