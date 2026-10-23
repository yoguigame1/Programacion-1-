DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

ARCHIVO_PRODUCTOS = "productos.txt"  # archivo maestro: código;nombre;precio
ARCHIVO_VENTAS = "ventas.txt"        # archivo de movimientos: día;código;unidades

# Datos del cuaderno: {número de día (0 = lunes): {código: unidades}}
DATOS_CUADERNO = {
    0: {101: 30, 102: 40, 103: 10, 104: 20, 105: 15},
    1: {101: 25, 102: 38, 103: 12, 104: 22},
    2: {101: 28, 102: 45, 103: 8, 104: 18, 105: 20},
    3: {101: 35, 102: 50, 103: 15, 104: 25, 105: 18},
    4: {101: 20, 102: 30, 103: 9, 104: 30, 105: 25},
}


# ------------------------------------------------------------------
# FUNCIONES (devuelven un valor)
# ------------------------------------------------------------------
def inicializar_catalogo():
    """Devuelve el catálogo inicial de productos (se usa el primer día)."""
    return {
        101: {"nombre": "Café con leche", "precio": 1500},
        102: {"nombre": "Medialuna", "precio": 700},
        103: {"nombre": "Sándwich de miga", "precio": 1800},
        104: {"nombre": "Agua mineral 500 ml", "precio": 1000},
        105: {"nombre": "Empanada", "precio": 1200},
        106: {"nombre": "Chipá (100 g)", "precio": 1300},
    }


def inicializar_matriz_ventas(num_dias, num_productos):
    """Crea una matriz de ceros: una fila por día y una columna por producto."""
    return [[0 for _ in range(num_productos)] for _ in range(num_dias)]


def pedir_entero(mensaje, minimo, maximo=None):
    """Pide un entero por teclado y repite hasta que sea válido."""
    while True:
        texto = input(mensaje)
        try:
            numero = int(texto)
        except ValueError:
            print("Error: debe ingresar un número entero.")
            continue

        if numero < minimo:
            print(f"Error: el valor debe ser mayor o igual a {minimo}.")
        elif maximo is not None and numero > maximo:
            print(f"Error: el valor debe ser menor o igual a {maximo}.")
        else:
            return numero


def buscar_indice(codigos, codigo):
    """Búsqueda secuencial: devuelve la posición del código o -1 si no está.
    El recorrido termina antes de llegar al final apenas lo encuentra (break)."""
    posicion = -1
    for i in range(len(codigos)):
        if codigos[i] == codigo:
            posicion = i
            break
    return posicion


def calcular_unidades_por_producto(ventas, idx_prod):
    """Total de unidades vendidas de un producto en toda la semana."""
    total = 0
    for dia in range(len(ventas)):
        total += ventas[dia][idx_prod]
    return total


def calcular_recaudacion_dia(ventas, catalogo, codigos, dia):
    """Recaudación total de un día."""
    recaudacion = 0
    for idx_prod, codigo in enumerate(codigos):
        recaudacion += ventas[dia][idx_prod] * catalogo[codigo]["precio"]
    return recaudacion


