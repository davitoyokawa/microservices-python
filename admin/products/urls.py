from django.contrib import admin
from django.urls import path
from . import views

from .views import ProductViewSet, UserAPIView

urlpatterns = [
    path('products/', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('products/<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    path('user/', UserAPIView.as_view()),
    path('products/<int:id>/ratings', views.get_product_ratings, name='get_product_ratings'),
]
