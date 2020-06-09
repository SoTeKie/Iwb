from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
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


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_groups': user.groups.values_list('name', flat=True)
        })
