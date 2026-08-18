"""Lectura de archivos con pandas (patrón Strategy + Factory).

PASO 4: crea este módulo.
- BaseReader (ABC) con método abstracto read(filepath) -> DataFrame.
- CsvReader: pd.read_csv.
- XlsxReader: pd.read_excel(engine="openpyxl").
- reader_factory(extension) -> BaseReader según .csv/.xlsx/.xls.
- Lanza FileReadError si el archivo no se puede leer.
"""

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from first_bot.exceptions import FileReadError

ENCODING = "utf-8"
EXTENSIONES = {".csv", ".xlsx", ".xls"}


class BaseReader(ABC):
    """Clase abstracta de lector de archivos."""

    @abstractmethod
    def read(self, filepath: Path) -> pd.DataFrame:
        """Lee el archivo y retorna un DataFrame."""


class CsvReader(BaseReader):
    """Lector de archivos CSV con encoding UTF-8."""

    def read(self, filepath: Path) -> pd.DataFrame:
        try:
            return pd.read_csv(filepath, encoding=ENCODING)
        except Exception as exc:
            raise FileReadError(f"No se pudo leer {filepath}: {exc}") from exc


class XlsxReader(BaseReader):
    """Lector de archivos Excel con engine openpyxl."""

    def read(self, filepath: Path) -> pd.DataFrame:
        try:
            return pd.read_excel(filepath, engine="openpyxl")
        except Exception as exc:
            raise FileReadError(f"No se pudo leer {filepath}: {exc}") from exc


def reader_factory(extension: str) -> BaseReader:
    """Retorna el lector según la extensión."""
    extension = extension.lower()
    if extension not in EXTENSIONES:
        raise FileReadError(f"Extensión no soportada: {extension}")
    if extension == ".csv":
        return CsvReader()
    return XlsxReader()