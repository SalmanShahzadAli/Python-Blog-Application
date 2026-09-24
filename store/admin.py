from django.contrib import admin
from .models import Product
from django.contrib import admin
from .models import Product, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'price', 'stock', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'owner__email')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'full_name', 'email', 'phone')
    inlines = [OrderItemInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)