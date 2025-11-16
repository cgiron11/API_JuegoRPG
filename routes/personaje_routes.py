from fastapi import APIRouter, status
from models.personaje import Personaje
from controllers.personaje_controllers import (
    get_one_personaje,
    get_all_personajes,
    create_personaje,
    update_personaje,
    delete_personaje,
    get_personaje_asignos
)

router = APIRouter(prefix="/personajes")

@router.get("/", tags=["Personaje"], status_code=status.HTTP_200_OK)
async def get_all_personajes_info():
    result = await get_all_personajes()
    return result

@router.get("/{id}", tags=["Personaje"], status_code=status.HTTP_200_OK)
async def get_one_personaje_info(id: int):
    result: Personaje = await get_one_personaje(id)
    return result

@router.post("/", tags=["Personaje"], status_code=status.HTTP_201_CREATED)
async def create_personaje_info(personaje_data: Personaje):
    result = await create_personaje(personaje_data)
    return result

@router.put("/{id}", tags=["Personaje"], status_code=status.HTTP_200_OK)
async def update_personaje_info(id: int, personaje_data: Personaje):
    personaje_data.id = id
    result = await update_personaje(personaje_data)
    return result

@router.delete("/{id}", tags=["Personaje"], status_code=status.HTTP_200_OK)
async def delete_personaje_info(id: int):
    status: str = await delete_personaje(id)
    return status

##Interaccion con personaje-asigno
@router.get("/{id}/asigno", tags=["Personaje"], status_code=status.HTTP_200_OK)
async def get_personaje_asignos_info(id: int):
    result = await get_personaje_asignos(id)
    return result