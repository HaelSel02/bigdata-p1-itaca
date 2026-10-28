import hashlib
import hmac
import json
import logging
import os
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingesta_itaca_xml")

RAIZ = Path(__file__).resolve().parent.parent
DIR_ENTRADA = RAIZ / "data" / "exportaciones"
DIR_SALIDA = RAIZ / "data" / "raw"

TABLAS = ["alumnos", "cursos", "calificaciones", "contenidos"]

# {columna_json: atributo_xml}; "Anyo" lo añade el script desde la carpeta
CONFIG = {
    "alumnos": {
        "nodo": "alumno",
        "campos": {"NIA": "NIA", "Curso": "curso", "Turno": "turno", "Grupo": "grupo"},
    },
    "cursos": {
        "nodo": "curso",
        "campos": {"Codigo": "codigo", "Nombre_Cas": "nombre_cas",
                   "Nombre_Val": "nombre_val", "Padre": "padre"},
    },
    "calificaciones": {
        "nodo": "calificacion",
        "campos": {"NIA": "alumno", "Curso": "curso", "Modulo": "contenido",
                   "Nota": "nota_numerica", "Evaluacion": "evaluacion"},
    },
    "contenidos": {
        "nodo": "contenido",
        "campos": {"Curso": "curso", "Modulo": "codigo", "Nombre_Modulo": "nombre_val"},
    },
}


def anonimizar_nia(nia):
    if nia is None:
        return None
    clave = os.environ["NIA_SECRET"].encode()
    return hmac.new(clave, nia.encode(), hashlib.sha256).hexdigest()[:16]


def listar_anios():
    return sorted(d.name for d in DIR_ENTRADA.iterdir() if d.is_dir())


def parsear_xml(anio: str, tabla: str) -> list[dict]:
    raiz = ET.parse(DIR_ENTRADA / anio / f"{tabla}.xml").getroot()
    cfg = CONFIG[tabla]
    registros = []
    for nodo in raiz.iter(cfg["nodo"]):
        reg = {"Anyo": anio}
        for col, attr in cfg["campos"].items():
            reg[col] = nodo.get(attr)
        if "NIA" in reg:
            reg["NIA"] = anonimizar_nia(reg["NIA"])
        registros.append(reg)
    logger.info("%s/%s: %d registros", anio, tabla, len(registros))
    return registros


def guardar(datos: list[dict], tabla: str) -> None:
    DIR_SALIDA.mkdir(parents=True, exist_ok=True)
    ruta = DIR_SALIDA / f"{tabla}_{date.today().isoformat()}.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    logger.info("Guardados %d registros en %s", len(datos), ruta)


if __name__ == "__main__":
    anios = listar_anios()
    for tabla in TABLAS:
        registros = []
        for anio in anios:
            try:
                registros.extend(parsear_xml(anio, tabla))
            except FileNotFoundError:
                logger.warning("No existe %s.xml en %s", tabla, anio)
        guardar(registros, tabla)