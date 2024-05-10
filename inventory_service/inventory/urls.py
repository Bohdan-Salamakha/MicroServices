from django.urls import path

from .views import ProductView, CategoryView

urlpatterns = [
    path(
        'product/',
        ProductView.as_view(),
        name='inventory_product'
    ),
    path(
        'category/',
        CategoryView.as_view(),
        name='inventory_category'
    ),
]

app_name = 'inventory'
