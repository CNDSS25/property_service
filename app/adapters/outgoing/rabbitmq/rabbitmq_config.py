import pika
from pika.exceptions import (
    AMQPConnectionError,
    StreamLostError,
    ChannelClosedByBroker
)
import time
from app.config import Config

class RabbitMQConnection:
    def __init__(self, host, port, user, password, exchange):
        self._params = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(user, password),
            heartbeat=3600,
            blocked_connection_timeout=30,
        )
        self._exchange = exchange
        self._connection = None
        self._channel = None

    def ensure_connection(self, retries=3, delay=5):
        attempt = 0
        while attempt < retries:
            try:
                if self._connection is None or self._connection.is_closed:
                    self._connection = pika.BlockingConnection(self._params)
                    self._channel = self._connection.channel()
                    self._channel.exchange_declare(
                        exchange=self._exchange,
                        exchange_type='topic',
                        durable=True
                    )
                return self._channel
            except (AMQPConnectionError, StreamLostError, ChannelClosedByBroker) as e:
                attempt += 1
                print(f"[RabbitMQ] Connection error ({e}), retrying in {delay}s...")
                time.sleep(delay)
        raise RuntimeError("Failed to connect to RabbitMQ after multiple retries.")

    def close(self):
        if self._connection and self._connection.is_open:
            self._connection.close()

# Singleton instance
rabbitmq_connection = RabbitMQConnection(
    host=Config.RABBITMQ_HOST,
    port=Config.RABBITMQ_PORT,
    user=Config.RABBITMQ_USER,
    password=Config.RABBITMQ_PASSWORD,
    exchange=Config.RABBITMQ_EXCHANGE
)
