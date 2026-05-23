"""Punto de entrada del juego Cazador de Contrasenas."""

from cazador import ErrorInesperado, iniciar_entorno_grafico


if __name__ == "__main__":
    try:
        iniciar_entorno_grafico()
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario.")
    except ErrorInesperado as error:
        print(error)
