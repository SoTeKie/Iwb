from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=30)
    individual_price = models.PositiveSmallIntegerField(default=0)

    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name="items")

    @property
    def price():
        return self.category.price if self.individual_price == 0 else self.individual_price

class Order(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, through="OrderInfo", related_name='orders')
    isPayed = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)

    def __str__():
        return "Order #{}".format(self.pk)

class OrderInfo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name="order_info")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="item_info")

    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__():
        return "Order #{} - item: {}".format(self.order.pk, self.item.name)


class Category(models.Model):
    name = models.CharField(max_length=15)
    price = models.PositiveSmallIntegerField

    def __str__():
        return self.name


