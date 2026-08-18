"""Detección de archivos ya procesados (tracking por fechas y conjuntos).

PASO 7: crea este módulo.

Nuevo sistema (tarea):
- ProcessableInputFile y ProcessableOutputFile son dataclasses congeladas,
  comparables entre sí por su ruta relativa (path_dir).
- get_unprocessed_files() recorre recursivamente input y output, construye
  conjuntos de objetos procesables y devuelve la diferencia inputs - outputs.
- Solo se consideran archivos .csv y .xlsx.
"""

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Union

from first_bot.config import INPUT_PATH, OUTPUT_PATH

EXTENSIONES = {".csv", ".xlsx"}
_PATRON_FECHA = re.compile(r"(\d{4})/(\d{1,2})/(\d{1,2})")

ProcessableFile = Union["ProcessableInputFile", "ProcessableOutputFile"]


def _extraer_fecha(path_dir: str) -> date:
    """Extrae year/month/day del primer segmento fecha de la ruta."""
    coincidencia = _PATRON_FECHA.search(path_dir)
    if coincidencia:
        anio, mes, dia = map(int, coincidencia.groups())
        try:
            return date(anio, mes, dia)
        except ValueError:
            pass
    return date.min


def _clasificar(path_dir: str, full_path: Path) -> tuple[int, int, int, date]:
    """Calcula year, month, day y date a partir de la ruta relativa."""
    fecha = _extraer_fecha(path_dir)
    return fecha.year, fecha.month, fecha.day, fecha


@dataclass(frozen=True)
class ProcessableInputFile:
    """Archivo de entrada pendiente o ya procesado.

    Igualdad y hash por path_dir, sin importar si es input u output.
    """

    year: int
    month: int
    day: int
    date: date
    path_dir: str
    full_path: Path

    @classmethod
    def desde_ruta(cls, base: Path, archivo: Path) -> "ProcessableInputFile":
        path_dir = archivo.relative_to(base).as_posix()
        anio, mes, dia, fecha = _clasificar(path_dir, archivo)
        return cls(anio, mes, dia, fecha, path_dir, archivo.resolve())

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, (ProcessableInputFile, ProcessableOutputFile)):
            return NotImplemented
        return self.path_dir == otro.path_dir

    def __hash__(self) -> int:
        return hash(self.path_dir)


@dataclass(frozen=True)
class ProcessableOutputFile:
    """Archivo de salida existente.

    Igualdad y hash por path_dir, sin importar si es input u output.
    """

    year: int
    month: int
    day: int
    date: date
    path_dir: str
    full_path: Path

    @classmethod
    def desde_ruta(cls, base: Path, archivo: Path) -> "ProcessableOutputFile":
        path_dir = archivo.relative_to(base).as_posix()
        anio, mes, dia, fecha = _clasificar(path_dir, archivo)
        return cls(anio, mes, dia, fecha, path_dir, archivo.resolve())

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, (ProcessableInputFile, ProcessableOutputFile)):
            return NotImplemented
        return self.path_dir == otro.path_dir

    def __hash__(self) -> int:
        return hash(self.path_dir)


def _recorrer(
    base: Path, cls: type[ProcessableFile]
) -> set[ProcessableFile]:
    """Recorre recursivamente un directorio y devuelve archivos procesables."""
    resultado: set[ProcessableFile] = set()
    if not base.exists():
        return resultado
    for ruta in base.rglob("*"):
        if ruta.is_file() and ruta.suffix.lower() in EXTENSIONES:
            resultado.add(cls.desde_ruta(base, ruta))
    return resultado


def get_unprocessed_files() -> list[ProcessableInputFile]:
    """Devuelve los archivos de entrada pendientes (inputs - outputs)."""
    inputs: set[ProcessableFile] = _recorrer(INPUT_PATH, ProcessableInputFile)
    outputs: set[ProcessableFile] = _recorrer(OUTPUT_PATH, ProcessableOutputFile)
    pendientes = inputs - outputs
    return sorted(pendientes, key=lambda archivo: archivo.path_dir)