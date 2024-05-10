from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserCreateSerializer, UserCreateWithoutPasswordSerializer


# from user_service.rabbitmq import send_message


class LogoutView(generics.GenericAPIView):
    @staticmethod
    @swagger_auto_schema(auto_schema=None)
    def get(request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={201: UserCreateWithoutPasswordSerializer()})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
