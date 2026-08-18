"""Generación de resultados: CSV, bitácora y resumen.

PASO 8: crea este módulo.
- setup_logging(): configura loguru con archivo rotativo en OUTPUT_PATH/logs.
- guardar_resultados(...): escribe el CSV de salida conservando la ruta
  relativa del archivo de entrada (tracking por fechas).
- resumen_archivo(...) y resumen_global(...): imprimen resúmenes en consola.
"""

import csv
from datetime import datetime
from pathlib import Path

from loguru import logger

from first_bot.config import OUTPUT_PATH
from first_bot.tracker import ProcessableInputFile
from first_bot.utils import output_filename

COLUMNAS_SALIDA = [
    "first_name",
    "last_name",
    "email",
    "tipo_solicitud",
    "fecha",
    "prioridad",
    "identificador",
    "estado",
    "resultado",
    "error",
]


def setup_logging() -> None:
    """Configura loguru con archivo rotativo en OUTPUT_PATH/logs."""
    directorio_logs = OUTPUT_PATH / "logs"
    directorio_logs.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = directorio_logs / f"bot_{timestamp}.log"
    logger.add(
        archivo,
        rotation="10 MB",
        retention="7 days",
        encoding="utf-8",
        enqueue=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    )


def guardar_resultados(
    entrada: ProcessableInputFile, filas: list[dict]
) -> Path:
    """Escribe el CSV de resultados conservando la ruta relativa."""
    ruta = output_filename(entrada.full_path)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_SALIDA)
        escritor.writeheader()
        escritor.writerows(filas)
    logger.info("Resultados guardados en: {}", ruta)
    return ruta


def resumen_archivo(entrada: ProcessableInputFile, stats: dict) -> None:
    """Imprime resumen por archivo."""
    logger.info("=" * 50)
    logger.info("RESUMEN: {}", entrada.path_dir)
    logger.info("  Total filas leídas:    {}", stats["total"])
    logger.info("  Válidas:               {}", stats["validos"])
    logger.info("  Duplicados:            {}", stats["duplicados"])
    logger.info("  Errores validación:    {}", stats["errores"])
    logger.info("  Envíos exitosos:       {}", stats["exitosos"])
    logger.info("  Envíos fallidos:       {}", stats["fallidos"])
    logger.info("=" * 50)


def resumen_global(stats: dict) -> None:
    """Imprime resumen global de la ejecución."""
    logger.info("=" * 50)
    logger.info("RESUMEN GLOBAL DE EJECUCIÓN")
    logger.info("  Archivos totales:      {}", stats["totales"])
    logger.info("  Archivos procesados:   {}", stats["procesados"])
    logger.info("  Archivos omitidos:     {}", stats["omitidos"])
    logger.info("=" * 50)