def leer_productos():
    """Lee el archivo de productos. Devuelve (catalogo, codigos).
    Si el archivo no existe, devuelve un catálogo y una lista vacíos."""
    catalogo = {}
    codigos = []
    try:
        with open(ARCHIVO_PRODUCTOS, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if linea == "":
                    continue

                partes = linea.split(";")
                if len(partes) != 3:
                    print(f"Aviso: línea {numero_linea} de {ARCHIVO_PRODUCTOS} ignorada (formato incorrecto).")
                    continue

                try:
                    codigo = int(partes[0])
                    precio = int(partes[2])
                except ValueError:
                    print(f"Aviso: línea {numero_linea} de {ARCHIVO_PRODUCTOS} ignorada (código o precio no numérico).")
                    continue

                nombre = partes[1].strip()
                if nombre == "" or precio < 0:
                    print(f"Aviso: línea {numero_linea} de {ARCHIVO_PRODUCTOS} ignorada (nombre vacío o precio negativo).")
                    continue

                if buscar_indice(codigos, codigo) != -1:
                    print(f"Aviso: línea {numero_linea} de {ARCHIVO_PRODUCTOS} ignorada (código {codigo} duplicado).")
                    continue

                catalogo[codigo] = {"nombre": nombre, "precio": precio}
                codigos.append(codigo)
    except FileNotFoundError:
        pass  # primer uso: todavía no hay catálogo guardado
    return catalogo, codigos


# ------------------------------------------------------------------
# PROCEDIMIENTOS (no devuelven nada)
# ------------------------------------------------------------------
def guardar_productos(catalogo, codigos):
    """Escribe el catálogo completo en el archivo de productos."""
    try:
        with open(ARCHIVO_PRODUCTOS, "w", encoding="utf-8") as archivo:
            for codigo in codigos:
                producto = catalogo[codigo]
                archivo.write(f"{codigo};{producto['nombre']};{producto['precio']}\n")
    except OSError:
        print("Error: no se pudo guardar el archivo de productos.")


def guardar_ventas(ventas, codigos):
    """Escribe en el archivo una línea por cada celda de la matriz con ventas."""
    try:
        with open(ARCHIVO_VENTAS, "w", encoding="utf-8") as archivo:
            for dia in range(len(ventas)):
                for idx_prod in range(len(codigos)):
                    if ventas[dia][idx_prod] > 0:
                        archivo.write(f"{dia + 1};{codigos[idx_prod]};{ventas[dia][idx_prod]}\n")
    except OSError:
        print("Error: no se pudo guardar el archivo de ventas.")


def leer_ventas(ventas, codigos):
    """Carga en la matriz las ventas guardadas en el archivo (si existe)."""
    try:
        with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if linea == "":
                    continue

                partes = linea.split(";")
                if len(partes) != 3:
                    print(f"Aviso: línea {numero_linea} de {ARCHIVO_VENTAS} ignorada (formato incorrecto).")
                    continue

                try:
                    dia = int(partes[0]) - 1
                    codigo = int(partes[1])
                    cantidad = int(partes[2])
                except ValueError:
                    print(f"Aviso: línea {numero_linea} de {ARCHIVO_VENTAS} ignorada (datos no numéricos).")
                    continue

                idx_prod = buscar_indice(codigos, codigo)
                if dia < 0 or dia >= len(DIAS) or idx_prod == -1 or cantidad <= 0:
                    print(f"Aviso: línea {numero_linea} de {ARCHIVO_VENTAS} ignorada (datos fuera de rango).")
                    continue

                # Si hubiera dos líneas del mismo día y producto, se suman
                ventas[dia][idx_prod] += cantidad
        print("-> Ventas anteriores cargadas desde el archivo.")
    except FileNotFoundError:
        print("-> No hay ventas guardadas todavía (primer uso).")


def agregar_producto(catalogo, codigos, ventas):
    """Carga un producto nuevo al catálogo, sin permitir códigos repetidos."""
    print("\n--- CARGAR PRODUCTO ---")
    codigo = pedir_entero("Ingrese código del producto: ", 1)
    if buscar_indice(codigos, codigo) != -1:
        print(f"Error: ya existe un producto con el código {codigo} ({catalogo[codigo]['nombre']}).")
        return

    nombre = input("Ingrese nombre del producto: ").strip()
    if nombre == "" or ";" in nombre:
        print("Error: el nombre no puede estar vacío ni contener ';'.")
        return

    precio = pedir_entero("Ingrese precio ($): ", 1)

    catalogo[codigo] = {"nombre": nombre, "precio": precio}
    codigos.append(codigo)
    for fila in ventas:
        fila.append(0)  # el producto nuevo es una columna nueva (con ceros) en cada día

    guardar_productos(catalogo, codigos)
    print(f"-> Producto cargado: {codigo} - {nombre} (${precio}).")


def registrar_venta(ventas, catalogo, codigos):
    """Registra una venta pidiendo día, producto y cantidad."""
    print("\n--- REGISTRAR VENTA ---")
    for i, nombre_dia in enumerate(DIAS):
        print(f"{i + 1}: {nombre_dia}")
    dia = pedir_entero("Ingrese día (1-5): ", 1, len(DIAS)) - 1

    print("Productos disponibles:")
    for codigo in codigos:
        print(f"  {codigo} - {catalogo[codigo]['nombre']} (${catalogo[codigo]['precio']})")
    codigo = pedir_entero("Ingrese código del producto: ", 0)
    idx_prod = buscar_indice(codigos, codigo)  # de código a columna de la matriz
    if idx_prod == -1:
        print("Error: el producto no existe en el catálogo.")
        return

    cantidad = pedir_entero("Ingrese cantidad vendida: ", 1)

    ventas[dia][idx_prod] += cantidad  # dos ventas del mismo producto y día se acumulan
    guardar_ventas(ventas, codigos)    # se guarda después de cada venta para no perder nada
    print(f"-> Venta registrada: {cantidad} x {catalogo[codigo]['nombre']} el {DIAS[dia]}.")


def mostrar_informes(ventas, catalogo, codigos):
    """Muestra todos los informes semanales."""
    print("\n==================================================")
    print("        INFORMES DE VENTAS DE LA SEMANA")
    print("==================================================")

    # 1. Unidades vendidas por producto
    print("\n1. UNIDADES VENDIDAS POR PRODUCTO:")
    totales_por_prod = []
    for idx, codigo in enumerate(codigos):
        total_prod = calcular_unidades_por_producto(ventas, idx)
        totales_por_prod.append(total_prod)
        print(f" - {catalogo[codigo]['nombre']}: {total_prod} unidades")

    # 2. Recaudación por día
    print("\n2. RECAUDACIÓN POR DÍA:")
    recaudaciones_dias = []
    recaudacion_total = 0
    for d in range(len(DIAS)):
        rec_dia = calcular_recaudacion_dia(ventas, catalogo, codigos, d)
        recaudaciones_dias.append(rec_dia)
        recaudacion_total += rec_dia
        print(f" - {DIAS[d]}: ${rec_dia:,.2f}")

    # 3. Producto más vendido y día de mayor recaudación
    max_unidades = max(totales_por_prod)
    if max_unidades > 0:
        mas_vendidos = [catalogo[codigos[i]]["nombre"]
                        for i, cant in enumerate(totales_por_prod) if cant == max_unidades]
        print(f"\n3. PRODUCTO(S) MÁS VENDIDO(S): {', '.join(mas_vendidos)} ({max_unidades} unidades)")
    else:
        print("\n3. PRODUCTO MÁS VENDIDO: no se registraron ventas.")

    max_rec = max(recaudaciones_dias)
    if max_rec > 0:
        dias_max = [DIAS[i] for i, rec in enumerate(recaudaciones_dias) if rec == max_rec]
        print(f"   DÍA DE MAYOR RECAUDACIÓN: {', '.join(dias_max)} (${max_rec:,.2f})")
    else:
        print("   DÍA DE MAYOR RECAUDACIÓN: no hubo ingresos.")

    # 4. Productos sin ventas
    print("\n4. PRODUCTOS SIN VENTAS:")
    sin_ventas = [catalogo[codigos[i]]["nombre"]
                  for i, cant in enumerate(totales_por_prod) if cant == 0]
    if sin_ventas:
        for nombre in sin_ventas:
            print(f" - {nombre}")
    else:
        print(" - Todos los productos registraron al menos una venta.")

    # 5. Recaudación total
    print(f"\n5. RECAUDACIÓN TOTAL DE LA SEMANA: ${recaudacion_total:,.2f}")
    print("==================================================\n")


def cargar_datos_cuaderno(ventas, codigos):
    """Reemplaza las ventas por los datos del cuaderno (prueba con datos normales)."""
    respuesta = input("Esto reemplaza las ventas guardadas. ¿Continuar? (s/n): ").strip().lower()
    if respuesta != "s":
        print("-> Operación cancelada.")
        return

    # Primero se vacía la matriz para que la prueba parta de cero
    for dia in range(len(ventas)):
        for idx_prod in range(len(codigos)):
            ventas[dia][idx_prod] = 0

    for dia, productos in DATOS_CUADERNO.items():
        for codigo, unidades in productos.items():
            idx_prod = buscar_indice(codigos, codigo)
            if idx_prod != -1:
                ventas[dia][idx_prod] = unidades

    guardar_ventas(ventas, codigos)
    print("-> Datos del cuaderno cargados correctamente.")


def main():
    # Al arrancar se recuperan los productos y las ventas guardados
    catalogo, codigos = leer_productos()
    if len(codigos) == 0:
        print("-> No hay catálogo guardado (primer uso). Se carga el catálogo inicial.")
        catalogo = inicializar_catalogo()
        codigos = sorted(catalogo.keys())
        guardar_productos(catalogo, codigos)
    else:
        print(f"-> Catálogo cargado desde el archivo: {len(codigos)} productos.")

    ventas = inicializar_matriz_ventas(len(DIAS), len(codigos))
    leer_ventas(ventas, codigos)

    while True:
        print("\n=== MENÚ BUFFET FACULTAD ===")
        print("1. Cargar un producto nuevo")
        print("2. Registrar una venta")
        print("3. Ver informes semanales")
        print("4. Cargar datos del cuaderno (prueba)")
        print("5. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_producto(catalogo, codigos, ventas)
        elif opcion == "2":
            registrar_venta(ventas, catalogo, codigos)
        elif opcion == "3":
            mostrar_informes(ventas, catalogo, codigos)
        elif opcion == "4":
            cargar_datos_cuaderno(ventas, codigos)
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
