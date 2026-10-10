"""Primer avance - AE2 Programación I (buffet).
Carga del catálogo en un diccionario, controlando que no se repitan códigos."""


def cargar_catalogo(productos):
    """Recibe una lista de (código, nombre, precio) y devuelve el catálogo.

    Si un código aparece más de una vez, se informa y se conserva el primero.
    """
    catalogo = {}
    for codigo, nombre, precio in productos:
        if codigo in catalogo:
            print(f"Error: el código {codigo} está repetido, se ignora '{nombre}'.")
        else:
            catalogo[codigo] = {"nombre": nombre, "precio": precio}
    return catalogo


PRODUCTOS = [
    (101, "Café con leche", 1500),
    (102, "Medialuna", 700),
    (103, "Sándwich de miga", 1800),
    (104, "Agua mineral 500 ml", 1000),
    (105, "Empanada", 1200),
    (106, "Chipá (100 g)", 1300),
    (101, "Alfajor", 900),  # código repetido a propósito (caso límite)
]

if __name__ == "__main__":
    catalogo = cargar_catalogo(PRODUCTOS)
    print(f"Productos cargados: {len(catalogo)}")
    for codigo in sorted(catalogo):
        print(f"{codigo} - {catalogo[codigo]['nombre']} (${catalogo[codigo]['precio']})")
