from django.contrib import admin
from .models import InventoryItem

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredient', 'quantity', 'unit')
    list_filter = ('user',)
    search_fields = ('ingredient__name',)
