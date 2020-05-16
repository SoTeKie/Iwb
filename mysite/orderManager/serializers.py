from rest_framework import serializers
from .models import Order, Category, Item, OrderInfo


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'url','name', 'price')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'url', 'name', 'category', 'price')

class OrderInfoSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source="item.id")
    name = serializers.ReadOnlyField(source="item.name")
    price = serializers.ReadOnlyField(source="item.price")

    class Meta:
        model = OrderInfo
        fields = ('id','name','price','quantity')

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = OrderInfoSerializer(source = "item_info", many=True)

    class Meta:
        model = Order
        fields = ('id', 'url', 'items')
