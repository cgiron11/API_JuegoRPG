from fastapi import APIRouter, status
from models.asigno import Asigno
from controllers.asigno_controllers import (
    get_one_Asignacion,
    get_all_Asignaciones,
    create_Asignacion,
    delete_Asignacion,
)

router = APIRouter(prefix="/asignaciones")

@router.get("/", tags=["Asigno"], status_code=status.HTTP_200_OK)
async def get_all_asignaciones_info():
    result = await get_all_Asignaciones()
    return result

@router.get("/{id}", tags=["Asigno"], status_code=status.HTTP_200_OK)
async def get_one_asignacion_info(id: int):
    result: Asigno = await get_one_Asignacion(id)
    return result

@router.post("/", tags=["Asigno"], status_code=status.HTTP_201_CREATED)
async def create_asignacion_info(asigno_data: Asigno):
    result = await create_Asignacion(asigno_data)
    return result

@router.delete("/{id}", tags=["Asigno"], status_code=status.HTTP_200_OK)
async def delete_asignacion_info(id: int):
    status: str = await delete_Asignacion(id)
    return status
