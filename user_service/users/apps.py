import pika
from django.apps import AppConfig

from user_service import settings


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


class RabbitMQConfig(AppConfig):
    connection = None
    channel = None
    name = 'rabbit_mq'
    verbose_name = 'RabbitMQ'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.connection = None
        self.channel = None

    def ready(self):
        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USERNAME,
            settings.RABBITMQ_PASSWORD
        )
        parameters = pika.ConnectionParameters(
            settings.RABBITMQ_HOST,
            settings.RABBITMQ_PORT,
            '/',
            credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    @classmethod
    def get_channel(cls):
        if cls.channel.is_closed:
            cls.channel = cls.connection.channel()
        return cls.channel
