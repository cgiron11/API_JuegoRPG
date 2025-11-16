from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Inventario(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El id autoincremental del inventario"
        )
    NombreInventario: Optional [str] = Field(
        description="Nombre del inventario",
        default=None,
        pattern=r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]{1,50}$",
        examples=["Inventario Principal", "Bolsa de Pociones", "Mochila de Aventurero"]
        )