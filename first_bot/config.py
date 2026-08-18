"""Configuración del bot desde .env.

PASO 1: crea este módulo.
- Carga variables de entorno con python-dotenv.
- Expone INPUT_PATH, OUTPUT_PATH, WEB_FORM_URL, HEADLESS como constantes.
- Usa rutas relativas con defaults razonables.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

INPUT_PATH = Path(os.getenv("INPUT_PATH", RAIZ_PROYECTO / "data" / "input")).resolve()
OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH", RAIZ_PROYECTO / "data" / "output")).resolve()
WEB_FORM_URL = os.getenv("WEB_FORM_URL", "https://ejemplo.com/formulario-solicitudes")
HEADLESS = os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")


def leer_config():
    """Lee y expone la configuración desde .env."""
    return {
        "INPUT_PATH": INPUT_PATH,
        "OUTPUT_PATH": OUTPUT_PATH,
        "WEB_FORM_URL": WEB_FORM_URL,
        "HEADLESS": HEADLESS,
    }
