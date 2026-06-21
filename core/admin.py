from django.contrib import admin
from .models import Asset, RequestTicket


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_type', 'status', 'assigned_to')
    list_filter = ('asset_type', 'status')
    search_fields = ('name',)


@admin.register(RequestTicket)
class RequestTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'asset_type', 'status', 'created_at')
    list_filter = ('status', 'asset_type')
    search_fields = ('user__username',)
