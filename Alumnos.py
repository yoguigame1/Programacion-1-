PROMEDIO_MINIMO = 6
ASISTENCIA_MINIMA = 75


def calcular_promedio(notas):
    """Recibe un arreglo de notas y devuelve su promedio."""
    if len(notas) == 0:
        return 0
    suma = 0
    for nota in notas:
        suma += nota
    return suma / len(notas)


def esta_regular(alumno):
    """Devuelve True si el alumno cumple promedio y asistencia mínimos."""
    cumple_promedio = calcular_promedio(alumno["notas"]) >= PROMEDIO_MINIMO
    cumple_asistencia = alumno["asistencia"] >= ASISTENCIA_MINIMA
    return cumple_promedio and cumple_asistencia


def obtener_motivos(alumno):
    """Devuelve un arreglo con los motivos por los que NO está regular."""
    motivos = []
    if calcular_promedio(alumno["notas"]) < PROMEDIO_MINIMO:
        motivos.append(f"promedio menor a {PROMEDIO_MINIMO}")
    if alumno["asistencia"] < ASISTENCIA_MINIMA:
        motivos.append(f"asistencia menor a {ASISTENCIA_MINIMA}%")
    return motivos


def mostrar_resultado(alumno):
    """Imprime la situación del alumno."""
    promedio = calcular_promedio(alumno["notas"])
    print(f"Alumno: {alumno['nombre']}")
    print(f"  Promedio:   {promedio:.2f}")
    print(f"  Asistencia: {alumno['asistencia']}%")

    if esta_regular(alumno):
        print("  Estado:     REGULAR")
    else:
        motivos = ", ".join(obtener_motivos(alumno))
        print(f"  Estado:     NO REGULAR ({motivos})")
    print()


def main():
    alumnos = [
        {"nombre": "Juan", "notas": [7, 8, 9, 6], "asistencia": 90},
        {"nombre": "Maria", "notas": [5, 6, 4, 7], "asistencia": 60},
        {"nombre": "Pedro", "notas": [1, 9, 4, 7], "asistencia": 95},
        {"nombre": "Ana", "notas": [6, 5, 7, 8], "asistencia": 85},
    ]

    cantidad_regulares = 0
    for alumno in alumnos:
        mostrar_resultado(alumno)
        if esta_regular(alumno):
            cantidad_regulares += 1

    print(f"Resumen: {cantidad_regulares} de {len(alumnos)} alumnos están regulares.")


if __name__ == "__main__":
    main()