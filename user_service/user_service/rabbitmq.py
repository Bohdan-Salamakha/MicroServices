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
