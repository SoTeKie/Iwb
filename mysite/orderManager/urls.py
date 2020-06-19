from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('orders', views.OrderView, basename='order')
router.register('categories', views.CategoryView)
router.register('items', views.ItemView, basename='item')

urlpatterns = [
    path('', include(router.urls)),
    path('auth-token/', views.CustomAuthToken.as_view())
]
