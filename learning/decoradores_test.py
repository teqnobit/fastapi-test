def decorador(funcion):
    def wrapper():
        print("Antes de llamar a la función...")
        funcion()
        print("Después de llamar a la función...")
    return wrapper

@decorador
def saludar():
    print("¡Hola!")

saludar()
