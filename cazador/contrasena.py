"""Clase Contrasena: generacion y validacion de claves aleatorias."""

import random
import string

from cazador.excepciones import ErrorContrasenaInvalida, ErrorLongitudInvalida


class Contrasena:
    """Genera y valida contrasenas para abrir cofres."""

    LONGITUD_MINIMA = 8
    ESPECIALES = "\u00bf\u00a1?=)(/\u00a8*+-%&$#!"

    def __init__(self, longitud: int):
        if longitud < self.LONGITUD_MINIMA:
            raise ErrorLongitudInvalida(longitud, self.LONGITUD_MINIMA)

        self.__longitud = longitud
        self.__valor = ""

    @property
    def longitud(self) -> int:
        return self.__longitud

    @property
    def valor(self) -> str:
        return self.__valor

    def __universo_caracteres(self) -> list[str]:
        caracteres = (
            string.ascii_uppercase
            + string.ascii_lowercase
            + string.digits
            + self.ESPECIALES
        )
        return list(dict.fromkeys(caracteres))

    def generar(self) -> str:
        """Genera una contrasena aleatoria y sin caracteres repetidos."""
        universo = self.__universo_caracteres()
        if self.__longitud > len(universo):
            raise ErrorContrasenaInvalida(
                "no hay suficientes caracteres unicos para la longitud solicitada"
            )

        obligatorios = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice(self.ESPECIALES),
        ]

        restantes = [caracter for caracter in universo if caracter not in obligatorios]
        extras = random.sample(restantes, self.__longitud - len(obligatorios))
        caracteres_finales = obligatorios + extras
        random.shuffle(caracteres_finales)

        candidata = "".join(caracteres_finales)
        self.validar(candidata)
        self.__valor = candidata
        return self.__valor

    def validar(self, candidata: str) -> bool:
        if len(candidata) != self.__longitud:
            raise ErrorContrasenaInvalida("la longitud no coincide con la solicitada")
        if len(candidata) != len(set(candidata)):
            raise ErrorContrasenaInvalida("contiene caracteres repetidos")
        if not any(caracter.isupper() for caracter in candidata):
            raise ErrorContrasenaInvalida("falta una letra mayuscula")
        if not any(caracter.islower() for caracter in candidata):
            raise ErrorContrasenaInvalida("falta una letra minuscula")
        if not any(caracter.isdigit() for caracter in candidata):
            raise ErrorContrasenaInvalida("falta un numero")
        if not any(caracter in self.ESPECIALES for caracter in candidata):
            raise ErrorContrasenaInvalida("falta un caracter especial permitido")

        return True

    def __str__(self) -> str:
        return self.__valor
