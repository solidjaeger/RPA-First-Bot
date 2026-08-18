# AGENTS.md

## Estado del proyecto

- **Esto es un scaffold, NO código funcional.** Todos los módulos en `Template/first_bot/*.py` son stubs (`def ...(): ... # Implementar`) con docstrings en español que marcan un paso de construcción (`PASO 1`…`PASO 11`). No asumas que el bot corre; verifica antes de ejecutar.
- No hay `README`, `requirements.txt`, `.env`, venv, tests, CI ni repo git. Los archivos de salida/logs en `Template/data/output/` provienen de una implementación anterior que fue reseteada a stubs.
- `Template.zip` en la raíz es una copia de respaldo del proyecto; no editar.

## Código y convenciones

- **Idioma:** docstrings, comentarios, mensajes de log y resúmenes van en español (convención del repo).
- **Orden de implementación:** los `PASO N` son vinculantes — `config` → `exceptions` → `models` → `readers` → `services` → `submitter` → `tracker` → `reporter` → `utils` → `orchestrator` → `main`. `orchestrator.py` (PASO 10) cablea el pipeline completo.
- **Stack planeado (declarado en docstrings; nada instalado aún):** python-dotenv, Pydantic v2, pandas (`engine="openpyxl"` para xlsx), loguru (rotación de logs), Playwright solo en `submitter.py` (por ahora es un stub; la implementación real del form llega después).
- `services.deduplicate` usa `key="email"` por defecto.

## Pipeline y datos

- Flujo: `config` → `tracker.get_unprocessed_files` → por archivo: `readers` → `services.validate` → `services.deduplicate` → `services.classify` → `submitter` → `reporter.guardar_resultados`.
- **Layout de datos:**
  - Entrada: `data/input/` (solo `.csv`, `.xlsx`, `.xls`).
  - Salida: `data/output/resultado_{stem}.csv` (ver `utils.output_filename`).
  - Logs: `data/output/logs/bot_YYYYMMDD_HHMMSS.log` (loguru, rotativo).
- **Idempotencia:** si `data/output/resultado_{stem}.csv` ya existe para un archivo de entrada, se salta (lógica de `tracker.py`).
- **Esquema de entrada (13 columnas):** `Persona` = `first_name, last_name, company_name, role_in_company, address, email, phone_number`; `Solicitud` = `tipo_solicitud, fecha, prioridad, identificador, descripcion, estado`. El archivo sentinel `data/input/solicitudes_prueba.csv` (UTF-8, con acentos/ñ, 20 filas) es la referencia canónica.
- **CSV de salida (10 columnas):** `first_name,last_name,email,tipo_solicitud,fecha,prioridad,identificador,estado,resultado,error`.
- Lectura de CSV/pandas requiere el parámetro de encoding UTF-8.