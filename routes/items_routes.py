from fastapi import APIRouter, status
from models.items import Items
from controllers.items_controllers import (
    get_one_item,
    get_all_items,
    create_item,
    update_item,
    delete_item,
)

router = APIRouter(prefix="/items")

@router.get("/", tags=["Items"], status_code=status.HTTP_200_OK)
async def get_all_items_info():
    result = await get_all_items()
    return result

@router.get("/{id}", tags=["Items"], status_code=status.HTTP_200_OK)
async def get_one_item_info(id: int):
    result: Items = await get_one_item(id)
    return result

@router.post("/", tags=["Items"], status_code=status.HTTP_201_CREATED)
async def create_item_info(item_data: Items):
    result = await create_item(item_data)
    return result

@router.put("/{id}", tags=["Items"], status_code=status.HTTP_200_OK)
async def update_item_info(id: int, item_data: Items):
    item_data.id = id
    result = await update_item(item_data)
    return result

@router.delete("/{id}", tags=["Items"], status_code=status.HTTP_200_OK)
async def delete_item_info(id: int):
    status: str = await delete_item(id)
    return status