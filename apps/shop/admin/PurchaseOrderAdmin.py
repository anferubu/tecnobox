from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import PurchaseOrder




@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(BaseModelAdmin):
    """
    Modelo PurchaseOrder de la interfaz de administración.
    """
    list_display = ['user', 'shopping_cart', 'subtotal', 'taxes', 'total', 'payment_method', 'shipping_address', 'status', 'created_at', 'updated_at', 'is_active']
    list_filter = ['status', 'is_active']
    search_fields = ['user', 'shopping_cart', 'payment_method', 'status', 'is_active']
    ordering = ['user', 'shopping_cart', 'payment_method', 'status']
    actions = [disable_selected, enable_selected]