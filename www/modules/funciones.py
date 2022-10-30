import asyncio
import json

from playwright.async_api import async_playwright


def cargar_ruta__(ruta):
    with open(ruta) as contenido:
        paginas = json.load(contenido)
        # print("Paginas: \n", paginas, "\n")
    return paginas


def cargar_config__(config):
    with open(config) as configuracion:
        configuracion = json.load(configuracion)
        # print("Configuracion: \n", configuracion, "\n\n")
    return configuracion


def guardar_json__(nombre, contenido):
    with open(nombre, "w") as archivo:
        json.dump(contenido, archivo, indent=4)
