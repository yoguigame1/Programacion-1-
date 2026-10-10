import json

ARCHIVO_JUGADORES = "jugadores.json"
ARCHIVO_PAREJAS = "parejas.json"


def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


def leer_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def pedir_texto(mensaje):
    """Pide un texto por teclado y repite hasta que no esté vacío."""
    texto = input(mensaje).strip()
    while texto == "":
        print("Error: no puede quedar vacío.")
        texto = input(mensaje).strip()
    return texto


def pedir_cantidad_jugadores():
    """Pide la cantidad de jugadores: debe ser par y de al menos 2."""
    while True:
        texto = input("¿Cuántos jugadores van a participar en el torneo? ").strip()
        if not texto.isdigit():
            print("Error: ingrese un número entero.")
        elif int(texto) < 2 or int(texto) % 2 != 0:
            print("Error: la cantidad debe ser par (mínimo 2), porque cada pareja lleva exactamente 2 jugadores.")
        else:
            return int(texto)


def nombre_jugador_repetido(nombre, jugadores):
    for jugador in jugadores:
        if jugador["nombre"].lower() == nombre.lower():
            return True
    return False


def nombre_pareja_repetido(nombre, parejas):
    for pareja in parejas:
        if pareja["nombre"].lower() == nombre.lower():
            return True
    return False


def cargar_jugadores():
    """a) Registra a los jugadores uno por uno (nombre y categoría)."""
    jugadores = []
    cantidad = pedir_cantidad_jugadores()

    for i in range(cantidad):
        print(f"\nJugador {i + 1}")
        nombre = pedir_texto("  Nombre: ")
        while nombre_jugador_repetido(nombre, jugadores):
            print("  Error: ya existe un jugador con ese nombre.")
            nombre = pedir_texto("  Nombre: ")
        categoria = pedir_texto("  Categoría (por ejemplo 4ª, 5ª o 6ª): ")
        jugadores.append({"nombre": nombre, "categoria": categoria})

    return jugadores


def leer_indices(entrada, cantidad):
    """Convierte '1,2' en [0, 1]. Devuelve None si la entrada no es válida."""
    partes = entrada.split(",")
    if len(partes) != 2:
        return None

    indices = []
    for parte in partes:
        parte = parte.strip()
        if not parte.isdigit():
            return None
        indice = int(parte) - 1
        if indice < 0 or indice >= cantidad:
            return None
        indices.append(indice)

    if indices[0] == indices[1]:
        return None
    return indices


def armar_parejas(jugadores):
    """b) Forma las parejas eligiendo 2 jugadores distintos entre los inscriptos."""
    parejas = []
    disponibles = jugadores.copy()  # jugadores que todavía no tienen pareja

    for i in range(len(jugadores) // 2):
        print(f"\n--- Pareja {i + 1} ---")
        nombre_pareja = pedir_texto("Nombre de la pareja (por ejemplo, Los Tanos): ")
        while nombre_pareja_repetido(nombre_pareja, parejas):
            print("Error: ya existe una pareja con ese nombre.")
            nombre_pareja = pedir_texto("Nombre de la pareja: ")

        while True:
            print("Jugadores disponibles:")
            for j, jugador in enumerate(disponibles):
                print(f"  {j + 1}. {jugador['nombre']} (Categoría: {jugador['categoria']})")

            entrada = input("Ingrese los números de los 2 jugadores separados por coma (ej: 1,2): ")
            indices = leer_indices(entrada, len(disponibles))
            if indices is None:
                print("Error: debe elegir exactamente 2 jugadores distintos de la lista.\n")
            else:
                break

        jugador1 = disponibles[indices[0]]
        jugador2 = disponibles[indices[1]]
        parejas.append({"nombre": nombre_pareja, "jugadores": [jugador1, jugador2]})
        disponibles.remove(jugador1)
        disponibles.remove(jugador2)

    return parejas


def mostrar_torneo(jugadores, parejas):
    print("\nJugadores inscriptos:")
    for jugador in jugadores:
        print(f"  {jugador['nombre']} (Categoría: {jugador['categoria']})")

    print("\nParejas formadas:")
    for pareja in parejas:
        print(f"  Pareja: {pareja['nombre']}")
        print(f"  Jugadores: {pareja['jugadores'][0]['nombre']} y {pareja['jugadores'][1]['nombre']}")
        print("  -----")


def main():
    print("=== TORNEO DE PÁDEL ===")
    print("1. Crear un torneo nuevo")
    print("2. Consultar el último torneo guardado")
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        jugadores = cargar_jugadores()
        guardar_json(ARCHIVO_JUGADORES, jugadores)
        parejas = armar_parejas(jugadores)
        guardar_json(ARCHIVO_PAREJAS, parejas)
        print("\nTorneo guardado correctamente.")
    elif opcion == "2":
        jugadores = leer_json(ARCHIVO_JUGADORES)
        parejas = leer_json(ARCHIVO_PAREJAS)
        if not jugadores and not parejas:
            print("Todavía no hay un torneo guardado.")
            return
    else:
        print("Opción no válida.")
        return

    mostrar_torneo(jugadores, parejas)


if __name__ == "__main__":
    main()