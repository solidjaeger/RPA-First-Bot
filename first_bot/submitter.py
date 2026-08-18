"""Envío de solicitudes al formulario web (Playwright).

PASO 6: crea este módulo.
- WebSubmitter con __init__(form_url, headless).
- submit(solicitudes) -> list[dict] con {identificador, resultado, error}.
- Ahora: stub que simula el registro.
- Después: Playwright sync abriendo navegador, navegando al form_url,
  llenando los campos de Persona y enviando una por una.
"""

from first_bot.models import Solicitud


class WebSubmitter:
    """Registra solicitudes en el formulario web.

    Por ahora simula el registro devolviendo éxito en todos los casos.
    En el futuro se reemplaza la implementación por Playwright sync.
    """

    def __init__(self, form_url: str, headless: bool = True):
        self.form_url = form_url
        self.headless = headless

    def submit(self, solicitudes: list[Solicitud]) -> list[dict]:
        """Simula el registro de cada solicitud en el formulario."""
        resultados = []
        for solicitud in solicitudes:
            resultados.append(
                {
                    "identificador": solicitud.identificador,
                    "resultado": "registrado",
                    "error": "",
                }
            )
        return resultados