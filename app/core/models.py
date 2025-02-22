from datetime import date
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from pydantic import ConfigDict, BaseModel, Field
from typing import Optional, List
from bson import ObjectId

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class RentalIncome(BaseModel):
    """
        Container for a rental income record.
    """

    date: date
    amount: float = Field(..., gt=0)
    tenant: str = Field(...)
    payment_method: str = Field(...)
    status: str = Field(...) # Paid, Pending, Overdue

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "date": "2024-02-01",
                "amount": 1200.0,
                "tenant": "John Doe",
                "payment_method": "Bank Transfer",
                "status": "Paid"
            }
        },
    )

class PropertyModel(BaseModel):
    """
    Container for a single property record.
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    owner: Optional[PyObjectId] = Field(alias="owner", default=None)
    title: str = Field(...)
    description: str = Field(...)
    price: float = Field(..., gt=0)
    location: str = Field(...)
    size_sqm: float = Field(..., gt=0)  # Size in square meters
    bedrooms: int = Field(..., ge=0)
    bathrooms: int = Field(..., ge=0)
    property_type: str = Field(...)  # e.g., "Apartment", "House", "Commercial"
    availability_status: str = Field(...)  # e.g., "Available", "Sold", "Rented"
    rental_income: List[RentalIncome]

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Luxury Villa with Sea View",
                "description": "A beautiful villa with 4 bedrooms and a private pool.",
                "price": 1200000.00,
                "location": "Mallorca, Spain",
                "size_sqm": 250.5,
                "bedrooms": 4,
                "bathrooms": 3,
                "property_type": "Villa",
                "availability_status": "Available",
                "rental_income": ""
            }
        },
    )


class UpdatePropertyModel(BaseModel):
    """
    A set of optional updates to be made to a property document in the database.
    """

    owner: Optional[PyObjectId] = Field(alias="owner", default=None)
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    size_sqm: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    property_type: Optional[str] = None
    availability_status: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "Updated Luxury Villa",
                "description": "A newly renovated villa with modern amenities.",
                "price": 1250000.00,
                "location": "Ibiza, Spain",
                "size_sqm": 260.0,
                "bedrooms": 5,
                "availability_status": "Available",
                "rental_income": ""
            }
        },
    )


class PropertyCollection(BaseModel):
    """
    A container holding a list of `PropertyModel` instances.
    """

    properties: List[PropertyModel]
