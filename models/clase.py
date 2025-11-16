from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Clase(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El id autoincremental de la clase"
        )
    nombreClase: Optional [str] = Field(
        description="Nombre de la clase",
        pattern=r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]{1,50}$",
        default=None,
        examples=["Mago", "Guerrero", "Arquero"]
        )
    descripcion: Optional [str] = Field(
        description="Descripción de la clase",
        max_length=500,
        default=None,
        examples=["Clase especializada en ataques mágicos", "Clase con gran fuerza física"]
        )
