from rest_framework import viewsets
from .models import Order, Category, Item
from .serializers import (OrderSerializer,
                          CategorySerializer,
                          ItemSerializer,)
from .permissions import OrderPermissions, ItemPermissions


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (OrderPermissions,)


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (ItemPermissions,)


class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = (ItemPermissions,)

    def get_queryset(self):
        return Item.objects.filter(in_stock=True)
