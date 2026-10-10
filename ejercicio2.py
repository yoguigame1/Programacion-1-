numero1 = int(input("Ingrese el primer número: "))
numero2 = int(input("Ingrese el segundo número: "))
numero3 = int(input("Ingrese el tercer número: "))

if numero1 == numero2 == numero3:
    print("Los tres números son iguales:", numero1)
# Se usa >= para que también funcione cuando hay números repetidos
elif numero1 >= numero2 and numero1 >= numero3:
    print("El 1er número es el mayor:", numero1)
elif numero2 >= numero1 and numero2 >= numero3:
    print("El 2do número es el mayor:", numero2)
else:
    print("El 3er número es el mayor:", numero3)