from django.contrib import admin
from django.contrib.auth.models import User


# Register your models here.

from . models import *
@admin.register(Order)           # admin.site.register(Order, allOrders)
class allOrders(admin.ModelAdmin):   
    list_display=['id','customer', 'user_name', 'complete', 'order_id', 'product_details', 'shipping_address']

@admin.register(Customer)
class customer(admin.ModelAdmin):
    list_display=['name', 'email', 'user', 'profile_pic', 'contact_no']
admin.site.register(Product)

@admin.register(Order_Item)
class Order_Item(admin.ModelAdmin):
    list_display=['product', 'order']

@admin.register(MyOrder)
class MyOrder(admin.ModelAdmin):
    list_display=['name', 'price', 'quantity', 'customer', 'order_id']
