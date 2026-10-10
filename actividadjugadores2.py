ARCHIVO = "jugadores.txt"
SEPARADOR = ";"


def pedir_texto(mensaje):
    """Pide un texto: no puede estar vacío ni contener el separador del archivo."""
    texto = input(mensaje).strip()
    while texto == "" or SEPARADOR in texto:
        print(f"Error: no puede estar vacío ni contener '{SEPARADOR}'.")
        texto = input(mensaje).strip()
    return texto


def pedir_cantidad(mensaje):
    """Pide un número entero mayor a 0."""
    texto = input(mensaje).strip()
    while not texto.isdigit() or int(texto) < 1:
        print("Error: ingrese un número entero mayor a 0.")
        texto = input(mensaje).strip()
    return int(texto)


def leer_jugadores():
    """Lee el archivo y devuelve una lista de diccionarios {nombre, categoria}."""
    jugadores = []
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split(SEPARADOR)
                if len(partes) == 2:
                    jugadores.append({"nombre": partes[0], "categoria": partes[1]})
    except FileNotFoundError:
        pass  # si el archivo no existe todavía, la lista queda vacía
    return jugadores


def guardar_jugadores(jugadores):
    """Reescribe el archivo completo con la lista de jugadores."""
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        for jugador in jugadores:
            archivo.write(jugador["nombre"] + SEPARADOR + jugador["categoria"] + "\n")


def buscar_por_nombre(nombre, jugadores):
    """Devuelve el jugador con ese nombre o None si no está."""
    for jugador in jugadores:
        if jugador["nombre"].lower() == nombre.lower():
            return jugador
    return None


def pedir_datos_jugador(existentes):
    """Pide nombre (que no se repita) y categoría de un jugador."""
    nombre = pedir_texto("Nombre del jugador: ")
    while buscar_por_nombre(nombre, existentes) is not None:
        print("Error: ya existe un jugador con ese nombre.")
        nombre = pedir_texto("Nombre del jugador: ")
    categoria = pedir_texto("Categoría (por ejemplo 4ª, 5ª o 6ª): ")
    return {"nombre": nombre, "categoria": categoria}


def cargar_jugadores():
    """Alta de una lista nueva de jugadores (reemplaza el contenido del archivo)."""
    if len(leer_jugadores()) > 0:
        respuesta = input("Ya hay jugadores guardados. ¿Desea reemplazarlos? (s/n): ").strip().lower()
        if respuesta != "s":
            print("Operación cancelada.")
            return

    cantidad = pedir_cantidad("¿Cuántos jugadores va a cargar? ")
    jugadores = []
    for i in range(cantidad):
        print(f"\nJugador {i + 1}")
        jugadores.append(pedir_datos_jugador(jugadores))

    guardar_jugadores(jugadores)
    print("Jugadores guardados correctamente.")


def agregar_jugador():
    """Alta de un solo jugador (se agrega al final del archivo)."""
    jugadores = leer_jugadores()
    nuevo = pedir_datos_jugador(jugadores)

    with open(ARCHIVO, "a", encoding="utf-8") as archivo:
        archivo.write(nuevo["nombre"] + SEPARADOR + nuevo["categoria"] + "\n")

    print("Jugador agregado correctamente.")


def mostrar_jugadores():
    """Consulta: muestra todos los jugadores."""
    jugadores = leer_jugadores()

    print("\nLISTA DE JUGADORES")
    if len(jugadores) == 0:
        print("No hay jugadores inscriptos.")
    for jugador in jugadores:
        print(f"Nombre: {jugador['nombre']} - Categoría: {jugador['categoria']}")


def buscar_jugador():
    """Consulta: busca un jugador por nombre."""
    nombre = input("Ingrese el nombre del jugador que busca: ").strip()
    jugador = buscar_por_nombre(nombre, leer_jugadores())

    if jugador is None:
        print("El jugador no está inscripto.")
    else:
        print(f"Jugador: {jugador['nombre']}")
        print(f"Categoría: {jugador['categoria']}")


def eliminar_jugador():
    """Baja: elimina un jugador por nombre."""
    nombre = input("Ingrese el nombre del jugador que desea eliminar: ").strip()
    jugadores = leer_jugadores()
    jugador = buscar_por_nombre(nombre, jugadores)

    if jugador is None:
        print("El jugador no está inscripto.")
    else:
        jugadores.remove(jugador)
        guardar_jugadores(jugadores)
        print("Jugador eliminado correctamente.")


def main():
    opcion = ""

    while opcion != "6":
        print("\n--- TORNEO DE PÁDEL ---")
        print("1. Cargar jugadores")
        print("2. Agregar un jugador")
        print("3. Mostrar jugadores")
        print("4. Buscar jugador")
        print("5. Eliminar jugador")
        print("6. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            cargar_jugadores()
        elif opcion == "2":
            agregar_jugador()
        elif opcion == "3":
            mostrar_jugadores()
        elif opcion == "4":
            buscar_jugador()
        elif opcion == "5":
            eliminar_jugador()
        elif opcion == "6":
            print("Programa finalizado.")
        else:
            print("Opción incorrecta.")


if __name__ == "__main__":
    main()