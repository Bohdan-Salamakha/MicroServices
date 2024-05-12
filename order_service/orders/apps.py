import pika
from django.apps import AppConfig
from pika.adapters import BlockingConnection

from user_service import settings


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'


class RabbitMQConfig(AppConfig):
    connection: BlockingConnection = None
    channel = None
    name = 'rabbit_mq'
    verbose_name = 'RabbitMQ'

    @classmethod
    def ready(cls):
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
        cls.connection = pika.BlockingConnection(parameters)
        cls.channel = cls.connection.channel()
        exchange_name = 'order_service_exchange'
        cls.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct',
            durable=True
        )
        queue_name = 'check_user_queue'
        cls.channel.queue_declare(queue=queue_name, durable=True)
        cls.channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key='check_user_key'
        )

    @classmethod
    def get_channel(cls):
        if cls.channel.is_closed:
            cls.channel = cls.connection.channel()
        return cls.channel

    @classmethod
    def get_connection(cls):
        if cls.connection.is_closed:
            cls.ready()
        return cls.connection
