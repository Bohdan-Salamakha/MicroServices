import pika
from django.conf import settings


def get_rabbit_connection():
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
    return pika.BlockingConnection(parameters)


def send_message(queue_name, message):
    connection = get_rabbit_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    connection.close()
