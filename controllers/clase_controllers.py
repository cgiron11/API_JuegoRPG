import json
import logging
from models.clase import Clase
from Utils.database import execute_query_json
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_one_clase( id: int) -> Clase:

    selecscripts = """
        SELECT [ID],
        [NombreClase],
        [Descripcion]
    FROM [JuegoRPG].[Clases]
    Where id = ?
    """

    params = [id]
    result_dict = []

    try:
        result = await execute_query_json(selecscripts, params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"Clase not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def get_all_clases() -> list[Clase]:
    selecscripts = """
        SELECT [ID],
        [NombreClase],
        [Descripcion]
    FROM [JuegoRPG].[Clases]
    """

    result_dict = []

    try:
        result = await execute_query_json(selecscripts)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def create_clase( clase: Clase) -> Clase:
    sqlscripts: str = """
        INSERT INTO [JuegoRPG].[Clases]
        ([NombreClase],
        [Descripcion])
    VALUES (?, ?);
    """

    params = [clase.nombreClase, clase.descripcion]
    
    insert_result = None

    try:
        insert_result = await execute_query_json( sqlscripts, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
    sqlfind = """
        SELECT [ID],
            [NombreClase],
            [Descripcion]
        FROM [JuegoRPG].[Clases]
        WHERE NombreClase = ?;
        """
    params = [clase.nombreClase]

    result_dict = []
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def update_clase( clase: Clase) -> Clase:

    dict = clase.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescripts = f"""
        UPDATE [JuegoRPG].[Clases]
        SET {variables}
        WHERE id = ?;
        """
    
    params = [ dict[k] for k in keys ]
    params.append(clase.id)

    update_result = None
    try:
        update_result = await execute_query_json( updatescripts, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
    sqlfind = """
        SELECT [ID],
            [NombreClase],
            [Descripcion]
        FROM [JuegoRPG].[Clases]
        WHERE ID = ?;
        """
    params = [clase.id]
    result_dict = []
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
## Interacciones de Clase con el personaje ##
async def get_clase_personajes( id: int) -> list[Clase]:
    selecscripts = """
        SELECT p.[ID],
            p.[NombrePersonaje]
        FROM [JuegoRPG].[Personajes] p
        WHERE p.Clase_ID = ?;
    """

    params = [id]

    try:
        result = await execute_query_json(selecscripts, params)
        result_dict = json.loads(result)
        if len(result_dict) == 0:
            raise HTTPException(status_code=404, detail="No se encontro ningun personaje de la clase especificada")
        
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")