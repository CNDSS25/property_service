from motor.motor_asyncio import AsyncIOMotorClient
from app.adapters.outgoing.db.db_adapter import MongoDBAdapter
from app.config import Config


client = AsyncIOMotorClient(Config.MONGODB_URL)
db = client.property_service
collection = db.get_collection("properties")
db_adapter = MongoDBAdapter(collection=collection)

def get_db_adapter():
    """
    Gibt den globalen Datenbankadapter zurück.
    """
    return db_adapter