import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key_example")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    MONGODB_URL = os.getenv("MONGODB_URL")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", default="guest")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", default="guest")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", default="localhost")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", default=5672)
    RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", default="FinSight")

    routing_keys = os.getenv("RABBITMQ_ROUTING_KEYS_COLLECTION",
                       default="properties_listed,rental_income")
    routing_keys_list = routing_keys.split(',')

    RABBITMQ_ROUTING_KEYS = {
        'properties_listed': routing_keys_list[0],
        'rental_income': routing_keys_list[1],
    }