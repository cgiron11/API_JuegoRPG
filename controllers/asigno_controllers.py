import json
import logging
from models.asigno import Asigno
from Utils.database import execute_query_json
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_all_Asignaciones() -> list[Asigno]:
    selecscripts = """
        SELECT [ID],
        [Inventario_Id],
        [Item_Id],
        [Personaje_Id]
    FROM [JuegoRPG].[Asigno]
    """

    result_dict = []

    try:
        result = await execute_query_json(selecscripts)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")

async def get_one_Asignacion( id: int) -> Asigno:

    selecscripts: str = """
        SELECT 
            ii.[ID] as Id,
            ii.[Inventario_Id],
            ii.[Item_Id],
            ii.[Personaje_Id],
            i.[Nombre_Inventario],
            it.[Nombre_Item],
            p.[NombrePersonaje] as Nombre_Personaje
        FROM [JuegoRPG].[Asigno] ii
        INNER JOIN [JuegoRPG].[Inventarios] i ON ii.[Inventario_Id] = i.[ID]
        INNER JOIN [JuegoRPG].[Items] it ON ii.[Item_Id] = it.[ID]
        INNER JOIN [JuegoRPG].[Personajes] p ON ii.[Personaje_Id] = p.[ID]
        WHERE ii.[ID] = ?;
    """
    params = [id]
    result_dict = []
    try:
        result = await execute_query_json(selecscripts, params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"Asignacion no encontrada")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")

async def create_Asignacion( asigno: Asigno) -> Asigno:
    sqlscripts: str = """
        INSERT INTO [JuegoRPG].[Asigno]
        ([Inventario_Id],
        [Item_Id],
        [Personaje_Id])
    VALUES (?, ?, ?);
    """

    params = [asigno.inventarioId, asigno.itemId, asigno.personajeId]
    insert_result = None

    try:
        insert_result = await execute_query_json(sqlscripts, params)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
    sqlfind: str = """
        SELECT [ID],
        [Inventario_Id],
        [Item_Id],
        [Personaje_Id]
        FROM [JuegoRPG].[Asigno]
        WHERE Inventario_Id = ? AND Item_Id = ? AND Personaje_Id = ?;
        """
    params = [asigno.inventarioId, asigno.itemId, asigno.personajeId]
    result_dict = []
    try:
        result = await execute_query_json(sqlfind, params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return[]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def delete_Asignacion( id: int) -> str:
    deletescripts: str = """
        DELETE FROM [JuegoRPG].[Asigno]
        WHERE ID = ?;
    """

    params = [id]

    try:
        await execute_query_json(deletescripts, params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")