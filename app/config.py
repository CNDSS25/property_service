import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key_example")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    MONGODB_URL = os.getenv("MONGODB_URL")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
