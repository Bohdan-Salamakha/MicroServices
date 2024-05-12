import pika
from django.conf import settings


class RabbitMQService:
    _connection = None
    _channel = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None or cls._connection.is_closed:
            cls._setup_connection()
        return cls._connection

    @classmethod
    def get_channel(cls):
        if cls._channel is None or cls._channel.is_closed:
            cls._setup_channel()
        return cls._channel

    @classmethod
    def _setup_connection(cls):
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
        cls._connection = pika.BlockingConnection(parameters)

    @classmethod
    def _setup_channel(cls):
        if cls._connection is None or cls._connection.is_closed:
            cls._setup_connection()
        cls._channel = cls._connection.channel()
        cls._setup_exchange_and_queue()

    @classmethod
    def _setup_exchange_and_queue(cls):
        exchange_name = 'order_service_exchange'
        queue_name = 'check_user_queue'
        routing_key = 'check_user_key'

        cls._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct',
            durable=True
        )
        cls._channel.queue_declare(queue=queue_name, durable=True)
        cls._channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=routing_key
        )

    @classmethod
    def close_connection(cls):
        if cls._connection:
            cls._connection.close()
            cls._connection = None

    @classmethod
    def close_channel(cls):
        if cls._channel:
            cls._channel.close()
            cls._channel = None
