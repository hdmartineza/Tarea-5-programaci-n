"""Clase JuegoCazador: controla el flujo completo del juego."""

from cazador.cofres import FabricaCofres
from cazador.contrasena import Contrasena
from cazador.excepciones import (
    ErrorContrasenaInvalida,
    ErrorInesperado,
    ErrorLongitudInvalida,
)


class JuegoCazador:
    """Administra rondas, puntaje, excepciones y continuidad del juego."""

    def __init__(self):
        self.__puntaje = 0
        self.__rondas = 0

    def __leer_contrasena(self) -> str:
        clave = input("Ingrese contrasena (minimo 8 caracteres): ").strip()

        if len(clave) < Contrasena.LONGITUD_MINIMA:
            raise ErrorLongitudInvalida(len(clave), Contrasena.LONGITUD_MINIMA)

        contrasena = Contrasena(len(clave))
        contrasena.validar(clave)
        return clave

    def __aplicar_cofre(self, cofre) -> None:
        puntos = cofre.abrir()
        self.__puntaje += puntos
        self.__rondas += 1

        signo = "+" if puntos > 0 else ""
        print(f"Tipo de cofre: {cofre.nombre}")
        print(cofre.mensaje())
        print(f"Puntos de la ronda: {signo}{puntos}")
        print(f"Puntos acumulados: {self.__puntaje}")

    def __penalizar(self, error: Exception) -> None:
        print(f"\n{error}")
        print("La contrasena no pudo considerarse valida.")
        cofre = FabricaCofres.crear_cofre_maldito()
        self.__aplicar_cofre(cofre)

    def jugar_ronda(self) -> None:
        print("\n" + "=" * 50)
        print(f"RONDA {self.__rondas + 1}")
        print("=" * 50)

        try:
            clave = self.__leer_contrasena()
            print(f"\nContrasena ingresada: {clave}")

            print("Resultado: contrasena valida.")

            cofre = FabricaCofres.crear_cofre_valido()
            self.__aplicar_cofre(cofre)

        except (
            ErrorLongitudInvalida,
            ErrorContrasenaInvalida,
        ) as error:
            self.__penalizar(error)
        except Exception as error:
            raise ErrorInesperado(str(error)) from error

    def mostrar_menu_principal(self) -> None:
        print("=" * 50)
        print("CAZADOR DE 3 CONTRASENAS")
        print("=" * 50)
        print("Ingresa contrasenas validas para abrir cofres y ganar puntos.")
        print("Si una contrasena no cumple las reglas, abre un cofre maldito.")
        print("\nCondiciones obligatorias:")
        print("- El usuario debe ingresar una contrasena de minimo 8 caracteres.")
        print("- Al menos una letra mayuscula.")
        print("- Al menos una letra minuscula.")
        print("- Al menos un numero.")
        print(f"- Al menos un caracter especial: {Contrasena.ESPECIALES}")
        print("- Sin caracteres repetidos.\n")

        while True:
            self.jugar_ronda()

            continuar = input("\nDesea jugar otra ronda? (s/n): ").strip().lower()
            if continuar != "s":
                break

        print("\n" + "=" * 50)
        print("RESUMEN FINAL")
        print("=" * 50)
        print(f"Rondas jugadas: {self.__rondas}")
        print(f"Puntaje final: {self.__puntaje}")
        print("Gracias por jugar.")
