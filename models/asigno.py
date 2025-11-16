from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Asigno(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El id autoincremental del asigno"
        )
    inventarioId: Optional[int] = Field(
        description="ID del inventario asociado",
        default=None
        )
    itemId: Optional[int] = Field(
        description="ID del ítem asignado",
        default=None
        )
    personajeId: Optional[int] = Field(
        description="ID del personaje asociado",
        default=None
        )