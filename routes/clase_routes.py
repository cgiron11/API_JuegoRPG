from fastapi import APIRouter, status
from models.clase import Clase
from controllers.clase_controllers import (
    get_one_clase,
    get_all_clases,
    create_clase,
    update_clase,
    get_clase_personajes
)

router = APIRouter(prefix="/clases")

@router.get("/", tags=["Clase"], status_code=status.HTTP_200_OK)
async def get_all_clases_info():
    result = await get_all_clases()
    return result

@router.get("/{id}", tags=["Clase"], status_code=status.HTTP_200_OK)
async def get_one_clase_info(id: int):
    result = await get_one_clase(id)
    return result

@router.post("/", tags=["Clase"], status_code=status.HTTP_201_CREATED)
async def create_clase_info(clase: Clase):
    result = await create_clase(clase)
    return result

@router.put("/{id}", tags=["Clase"], status_code=status.HTTP_200_OK)
async def update_clase_info(id: int, clase: Clase):
    clase.id = id
    result = await update_clase(clase)
    return result

##Interaccion con clase-personajes

@router.get("/{id}", tags=["Clase"], status_code=status.HTTP_200_OK)
async def get_clase_personajes_info(id: int):
    result = await get_clase_personajes(id)
    return result
