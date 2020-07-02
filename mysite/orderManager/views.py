from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Order, Category, Item
from .serializers import (OrderSerializer,
                          CategorySerializer,
                          ItemSerializer,)
from .permissions import OrderPermissions, ItemPermissions
from django.utils import timezone
from datetime import timedelta

class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (OrderPermissions,)

    def get_queryset(self):
        time_threshold = timezone.now() - timedelta(hours=24)
        return Order.objects.filter(created_time__gte=time_threshold)

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (ItemPermissions,)


class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (ItemPermissions,)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_group': user.groups.all()[0].name
        })
