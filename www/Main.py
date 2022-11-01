import asyncio

from modules.funciones import cargar_config__, cargar_ruta__, guardar_json__
from playwright.async_api import async_playwright

# Variables
ruta = 'config/url.json'
config = 'config/paginas.json'

# Cargar datos
if __name__ == '__main__':
    r = cargar_ruta__(ruta)
    c = cargar_config__(config)

    iteracion = []

    # iteracion: [paginas, configuracion]
    for i, j in zip(r, c):
        if i.get("pag") == j.get("pag") and i.get("pag") not in iteracion:
            iteracion.append(i.get("pag"))

    # iteracion: [iteracion, configuracion]
    for i, c, p in zip(iteracion, c, r):
        if i == c.get("pag"):
            async def main():
                async with async_playwright() as pw:
                    browser = await pw.chromium.launch(headless=False)
                    page = await browser.new_page()

                    # Abrir la pagina
                    await page.goto(p.get("url"))

                    # Imprimir en consola
                    print("Nombre del sitio:", p.get("nombre"))
                    print("Categoria del sitio:", p.get("categoria"))
                    print("Pagina N°:", p.get("pag"), "\n\n")

                    # Traer el contenido de la pagina
                    contenido = c.get("configuracion")

                    # Pagina 1 Configuracion
                    if p.get("pag") == 1:
                        # Insertar búsqueda
                        await page.type(contenido.get("buscar").get("clase"), contenido.get("buscar").get("text"))
                        # Hace click en el botón de buscar
                        await page.click(contenido.get("buscar").get("click"))

                        # Espera el selector
                        await page.wait_for_selector(contenido.get("selectores").get("inicio"))
                        await asyncio.sleep(2)

                        # Investigar en la pagina
                        enlaces = await page.evaluate("""async () => {
                                    const link = document.querySelectorAll("[class='details'] h2 a");
                                    const linksArray = [];
                                    for (let links of link) {
                                    linksArray.push(links.href);
                                    }
                                    return linksArray;
                                    }""")

                        # Array de enlaces
                        posts = []

                        for enlace in enlaces:
                            # Ingresa a la pagina del enlace actual
                            await page.goto(enlace)
                            await page.wait_for_selector(contenido.get("selectores").get("entrada"))

                            # Obtiene datos del post
                            post = await page.evaluate("""async () => {
                                        const tmp = {};

                                        // Obtiene el titulo
                                        tmp.titulo = document.querySelector(".entry-title").innerText;

                                        // Retorna los datos
                                        return tmp;
                                        }""")

                            posts.append(post)

                        # Guardar los datos en un archivo JSON
                        guardar_json__("data/pagina1.json", posts)

                        # Captura de pantalla
                        await page.screenshot(path="capturas__de__pantalla/__pagina1.png")
                        await asyncio.sleep(2)

                    # Pagina 2 Configuracion
                    if p.get("pag") == 2:
                        # Insertar búsqueda
                        await page.locator(contenido.get("buscar").get("clase")).type(contenido.get("buscar").get("text"))
                        # Hace click en el botón de buscar
                        await page.click(contenido.get("buscar").get("click"))

                        # Captura de pantalla
                        await asyncio.sleep(10)
                        await page.screenshot(path="capturas__de__pantalla/__pagina2.png")
                        await asyncio.sleep(2)

                    # Cerrar el navegador
                    await browser.close()

            asyncio.run(main())
