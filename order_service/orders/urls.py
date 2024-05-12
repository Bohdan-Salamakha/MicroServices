from django.urls import path

from .views import OrderHistoryView, OrderView

urlpatterns = [
    path('history/<int:user_id>/', OrderHistoryView.as_view(), name='orders_history'),
    path('', OrderView.as_view(), name='orders_order'),
]

app_name = 'orders'
