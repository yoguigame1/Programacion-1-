import json

ARCHIVO = "alumnos.json"
PROMEDIO_MINIMO = 6
ASISTENCIA_MINIMA = 75


def calcular_promedio(notas):
    """Recibe un arreglo de notas y devuelve su promedio."""
    if len(notas) == 0:
        return 0
    return sum(notas) / len(notas)


def esta_regular(alumno):
    """Devuelve True si el alumno cumple con el promedio y la asistencia mínimos."""
    promedio = calcular_promedio(alumno["notas"])
    return promedio >= PROMEDIO_MINIMO and alumno["asistencia"] >= ASISTENCIA_MINIMA


def guardar_alumnos(alumnos):
    """Guarda la lista de alumnos en el archivo JSON."""
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(alumnos, archivo, ensure_ascii=False, indent=4)


def leer_alumnos():
    """Lee la lista de alumnos desde el archivo JSON."""
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print("Todavía no hay alumnos guardados.")
        return []


def mostrar_estado(alumno):
    """Imprime el promedio, la asistencia y el estado del alumno."""
    promedio = calcular_promedio(alumno["notas"])
    estado = "REGULAR" if esta_regular(alumno) else "NO REGULAR"
    print(f"{alumno['nombre']} - Promedio: {promedio:.2f} - "
          f"Asistencia: {alumno['asistencia']}% -> {estado}")


def main():
    datos_alumnos = [
        {"nombre": "Juan", "notas": [7, 8, 9, 6], "asistencia": 90},
        {"nombre": "Maria", "notas": [5, 6, 4, 7], "asistencia": 60},
        {"nombre": "Pedro", "notas": [1, 9, 4, 7], "asistencia": 95},
        {"nombre": "Ana", "notas": [6, 5, 7, 8], "asistencia": 85},
    ]

    guardar_alumnos(datos_alumnos)
    alumnos = leer_alumnos()

    for alumno in alumnos:
        mostrar_estado(alumno)


if __name__ == "__main__":
    main()