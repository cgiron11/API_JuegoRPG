import json
import logging
from models.personaje import Personaje
from Utils.database import execute_query_json
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_all_personajes() -> list[Personaje]:
    selecscripts = """
        SELECT [ID],
        [NombrePersonaje],
        [Nivel],
        [Vida],
        [Clase_ID]
    FROM [JuegoRPG].[Personajes]
    """

    result_dict = []

    try:
        result = await execute_query_json(selecscripts)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")

async def get_one_personaje( id: int) -> Personaje:

    selecscripts = """
    SELECT p.[ID],
           p.[NombrePersonaje],
           p.[Nivel],
           p.[Vida],
           p.[Clase_ID],
           c.[NombreClase],
           c.[Descripcion]
    FROM [JuegoRPG].[Personajes] p
    INNER JOIN [JuegoRPG].[Clases] c ON p.Clase_ID = c.ID
    WHERE p.ID = ?
    """

    params = [id]
    result_dict = []

    try:
        result = await execute_query_json(selecscripts, params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"Personaje not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def create_personaje( personaje: Personaje) -> Personaje:
    sqlscripts: str = """
        INSERT INTO [JuegoRPG].[Personajes]
        ([NombrePersonaje],
        [Nivel],
        [Vida],
        [Clase_ID])
    VALUES (?, ?, ?, ?);
    """

    params = [personaje.nombrePersonaje, personaje.nivel, personaje.vida, personaje.Clase_ID]

    insert_result = None

    try:
        insert_result = await execute_query_json(sqlscripts, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
    sqlfind: str = """
        SELECT [ID],
        [NombrePersonaje],
        [Nivel],
        [Vida],
        [Clase_ID]
        FROM [JuegoRPG].[Personajes]
        WHERE NombrePersonaje = ?;
        """
    params = [personaje.nombrePersonaje]
    result_dict = []
    try:
        result = await execute_query_json(sqlfind, params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }") 

async def update_personaje( personaje: Personaje) -> Personaje:

    dict = personaje.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescripts: str = f"""
        UPDATE [JuegoRPG].[Personajes]
        SET {variables}
        WHERE [id] = ?;
    """
    params = [ dict[k] for k in keys ]
    params.append( personaje.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescripts, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    sqlfind: str = f"""
        SELECT [ID],
        [NombrePersonaje],
        [Nivel],
        [Vida],
        [Clase_ID]
        FROM [JuegoRPG].[Personajes]
        WHERE id = ?;
        """
    params = [personaje.id]
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
    
async def delete_personaje( id: int) -> str:
    deletescripts: str = """
        DELETE FROM [JuegoRPG].[Personajes]
        WHERE [id] = ?;
    """

    params = [id]

    try:
        await execute_query_json(deletescripts, params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
## Interacioness de personaje con Asigno
async def get_personaje_asignos( id: int) -> dict:
    selecscripts = """
        SELECT p.[ID] as Personaje_Id,
            p.[NombrePersonaje] as Nombre_Personaje,
            p.[Nivel],
            p.[Vida],
            p.[Clase_ID],
            a.[ID] as Asignacion_ID,
            a.[Inventario_ID],
            a.[Item_ID],
            a.[Personaje_ID]
        FROM [JuegoRPG].[Personajes] p
        INNER JOIN [JuegoRPG].[Asigno] a ON p.[ID] = a.[Personaje_ID]
        WHERE p.[ID] = ?;
    """

    params = [id]

    try:
        result = await execute_query_json(selecscripts, params)
        result_dict = json.loads(result)

        if len(result_dict) == 0:
            raise HTTPException(status_code=404, detail="No se encontro ninguna asignacion con este personaje")
        primer_registro = result_dict[0]
        asignaciones = []
        for registro in result_dict:
            asignacion = {
                "Asignacion_ID": registro["Asignacion_ID"],
                "Inventario_ID": registro["Inventario_ID"],
                "Item_ID": registro["Item_ID"],
            }
            asignaciones.append(asignacion)
        
        response = {
            "Personaje_Id": primer_registro["Personaje_Id"],
            "Nombre_Personaje": primer_registro["Nombre_Personaje"],
            "Nivel": primer_registro["Nivel"],
            "Vida": primer_registro["Vida"],
            "Clase_ID": primer_registro["Clase_ID"],
            "Asignaciones": asignaciones
        }

        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")