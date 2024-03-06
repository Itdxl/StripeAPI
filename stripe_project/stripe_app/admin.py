from django.contrib import admin

from .models import Item, Order, OrderItem, Discount, Tax


admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Discount)
admin.site.register(Tax)