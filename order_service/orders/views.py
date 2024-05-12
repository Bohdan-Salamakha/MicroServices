import pika
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from .tasks import check_user_exists


class OrderView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='order_queue')
        channel.basic_publish(exchange='', routing_key='order_queue', body=str(order.id))
        connection.close()


class OrderHistoryView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user_exists = check_user_exists.apply_async(args=[user_id])
        if not user_exists.get(timeout=10):
            return Response({"error": "User does not exist"}, status=404)
        return self.queryset.objects.filter(user__id=user_id)


class LogoutView(generics.GenericAPIView):
    @staticmethod
    @swagger_auto_schema(auto_schema=None)
    def get(request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')
