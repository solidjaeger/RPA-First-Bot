"""Excepciones personalizadas del bot.

PASO 2: crea este módulo.
- Define una excepción base BotException.
- Hereda: FileReadError, ValidationFailedError, SubmissionError.
"""


class BotException(Exception):
    """Base exception del bot."""


class FileReadError(BotException):
    """Error al leer un archivo de entrada."""


class ValidationFailedError(BotException):
    """Error de validación de datos."""


class SubmissionError(BotException):
    """Error al enviar una solicitud al formulario web."""
