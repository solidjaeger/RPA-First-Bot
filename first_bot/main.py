"""Entrypoint del bot.

PASO 11: crea este módulo.
- main() instancia Orchestrator y llama run().
"""

from first_bot.orchestrator import Orchestrator


def main():
    """Punto de entrada del bot."""
    Orchestrator().run()


if __name__ == "__main__":
    main()