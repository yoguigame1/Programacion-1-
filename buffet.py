DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

# Datos del cuaderno: {número de día (0 = lunes): {código: unidades}}
DATOS_CUADERNO = {
    0: {101: 30, 102: 40, 103: 10, 104: 20, 105: 15},
    1: {101: 25, 102: 38, 103: 12, 104: 22},
    2: {101: 28, 102: 45, 103: 8, 104: 18, 105: 20},
    3: {101: 35, 102: 50, 103: 15, 104: 25, 105: 18},
    4: {101: 20, 102: 30, 103: 9, 104: 30, 105: 25},
}


def inicializar_catalogo():
    """Devuelve el catálogo inicial de productos."""
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
    if codigo not in catalogo:
        print("Error: el producto no existe en el catálogo.")
        return

    cantidad = pedir_entero("Ingrese cantidad vendida: ", 1)

    idx_prod = codigos.index(codigo)  # de código a columna de la matriz
    ventas[dia][idx_prod] += cantidad
    print(f"-> Venta registrada: {cantidad} x {catalogo[codigo]['nombre']} el {DIAS[dia]}.")


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
    """Precarga en la matriz los datos del cuaderno."""
    for dia, productos in DATOS_CUADERNO.items():
        for codigo, unidades in productos.items():
            ventas[dia][codigos.index(codigo)] = unidades
    print("-> Datos del cuaderno cargados correctamente.")


def main():
    catalogo = inicializar_catalogo()
    codigos = sorted(catalogo.keys())
    ventas = inicializar_matriz_ventas(len(DIAS), len(codigos))

    while True:
        print("\n=== MENÚ BUFFET FACULTAD ===")
        print("1. Registrar una venta")
        print("2. Ver informes semanales")
        print("3. Cargar datos del cuaderno (prueba)")
        print("4. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_venta(ventas, catalogo, codigos)
        elif opcion == "2":
            mostrar_informes(ventas, catalogo, codigos)
        elif opcion == "3":
            cargar_datos_cuaderno(ventas, codigos)
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()