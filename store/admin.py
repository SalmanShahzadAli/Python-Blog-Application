from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'price', 'stock', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'owner__email')


admin.site.register(Product, ProductAdmin)