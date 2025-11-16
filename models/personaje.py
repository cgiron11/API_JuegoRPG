from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Personaje(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El id autoincremental del personaje"
        )
    nombrePersonaje: Optional [str] = Field(
        description="Nombre del personaje",
        default=None,
        pattern=r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]{1,50}$",
        examples=["Aragorn", "Legolas", "Gandalf"]
        )
    nivel: Optional[int] = Field(
        description="Nivel del personaje",
        default=None,
        ge=0,
        le=200,
        examples=[1, 25, 50, 75, 100]
        )
    vida: Optional[int] = Field(
        description="Puntos de vida del personaje",
        default=None,
        ge=0,
        le=1000,
        examples=[100, 500, 1000]
        )
    Clase_ID: Optional[int] = Field(
        description="ID de la clase a la que pertenece el personaje",
        default=None,
        ge=1,
        examples=[1, 2, 3]
        )