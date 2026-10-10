
edad = int(input("Ingrese su edad: "))
while edad < 0:
    edad = int(input("La edad no puede ser negativa. Ingrese su edad: "))

sexo = input("Ingrese su sexo (M = masculino, F = femenino): ").strip().upper()
while sexo != "M" and sexo != "F":
    sexo = input("Sexo inválido. Ingrese M o F: ").strip().upper()

if sexo == "M":
    descripcion = "hombre"
else:
    descripcion = "mujer"

if edad >= 16:
    print(f"Usted es {descripcion} y puede votar.")
else:
    print(f"Usted es {descripcion} y no puede votar.")

