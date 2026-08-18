"""Lógica de negocio: validación, deduplicación y clasificación.

PASO 5: crea este módulo.
- validate(df) -> (validos: list[Solicitud], errores: list[dict]):
  convierte cada fila a Solicitud y captura errores de validación.
- deduplicate(validos, key="email") -> (unicos, duplicados):
  primera ocurrencia se mantiene, el resto se marca duplicado.
- classify(unicos, by="tipo_solicitud") -> dict[tipo, list[Solicitud]].
"""

import pandas as pd
from pydantic import ValidationError

from first_bot.models import COLUMNAS_ARCHIVO, Persona, Solicitud

CAMPOS_PERSONA = [
    "first_name",
    "last_name",
    "company_name",
    "role_in_company",
    "address",
    "email",
    "phone_number",
]
CAMPOS_SOLICITUD = [
    "tipo_solicitud",
    "fecha",
    "prioridad",
    "identificador",
    "descripcion",
    "estado",
]


def normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte los nombres de columna a snake_case (espacios -> _ y minúsculas)."""
    renombres = {}
    for columna in df.columns:
        renombres[columna] = str(columna).strip().lower().replace(" ", "_")
    return df.rename(columns=renombres)


def _fila_a_dict(fila: pd.Series) -> dict:
    """Devuelve dict con claves snake_case, descartando claves vacías."""
    return {clave: valor for clave, valor in fila.items() if str(clave).strip()}


def _es_fila_vacia(fila: pd.Series) -> bool:
    return fila.isna().all() or not any(str(v).strip() for v in fila.values)


def validate(df: pd.DataFrame) -> tuple[list[Solicitud], list[dict]]:
    """Valida cada fila del DataFrame."""
    df = normalizar_columnas(df)
    faltantes = [col for col in COLUMNAS_ARCHIVO if col not in df.columns]
    if faltantes:
        return [], [{"fila": None, "error": f"Columnas faltantes: {', '.join(faltantes)}"}]

    validos: list[Solicitud] = []
    errores: list[dict] = []
    for indice, fila in df.iterrows():
        if _es_fila_vacia(fila):
            continue
        datos = _fila_a_dict(fila)
        try:
            persona = Persona(**{campo: datos[campo] for campo in CAMPOS_PERSONA})
            solicitud = Solicitud(
                persona=persona,
                **{campo: datos[campo] for campo in CAMPOS_SOLICITUD},
            )
        except ValidationError as exc:
            errores.append(
                {
                    "fila": indice,
                    "identificador": datos.get("identificador"),
                    "error": "; ".join(
                        f"{error['loc'][0]}: {error['msg']}" for error in exc.errors()
                    ),
                }
            )
            continue
        validos.append(solicitud)
    return validos, errores


def deduplicate(
    validos: list[Solicitud], key: str = "email"
) -> tuple[list[Solicitud], list[Solicitud]]:
    """Elimina solicitudes duplicadas por clave (primera ocurrencia gana)."""
    vistos = set()
    unicos: list[Solicitud] = []
    duplicados: list[Solicitud] = []
    for solicitud in validos:
        clave = getattr(solicitud.persona, key)
        if clave in vistos:
            duplicados.append(solicitud)
        else:
            vistos.add(clave)
            unicos.append(solicitud)
    return unicos, duplicados


def classify(unicos: list[Solicitud], by: str = "tipo_solicitud") -> dict:
    """Agrupa solicitudes por campo."""
    grupos: dict = {}
    for solicitud in unicos:
        clave = getattr(solicitud, by)
        grupos.setdefault(clave, []).append(solicitud)
    return grupos