"""Punto de entrada del juego Cazador de Contrasenas."""

from cazador import ErrorInesperado, JuegoCazador


if __name__ == "__main__":
    try:
        juego = JuegoCazador()
        juego.mostrar_menu_principal()
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario.")
    except ErrorInesperado as error:
        print(error)
