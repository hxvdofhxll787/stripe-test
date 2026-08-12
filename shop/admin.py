from django.contrib import admin
from .models import Item, Order, OrderItem, Discount


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price')
    search_fields = ('name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_price', 'discount', 'total_price_with_discount', 'discount_amount')
    search_fields = ('name',)
    inlines = [OrderItemInline]

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'percent')
    search_fields = ('name',)