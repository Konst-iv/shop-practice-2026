from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status'] 
    inlines = [OrderItemInline] 