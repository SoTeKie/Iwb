from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('orders', views.OrderView)
router.register('categories', views.CategoryView)
router.register('items', views.ItemView)

urlpatterns = [
    path('', include(router.urls)),
]