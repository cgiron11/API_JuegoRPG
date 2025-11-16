import json
import logging
from models.items import Items
from Utils.database import execute_query_json
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_all_items() -> list[Items]:
    selecscripts = """
        SELECT [ID],
        [NombreItem]
    FROM [JuegoRPG].[Items]
    """

    result_dict = []

    try:
        result = await execute_query_json(selecscripts)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")

async def get_one_item( id: int) -> Items:

    selecscripts = """
        SELECT [ID],
        [NombreItem]
    FROM [JuegoRPG].[Items]
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
            raise HTTPException(status_code=404, detail=f"Item not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def create_item( item: Items) -> Items:
    sqlscripts: str = """
        INSERT INTO [JuegoRPG].[Items]
        ([NombreItem])
    VALUES (?);
    """

    params = [item.nombreItem]
    insert_result = None

    try:
        insert_result = await execute_query_json(sqlscripts, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
    sqlfind: str = """
        SELECT [ID],
        [NombreItem]
        FROM [JuegoRPG].[Items]
        WHERE NombreItem = ?;
        """
    params = [item.nombreItem]
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
    
async def update_item(item: Items) -> Items:
    updatescripts: str = f"""
        UPDATE [JuegoRPG].[Items]
        SET [NombreItem] = ?
        WHERE [id] = ?;
        """
    params = [item.nombreItem, item.id]
    update_result=None
    try:
        update_ressult=await execute_query_json(updatescripts, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
    sqlfind: str = f"""
        SELECT [ID],
        [NombreItem]
        FROM [JuegoRPG].[Items]
        WHERE NombreItem = ?;
        """
    params = [item.nombreItem]
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

async def delete_item( id: int) -> str:
    deletescripts: str = """
        DELETE FROM [JuegoRPG].[Items]
        WHERE id = ?;
        """
    params = [id]

    try:
        await execute_query_json(deletescripts, params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")