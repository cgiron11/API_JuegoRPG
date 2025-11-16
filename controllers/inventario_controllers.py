import json
import logging
from models.inventario import Inventario
from Utils.database import execute_query_json
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_all_inventarios() -> list[Inventario]:
    selecscripts = """
        SELECT [ID],
        [NombreInventario]
    FROM [JuegoRPG].[Inventarios]
    """

    result_dict = []

    try:
        result = await execute_query_json(selecscripts)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")

async def get_one_inventario( id: int) -> Inventario:

    selecscripts = """
        SELECT [ID],
        [NombreInventario]
    FROM [JuegoRPG].[Inventarios]
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
            raise HTTPException(status_code=404, detail=f"Inventario not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def create_inventario( inventario: Inventario) -> Inventario:
    sqlscripts: str = """
        INSERT INTO [JuegoRPG].[Inventarios]
        ([NombreInventario])
    VALUES (?);
    """

    params = [inventario.NombreInventario]
    insert_result = None

    try:
        insert_result = await execute_query_json(sqlscripts, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
    sqlfind: str = """
        SELECT [ID],
        [NombreInventario]
        FROM [JuegoRPG].[Inventarios]
        WHERE NombreInventario = ?;
        """
    params = [inventario.NombreInventario]
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

async def update_inventario(inventario: Inventario) -> Inventario:
    updatescripts: str = f"""
        UPDATE [JuegoRPG].[Inventarios]
        SET NombreInventario = ?
        WHERE [id] = ?;
        """
    params = [inventario.NombreInventario, inventario.id]
    update_result = None
    try:
        update_result=await execute_query_json(updatescripts, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
    sqlfind: str = f"""
        SELECT [ID],
        [NombreInventario]
        FROM [JuegoRPG].[Inventarios]
        WHERE NombreInventario = ?;
        """
    params = [inventario.NombreInventario]
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

async def delete_inventario( id: int) -> str:
    deletescripts: str = f"""
        DELETE FROM [JuegoRPG].[Inventarios]
        WHERE [id] = ?;
        """
    params = [id]

    try:
        await execute_query_json(deletescripts, params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")