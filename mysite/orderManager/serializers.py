from rest_framework import serializers
from .models import Order, Category, Item, OrderInfo


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'url', 'name', 'price')


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    def update(self, instance, validated_data):
        uneditable_fields = ['id', 'url', 'name', 'price']
        for field in uneditable_fields:
            if field in validated_data:
                raise serializers.ValidationError("Uneditable fields! {}"
                                                  .format(uneditable_fields))
        return super().update(instance, validated_data)

    class Meta:
        model = Item
        fields = ('id', 'url', 'name', 'category', 'price', 'in_stock')


class OrderInfoSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField()
    name = serializers.ReadOnlyField(source='item.name')
    price = serializers.ReadOnlyField(source='item.price')

    class Meta:
        model = OrderInfo
        fields = ('item_id', 'name', 'price', 'quantity')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = OrderInfoSerializer(source='item_info', many=True)

    def create(self, validated_data):
        items_data = validated_data.pop('item_info')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            data = dict(item)
            OrderInfo.objects.create(order=order,
                                     item=Item.objects.get(pk=data['item_id']),
                                     quantity=data['quantity'])
        return order

    def update(self, instance, validated_data):
        uneditable_fields = ['id', '__str__', 'customer', 'url', 'notes', 'items']
        for field in uneditable_fields:
            if field in validated_data:
                raise serializers.ValidationError("Uneditable fields! {}"
                                                  .format(uneditable_fields))
        return super().update(instance, validated_data)

    def validate(self, attrs):
        data = dict(attrs)

        if self.instance:
            return data
        if not data['item_info']:
            raise serializers.ValidationError('Empty orders are not allowed.')

        for item in data['item_info']:
            if not Item.objects.filter(id=item['item_id']).exists():
                raise serializers.ValidationError('Item doesn\'t exist.')
        return data

    class Meta:
        model = Order
        fields = ('id', '__str__', 'url', 'customer', 'isCompleted', 'isPaid', 'notes', 'items')
