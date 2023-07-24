from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Customer, Product, Price


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'name', 'id')
    search_fields = ('id', 'user', 'name', 'email')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'description', 'active')
    list_filter = ('active', )
    search_fields = ('id', 'name', 'description')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', 'unit_amount', 'currency', 'active')
    list_filter = ('currency', 'active')
    search_fields = ('id', 'product', 'unit_amount', 'currency')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price, PriceAdmin)