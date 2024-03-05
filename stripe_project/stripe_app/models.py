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


# class Order(models.Model):
#     user = models.ForeignKey(User,
#         ON_DELETE=models.Cascade)


# class Discount(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(max_length=250, blank=True)
#     amount = models.IntegerField()
