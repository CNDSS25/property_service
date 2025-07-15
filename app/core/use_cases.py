class PropertyUseCases:
    def __init__(self, db_adapter):
        self.db_adapter = db_adapter

    async def create_property(self, property):
        return await self.db_adapter.create_property(property)

    async def list_properties(self):
        return await self.db_adapter.list_properties()

    async def list_properties_by_owner(self, owner):
        return await self.db_adapter.list_properties_by_owner(owner)

    async def list_rental_payments(self, owner, isPaid):
        return await self.db_adapter.list_rental_payments(owner, isPaid)

    async def show_property(self, id):
        return await self.db_adapter.show_property(id)

    async def update_property(self, id, property):
        return await self.db_adapter.update_property(id, property)

    async def add_rental_income(self, id, income):
        return await self.db_adapter.add_rental_income(id, income)

    async def delete_property(self, id):
        return await self.db_adapter.delete_property(id)