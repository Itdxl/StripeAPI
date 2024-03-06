from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Item(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits = 10, decimal_places=2)

    class Meta:
        verbose_name = ('Предмет')  
        verbose_name_plural = ('Предметы')

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ('Заказ')
        verbose_name_plural = ('Заказы')


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='order_items', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.name} в количестве {self.quantity} штук. "


