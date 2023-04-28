from django.contrib import admin

from core.models import Product, CartProduct, Cart


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']



admin.site.register(Product, ProductAdmin)