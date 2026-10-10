
cant_bancos = int(input("Ingrese la cantidad de bancos del aula: "))
while cant_bancos < 0:
    cant_bancos = int(input("No puede ser negativo. Ingrese la cantidad de bancos: "))

cant_alumnos = int(input("Ingrese la cantidad de alumnos inscriptos: "))
while cant_alumnos < 0:
    cant_alumnos = int(input("No puede ser negativo. Ingrese la cantidad de alumnos: "))

if cant_alumnos <= cant_bancos:
    print("Los bancos alcanzan para todos los alumnos.")
else:
    bancos_faltantes = cant_alumnos - cant_bancos
    print(f"Los bancos NO alcanzan. Hay que agregar {bancos_faltantes} banco(s).")