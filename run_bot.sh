#!/usr/bin/env bash
# Launcher en bucle para Linux (equivalente a run_bot.bat)

echo "========================================"
echo "  First Bot - Procesador de Solicitudes"
echo "========================================"
echo
echo "Presiona Ctrl+C para detener el bot."
echo

while true; do
    echo "[$(date '+%d/%m/%Y %H:%M:%S')] Ejecutando bot..."
    ".venv/bin/python" -m first_bot.main
    echo
    echo "[$(date '+%d/%m/%Y %H:%M:%S')] Esperando 60 segundos para la proxima ejecucion..."
    echo "(Presiona cualquier tecla para pausar/reanudar)"
    read -r -t 60 -n 1
done
