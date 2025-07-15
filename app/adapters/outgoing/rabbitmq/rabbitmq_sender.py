import pika, json
from app.config import Config
from .rabbitmq_config import rabbitmq_connection

def publish_event(event: str, payload: dict, connection=None):
    if connection is None:
        connection = rabbitmq_connection
    channel = connection.ensure_connection()
    properties = pika.BasicProperties(
        content_type='application/json',
        delivery_mode=2,
    )
    channel.basic_publish(
        exchange=Config.RABBITMQ_EXCHANGE,
        routing_key=Config.RABBITMQ_ROUTING_KEYS[event],
        body=json.dumps(payload),
        properties=properties
    )