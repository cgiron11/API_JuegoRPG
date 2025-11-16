from fastapi import APIRouter, status
from models.inventario import Inventario
from controllers.inventario_controllers import (
    get_one_inventario,
    get_all_inventarios,
    create_inventario,
    update_inventario,
    delete_inventario,
)

router = APIRouter(prefix="/inventarios")

@router.get("/", tags=["Inventario"], status_code=status.HTTP_200_OK)
async def get_all_inventarios_info():
    result = await get_all_inventarios()
    return result

@router.get("/{id}", tags=["Inventario"], status_code=status.HTTP_200_OK)
async def get_one_inventario_info(id: int):
    result: Inventario = await get_one_inventario(id)
    return result

@router.post("/", tags=["Inventario"], status_code=status.HTTP_201_CREATED)
async def create_inventario_info(inventario_data: Inventario):
    result = await create_inventario(inventario_data)
    return result

@router.put("/{id}", tags=["Inventario"], status_code=status.HTTP_200_OK)
async def update_inventario_info(id: int, inventario_data: Inventario):
    inventario_data.id = id
    result = await update_inventario(inventario_data)
    return result

@router.delete("/{id}", tags=["Inventario"], status_code=status.HTTP_200_OK)
async def delete_inventario_info(id: int):
    status: str = await delete_inventario(id)
    return status