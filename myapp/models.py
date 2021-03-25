from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    money = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.username


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование', blank=False, null=False)
    description = models.CharField(max_length=1000, verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity_in_stock = models.PositiveIntegerField(verbose_name='Наличие на складе')
    available = models.BooleanField(default=True, verbose_name='Имеется в наличии')

    def __str__(self):
        return self.title


class Purchase(models.Model):
    user = models.ForeignKey(MyUser, verbose_name='Покупатель', on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    time_of_buy = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product}"


class Return(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.DO_NOTHING)
    return_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name="returns")

