from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Items(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El id autoincremental del ítem"
        )
    nombreItem: Optional [str] = Field(
        description="Nombre del ítem",
        pattern=r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]{1,50}$",
        default=None,
        examples=["Espada Larga", "Arco Élfico", "Varita Mágica"]
        )