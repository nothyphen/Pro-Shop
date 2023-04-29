from django.contrib import admin
from .models import Category, Customer, ShippingAddress, Order, OrderItem, Product, Banner
# Register your models here.

class CategotyList(admin.ModelAdmin):
    list_display = ['id', 'name']

class CustomerList(admin.ModelAdmin):
    list_display = ['id', 'name']

class ProductList(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']

class OrderList(admin.ModelAdmin):
    list_display = ['id', 'customer', 'transation_id']

class OrderItemList(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity']

class ShippingAddressList(admin.ModelAdmin):
    list_display = ['id', 'customer', 'state', 'city']

admin.site.register(Category, CategotyList)
admin.site.register(Product, ProductList)
admin.site.register(Customer, CustomerList)
admin.site.register(Order, OrderList)
admin.site.register(OrderItem, OrderItemList)
admin.site.register(ShippingAddress, ShippingAddressList)
admin.site.register(Banner)