# Tarea: Nuevo sistema de tracking por fechas con conjuntos

## Contexto actual

El bot actualmente busca archivos planos en data/input/ y compara con data/output/ usando el prefijo resultado_. Es simple pero poco escalable.

## Nueva estructura de directorios


data/input/
  2028/01/15/
    solicitudes_a.csv
    pedidos_b.xlsx
  2028/01/16/
    reclamos_c.csv

data/output/
  2028/01/15/
    solicitudes_a.csv
    pedidos_b.xlsx
  2028/01/16/
    (vacío → reclamos_c.csv está pendiente)


Los archivos de salida mantienen el mismo nombre y la misma ruta relativa que los de entrada. Si un archivo existe en ambas ramas con la misma ruta relativa, ya fue procesado.

## Consigna

### 1. Crear las clases ProcessableInputFile y ProcessableOutputFile

Ambas deben ser @dataclass(frozen=True) y deben ser *comparables entre sí* (un input puede compararse con un output y viceversa). La igualdad se define por la *ruta relativa* dentro del directorio base.

Atributos requeridos:

| Atributo    | Tipo   | Ejemplo                                      | De dónde se obtiene                    |
| ----------- | ------ | -------------------------------------------- | -------------------------------------- |
| year      | int  | 2028                                       | Extraído de la ruta                    |
| month     | int  | 1                                          | Extraído de la ruta                    |
| day       | int  | 15                                         | Extraído de la ruta                    |
| date      | date | date(2028, 1, 15)                          | Construido con year/month/day          |
| path_dir  | str  | "2028/01/15/solicitudes.csv"               | Ruta relativa desde el directorio base |
| full_path | Path | /abs/data/input/2028/01/15/solicitudes.csv | Ruta absoluta real                     |

Deben implementar __eq__ y __hash__ para que dos objetos sean iguales si comparten path_dir, *sin importar* si uno es input y otro output.

### 2. Reescribir get_unprocessed_files()

La función debe devolver los archivos pendientes de procesar aplicando *diferencia de conjuntos*:

1. Recorrer recursivamente el directorio de entrada y crear objetos ProcessableInputFile
2. Recorrer recursivamente el directorio de salida y crear objetos ProcessableOutputFile
3. Obtener los pendientes como inputs - outputs

Solo deben considerarse las extensiones .csv, .xlsx.
