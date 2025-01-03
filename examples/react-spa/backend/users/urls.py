from django.urls import path
from .views import ProductCreate, ProductDetail

urlpatterns = [
    path('products/', ProductCreate.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
]
    