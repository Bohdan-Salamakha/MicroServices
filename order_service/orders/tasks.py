import json
import time

import pika
import uuid
from celery import shared_task

from order_service.orders.apps import RabbitMQConfig


@shared_task
def check_user_exists(user_id):
    connection = RabbitMQConfig.get_connection()
    channel = connection.channel()
    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue
    corr_id = str(uuid.uuid4())
    channel.basic_publish(
        exchange='order_service_exchange',
        routing_key='check_user_key',
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=corr_id,
        ),
        body=json.dumps({'user_id': user_id}).encode(),
    )
    response = None

    def on_response(ch, method, props, body):
        nonlocal response
        if corr_id == props.correlation_id:
            response = body
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=False
    )

    start_time = time.time()
    timeout = 10

    while response is None and (time.time() - start_time) < timeout:
        connection.process_data_events(time_limit=0.9)
        time.sleep(0.1)

    if response is None:
        connection.close()
        raise TimeoutError("Response not received within the timeout period.")
    return response
