from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

    autocomplete_fields = ('book', 'cart')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name')

    readonly_fields = ('created_at', 'updated_at')

    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

    readonly_fields = ('price', 'discount', 'final_price')
    autocomplete_fields = ('book', 'order')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'status', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name')

    readonly_fields = ('created_at', 'updated_at', 'total_price')

    inlines = [OrderItemInline]

admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)