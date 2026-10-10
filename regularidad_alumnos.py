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


def mostrar_estado(alumno):
    """Imprime el promedio, la asistencia y el estado del alumno."""
    promedio = calcular_promedio(alumno["notas"])
    if esta_regular(alumno):
        estado = "REGULAR"
    else:
        estado = "NO REGULAR"
    print(f"{alumno['nombre']} - Promedio: {promedio:.2f} - "
          f"Asistencia: {alumno['asistencia']}% -> {estado}")


def main():
    alumnos = [
        {"nombre": "Juan", "notas": [7, 8, 9, 6], "asistencia": 90},
        {"nombre": "Maria", "notas": [5, 6, 4, 7], "asistencia": 60},
        {"nombre": "Pedro", "notas": [1, 9, 4, 7], "asistencia": 95},
        {"nombre": "Ana", "notas": [6, 5, 7, 8], "asistencia": 85},
    ]

    for alumno in alumnos:
        mostrar_estado(alumno)


if __name__ == "__main__":
    main()