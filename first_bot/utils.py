"""Helpers de rutas.

PASO 9: crea este módulo.
- output_filename(input_path) -> Path: retorna el archivo de salida
  conservando la ruta relativa del input dentro de OUTPUT_PATH.
"""

from pathlib import Path

from first_bot.config import INPUT_PATH, OUTPUT_PATH


def output_filename(input_path: Path) -> Path:
    """Calcula la ruta del archivo de salida manteniendo la ruta relativa."""
    ruta = Path(input_path).resolve()
    try:
        relativa = ruta.relative_to(INPUT_PATH)
    except ValueError:
        relativa = Path(ruta.name)
    return OUTPUT_PATH / relativa