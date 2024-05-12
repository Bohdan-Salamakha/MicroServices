from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from drf_yasg.utils import swagger_auto_schema
from order_service.celery import app
from rest_framework import generics
from rest_framework.exceptions import NotFound

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderHistoryView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        result = app.send_task(
            'users.tasks.check_user_exists',
            args=[user_id],
            queue='check_user_queue',
        )
        if not result.get(timeout=10):
            raise NotFound('User does not exist')
        return self.queryset.filter(user_id=user_id)


class LogoutView(generics.GenericAPIView):
    @staticmethod
    @swagger_auto_schema(auto_schema=None)
    def get(request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')
