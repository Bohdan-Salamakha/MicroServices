from django.urls import path

from .views import CreateUserView

urlpatterns = [
    path('user/', CreateUserView.as_view(), name='user_user'),
]

app_name = 'users'
