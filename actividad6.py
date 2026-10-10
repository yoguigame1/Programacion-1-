usuarios_registrados = {
    "usuario": "contraseña",
    "admin": "clave",
}

INTENTOS_MAXIMOS = 3
intentos = 0
acceso = False

while intentos < INTENTOS_MAXIMOS and not acceso:
    usuario = input("Ingrese su usuario: ").strip()
    clave = input("Ingrese su contraseña: ").strip()
    intentos += 1

    if not usuario.isalpha() or not clave.isalpha():
        print("Error: el usuario y la contraseña deben estar formados solo por letras.")
    elif usuario in usuarios_registrados and usuarios_registrados[usuario] == clave:
        acceso = True
    else:
        print("Usuario o contraseña incorrectos.")

    if not acceso and intentos < INTENTOS_MAXIMOS:
        print(f"Le quedan {INTENTOS_MAXIMOS - intentos} intento(s).\n")

if acceso:
    print(f"Inicio de sesión exitoso. ¡Bienvenido, {usuario}!")
else:
    print("Acceso bloqueado: superó la cantidad de intentos permitidos.")