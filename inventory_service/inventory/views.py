from django.http import HttpResponseRedirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from django.contrib.auth import logout
from .models import Product, Category
from .serializers import ProductSerializer, ProductsByCategoryQuerySerializer, CategorySerializer


class ProductView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(query_serializer=ProductsByCategoryQuerySerializer())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        query_serializer = ProductsByCategoryQuerySerializer(data=self.request.query_params)
        query_serializer.is_valid(raise_exception=True)
        category_name = query_serializer.validated_data.get('category_name')
        if category_name is not None:
            queryset = queryset.filter(category__name=category_name)
        return queryset


class CategoryView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class LogoutView(generics.GenericAPIView):
    @staticmethod
    @swagger_auto_schema(auto_schema=None)
    def get(request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')
