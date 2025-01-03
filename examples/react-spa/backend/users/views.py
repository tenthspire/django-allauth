from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializers

class ProductCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

class ProductDetail(generics.RetrieveUpdateDestroyAPIView): # for update and delete the specific product 
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    