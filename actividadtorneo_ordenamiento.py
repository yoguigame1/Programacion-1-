import json
import os

ARCHIVO_INSCRIPTOS = "inscriptos.json"
ARCHIVO_PAREJAS = "parejas.json"


def pedir_texto(mensaje):
    texto = input(mensaje).strip()
    while texto == "":
        print("Error: no puede quedar vacío.")
        texto = input(mensaje).strip()
    return texto


def pedir_cantidad_jugadores():
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
    parejas = []
    disponibles = jugadores.copy()

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


def guardar_json(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def cargar_json(archivo):
    if not os.path.exists(archivo):
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)


def mostrar_alfabetico(jugadores):
    ordenados = jugadores.copy()
    comparaciones = 0
    intercambios = 0

    for i in range(len(ordenados) - 1):
        menor = i
        for j in range(i + 1, len(ordenados)):
            comparaciones += 1
            if ordenados[j]["nombre"].lower() < ordenados[menor]["nombre"].lower():
                menor = j
        if menor != i:
            auxiliar = ordenados[i]
            ordenados[i] = ordenados[menor]
            ordenados[menor] = auxiliar
            intercambios += 1

    print("\nInscriptos en orden alfabético:")
    for jugador in ordenados:
        print(f"  {jugador['nombre']} (Categoría: {jugador['categoria']})")
    print(f"\nSelección -> Comparaciones: {comparaciones} | Intercambios: {intercambios}")


def mostrar_por_categoria(jugadores):
    ordenados = jugadores.copy()
    comparaciones = 0
    intercambios = 0

    for i in range(len(ordenados) - 1):
        for j in range(len(ordenados) - 1 - i):
            comparaciones += 1
            jugador1 = ordenados[j]
            jugador2 = ordenados[j + 1]
            if jugador1["categoria"] > jugador2["categoria"] or (
                jugador1["categoria"] == jugador2["categoria"]
                and jugador1["nombre"].lower() > jugador2["nombre"].lower()
            ):
                ordenados[j] = jugador2
                ordenados[j + 1] = jugador1
                intercambios += 1

    categoria = ""
    for jugador in ordenados:
        if jugador["categoria"] != categoria:
            categoria = jugador["categoria"]
            print(f"\nCategoría {categoria}:")
        print(f"  {jugador['nombre']}")
    print(f"\nBurbuja -> Comparaciones: {comparaciones} | Intercambios: {intercambios}")


def cargar_puntos(parejas):
    if len(parejas) == 0:
        print("Todavía no hay parejas.")
        return

    print("\nParejas:")
    for i, pareja in enumerate(parejas):
        print(f"  {i + 1}. {pareja['nombre']} ({pareja['puntos']} puntos)")

    while True:
        texto = input("Número de la pareja: ").strip()
        if not texto.isdigit():
            print("Error: ingrese un número entero.")
        elif int(texto) < 1 or int(texto) > len(parejas):
            print("Error: elija una pareja de la lista.")
        else:
            break
    indice = int(texto) - 1

    while True:
        texto = input("Puntos que gana: ").strip()
        if texto.isdigit():
            break
        print("Error: ingrese un número entero.")
    parejas[indice]["puntos"] += int(texto)


def mostrar_posiciones(parejas):
    ordenadas = parejas.copy()

    for i in range(len(ordenadas) - 1):
        mayor = i
        for j in range(i + 1, len(ordenadas)):
            if ordenadas[j]["puntos"] > ordenadas[mayor]["puntos"]:
                mayor = j
        auxiliar = ordenadas[i]
        ordenadas[i] = ordenadas[mayor]
        ordenadas[mayor] = auxiliar

    print("\nTabla de posiciones:")
    print("Puesto | Pareja | Puntos")
    for i, pareja in enumerate(ordenadas):
        print(f"{i + 1} | {pareja['nombre']} | {pareja['puntos']}")


def main():
    jugadores = cargar_json(ARCHIVO_INSCRIPTOS)
    parejas = cargar_json(ARCHIVO_PAREJAS)

    opcion = ""
    while opcion != "0":
        print("\n=== TORNEO ===")
        print("1. Crear un torneo nuevo")
        print("2. Inscriptos en orden alfabético (Selección)")
        print("3. Jugadores por categoría (Burbuja)")
        print("4. Cargar puntos a una pareja")
        print("5. Tabla de posiciones")
        print("0. Salir")
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            print("=== CREAR UN TORNEO NUEVO ===")
            jugadores = cargar_jugadores()
            parejas = armar_parejas(jugadores)
            mostrar_torneo(jugadores, parejas)
            for pareja in parejas:
                pareja["puntos"] = 0
            guardar_json(ARCHIVO_INSCRIPTOS, jugadores)
            guardar_json(ARCHIVO_PAREJAS, parejas)
        elif opcion == "2":
            mostrar_alfabetico(jugadores)
        elif opcion == "3":
            mostrar_por_categoria(jugadores)
        elif opcion == "4":
            cargar_puntos(parejas)
            guardar_json(ARCHIVO_PAREJAS, parejas)
        elif opcion == "5":
            mostrar_posiciones(parejas)
        elif opcion != "0":
            print("Error: opción no válida.")


if __name__ == "__main__":
    main()
