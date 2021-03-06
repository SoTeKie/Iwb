from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Category(models.Model):
    name = models.CharField(max_length=15)
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Item(models.Model):
    category = models.ForeignKey('Category',
                                 on_delete=models.PROTECT,
                                 related_name='items')

    name = models.CharField(max_length=30)
    individual_price = models.PositiveSmallIntegerField(default=0)
    in_stock = models.BooleanField(default=True)

    @property
    def price(self):
        return (self.category.price if self.individual_price == 0
                else self.individual_price)

    def __str__(self):
        return self.name


class OrderInfo(models.Model):
    item = models.ForeignKey('Item',
                             on_delete=models.CASCADE,
                             related_name='order_info')
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              related_name='item_info')

    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return 'Order #{} - item: {}'.format(self.order.pk, self.item.name)


class Order(models.Model):
    items = models.ManyToManyField('Item',
                                   through='OrderInfo',
                                   related_name='orders')

    customer = models.CharField(max_length=30)
    created_time = models.DateTimeField(auto_now_add=True)
    isPaid = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)
    notes = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return '#{}'.format(self.pk)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
