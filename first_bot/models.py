"""Modelos de datos con Pydantic.

PASO 3: crea este módulo.
- Persona(BaseModel): first_name, last_name, company_name, role_in_company,
  address, email (EmailStr), phone_number. Validar campos no vacíos.
- Solicitud(BaseModel): persona (Persona embebida), tipo_solicitud,
  fecha (date), prioridad (Literal alta/media/baja), identificador,
  descripcion, estado (Literal pendiente/en_proceso/completada).
- Validar fecha desde múltiples formatos de string.
- COLUMNAS_ARCHIVO: lista de las 13 columnas esperadas del archivo.
"""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

Prioridad = Literal["alta", "media", "baja"]
Estado = Literal["pendiente", "en_proceso", "completada"]

FORMATOS_FECHA = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y")

COLUMNAS_ARCHIVO = [
    "first_name",
    "last_name",
    "company_name",
    "role_in_company",
    "address",
    "email",
    "phone_number",
    "tipo_solicitud",
    "fecha",
    "prioridad",
    "identificador",
    "descripcion",
    "estado",
]


def _validar_no_vacio(valor: object) -> str:
    """Rechaza None, NaN o cadenas vacías/solo espacios."""
    if valor is None:
        raise ValueError("El campo no puede estar vacío.")
    if isinstance(valor, float) and valor != valor:  # NaN
        raise ValueError("El campo no puede estar vacío.")
    texto = str(valor).strip()
    if not texto:
        raise ValueError("El campo no puede estar vacío.")
    return texto


class Persona(BaseModel):
    """Datos personales mapeables al formulario web."""

    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    company_name: str = Field(min_length=1)
    role_in_company: str = Field(min_length=1)
    address: str = Field(min_length=1)
    email: EmailStr
    phone_number: str = Field(min_length=1)

    @field_validator(
        "first_name",
        "last_name",
        "company_name",
        "role_in_company",
        "address",
        "phone_number",
        mode="before",
    )
    @classmethod
    def _normalizar_texto(cls, valor: object) -> str:
        return _validar_no_vacio(valor)


class Solicitud(BaseModel):
    """Solicitud completa: persona + datos de negocio."""

    persona: Persona
    tipo_solicitud: str = Field(min_length=1)
    fecha: date
    prioridad: Prioridad
    identificador: str = Field(min_length=1)
    descripcion: str = Field(min_length=1)
    estado: Estado

    @field_validator("tipo_solicitud", "identificador", "descripcion", mode="before")
    @classmethod
    def _normalizar_texto(cls, valor: object) -> str:
        return _validar_no_vacio(valor)

    @field_validator("fecha", mode="before")
    @classmethod
    def _parsear_fecha(cls, valor: object) -> date:
        if isinstance(valor, datetime):
            return valor.date()
        if isinstance(valor, date):
            return valor
        texto = str(valor).strip()
        for formato in FORMATOS_FECHA:
            try:
                return datetime.strptime(texto, formato).date()
            except ValueError:
                continue
        raise ValueError(f"Formato de fecha no reconocido: {valor!r}")
