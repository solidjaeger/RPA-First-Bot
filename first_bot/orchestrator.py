"""Orquestador del pipeline.

PASO 10: crea este módulo.
- Orchestrator con método run().
- Orden: setup_logging -> get_unprocessed_files -> por archivo:
  leer -> validar -> deduplicar -> clasificar -> enviar -> guardar resultados.
- Usa loguru para registrar cada paso.
"""

from loguru import logger

from first_bot.config import HEADLESS, WEB_FORM_URL
from first_bot.exceptions import FileReadError
from first_bot.readers import reader_factory
from first_bot.reporter import (
    guardar_resultados,
    resumen_archivo,
    resumen_global,
    setup_logging,
)
from first_bot.services import classify, deduplicate, validate
from first_bot.submitter import WebSubmitter
from first_bot.tracker import ProcessableInputFile, get_unprocessed_files

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


class Orchestrator:
    """Coordina el pipeline completo."""

    def __init__(self):
        self.submitter = WebSubmitter(WEB_FORM_URL, headless=HEADLESS)

    def _procesar_archivo(self, entrada: ProcessableInputFile) -> dict:
        """Lee, valida, deduplica, clasifica, envía y guarda un archivo."""
        logger.info("Procesando: {}", entrada.path_dir)
        try:
            lector = reader_factory(entrada.full_path.suffix)
            df = lector.read(entrada.full_path)
        except FileReadError as exc:
            logger.error("  Error de lectura: {}", exc)
            raise

        validos, errores = validate(df)
        unicos, duplicados = deduplicate(validos)
        grupos = classify(unicos)
        logger.info("  Validación: {} válidos, {} errores", len(validos), len(errores))
        logger.info("  Clasificación: {} tipo(s)", len(grupos))

        resultados = self.submitter.submit(unicos)
        exitosos = sum(1 for r in resultados if not r["error"])
        fallidos = len(resultados) - exitosos
        logger.info("  Envíos: {} OK, {} fallidos", exitosos, fallidos)

        filas = self._construir_filas(validos, duplicados, resultados)
        guardar_resultados(entrada, filas)

        return {
            "total": len(df),
            "validos": len(validos),
            "duplicados": len(duplicados),
            "errores": len(errores),
            "exitosos": exitosos,
            "fallidos": fallidos,
        }

    @staticmethod
    def _construir_filas(validos, duplicados, resultados) -> list[dict]:
        """Une solicitudes válidas, duplicadas y resultados de envío."""
        resultado_por_id = {r["identificador"]: r for r in resultados}
        ids_duplicados = {s.identificador for s in duplicados}
        filas = []
        for solicitud in validos:
            envio = resultado_por_id.get(
                solicitud.identificador,
                {"resultado": "no_enviado", "error": ""},
            )
            if solicitud.identificador in ids_duplicados:
                estado_resultado = "duplicado"
                error = "Duplicado: no enviado."
            else:
                estado_resultado = envio["resultado"]
                error = envio["error"]
            filas.append(
                {
                    "first_name": solicitud.persona.first_name,
                    "last_name": solicitud.persona.last_name,
                    "email": solicitud.persona.email,
                    "tipo_solicitud": solicitud.tipo_solicitud,
                    "fecha": solicitud.fecha.isoformat(),
                    "prioridad": solicitud.prioridad,
                    "identificador": solicitud.identificador,
                    "estado": solicitud.estado,
                    "resultado": estado_resultado,
                    "error": error,
                }
            )
        return filas

    def run(self) -> None:
        """Ejecuta el proceso completo."""
        setup_logging()
        pendientes = get_unprocessed_files()
        logger.info("Archivos pendientes: {}", len(pendientes))

        procesados = 0
        omitidos = 0
        for entrada in pendientes:
            try:
                stats = self._procesar_archivo(entrada)
            except FileReadError:
                omitidos += 1
                continue
            procesados += 1
            resumen_archivo(entrada, stats)

        resumen_global(
            {
                "totales": len(pendientes),
                "procesados": procesados,
                "omitidos": omitidos,
            }
        )