from app.core.models import PropertyCollection
from bson import ObjectId
from pymongo import ReturnDocument


class MongoDBAdapter:
    def __init__(self, collection):
        self.collection = collection

    async def create_property(self, property):
        new_property = await self.collection.insert_one(
            property.model_dump(by_alias=True, exclude=["id"])
        )
        created_property = await self.collection.find_one(
            {"_id": new_property.inserted_id}
        )
        return created_property


    async def list_properties(self):
        return PropertyCollection(properties=await self.collection.find().to_list(1000))

    async def list_properties_by_owner(self, owner):
        properties = await self.collection.find({"owner": ObjectId(owner)}).to_list(1000)
        return PropertyCollection(properties=properties)

    async def show_property(self, id):
        return await self.collection.find_one({"_id": ObjectId(id)})

    #TODO: optimieren und aufteilen
    async def update_property(self, id, property):
        property_data = {
            k: v for k, v in property.model_dump(by_alias=True).items() if v is not None
        }

        if len(property_data) >= 1:
            update_result = await self.collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": property_data},
                return_document=ReturnDocument.AFTER,
            )
            return update_result

        # The update is empty, but we should still return the matching document:
        if (existing_property := await self.collection.find_one({"_id": id})) is not None:
            return existing_property

    async def delete_property(self, id):
        return await self.collection.delete_one({"_id": ObjectId(id)})
