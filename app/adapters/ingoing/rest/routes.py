from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.responses import Response
from fastapi.security import HTTPAuthorizationCredentials

from app.adapters.outgoing.jwt.auth_adapter import get_current_user, decode_token, get_current_user_from_Token
from app.dependencies import get_db_adapter
from app.core.use_cases import PropertyUseCases
from app.core.models import PropertyModel, PropertyCollection, UpdatePropertyModel

PROTECTED = [Depends(get_current_user)]
router = APIRouter(
    dependencies=PROTECTED
)

@router.post(
    "/properties/",
    response_description="Add new property",
    response_model=PropertyModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_property(
        property: PropertyModel = Body(...),
        db_adapter=Depends(get_db_adapter)
):
    """
        Insert a new property record.

        A unique `id` will be created and provided in the response.
    """
    property_use_cases = PropertyUseCases(db_adapter)
    return await property_use_cases.create_property(property)


@router.get(
    "/properties/",
    response_description="List all properties",
    response_model=PropertyCollection,
    response_model_by_alias=False,
)
async def list_properties(db_adapter=Depends(get_db_adapter)):
    """
        List all the property data in the database.

        The response is unpaginated and limited to 1000 results.
    """
    property_use_cases = PropertyUseCases(db_adapter)
    return await property_use_cases.list_properties()


@router.get(
    "/ownedProperties/",
    response_description="List all properties from one owner",
    response_model=PropertyCollection,
    response_model_by_alias=False,
)
async def show_property_by_owner(
        owner: HTTPAuthorizationCredentials = Depends(get_current_user_from_Token),
        db_adapter=Depends(get_db_adapter)
):
    """
        Retrieve all properties associated with a specific `owner`.
    """
    property_use_cases = PropertyUseCases(db_adapter)
    properties = await property_use_cases.list_properties_by_owner(owner)
    if not properties:
        raise HTTPException(status_code=404, detail="No properties found for this owner")

    return properties


@router.get(
    "/properties/{id}",
    response_description="Get a single property",
    response_model=PropertyModel,
    response_model_by_alias=False,
)
async def show_property(id: str, db_adapter=Depends(get_db_adapter)):
    """
        Get the record for a specific property, looked up by `id`.
    """
    property_use_cases = PropertyUseCases(db_adapter)
    if (
        property := await property_use_cases.show_property(id)
    ) is not None:
        return property

    raise HTTPException(status_code=404, detail=f"Property {id} not found")


@router.put(
    "/properties/{id}",
    response_description="Update a property",
    response_model=PropertyModel,
    response_model_by_alias=False,
)
async def update_property(
        id: str,
        property: UpdatePropertyModel = Body(...),
        db_adapter=Depends(get_db_adapter)
):
    """
    Update individual fields of an existing property record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    property_use_cases = PropertyUseCases(db_adapter)
    update_result = await property_use_cases.update_property(id, property)
    if update_result is not None:
        return update_result
    else:
        raise HTTPException(status_code=404, detail=f"Property {id} not found")


@router.delete(
    "/properties/{id}",
    response_description="Delete a property"
)
async def delete_property(id: str, db_adapter=Depends(get_db_adapter)):
    """
    Remove a single property record from the database.
    """
    property_use_cases = PropertyUseCases(db_adapter)
    delete_result = await property_use_cases.delete_property(id)
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Property {id} not found")

# TODO: split in new router -> rentalPayments CRUD
@router.get(
    "/properties/rental-income-summary/",
    response_description="List all properties from one owner",
    response_model=PropertyCollection,
    response_model_by_alias=False,
)
async def get_all_rental_income_summary(
        isPaid: bool,
        owner: HTTPAuthorizationCredentials = Depends(get_current_user_from_Token),
        db_adapter=Depends(get_db_adapter)
):
    """
        Get rental income summary. Depends on `isPaid`.
    """
    property_use_cases = PropertyUseCases(db_adapter)
    rental_payments = await property_use_cases.list_rental_payments(owner, isPaid)
    if not rental_payments:
        raise HTTPException(status_code=404, detail="No rental payments found for this owner")

    return rental_payments