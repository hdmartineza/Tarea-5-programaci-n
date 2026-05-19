"""Clases de cofres del juego."""

import random
from abc import ABC, abstractmethod


class Cofre(ABC):
    """Clase base que representa un cofre."""

    def __init__(self, nombre: str, puntos: int):
        self._nombre = nombre
        self._puntos = puntos

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def puntos(self) -> int:
        return self._puntos

    def abrir(self) -> int:
        return self._puntos

    @abstractmethod
    def mensaje(self) -> str:
        """Mensaje propio de cada tipo de cofre."""


class CofreComun(Cofre):
    def __init__(self):
        super().__init__("Comun", 10)

    def mensaje(self) -> str:
        return "Cofre Comun abierto. Ganas 10 puntos."


class CofreRaro(Cofre):
    def __init__(self):
        super().__init__("Raro", 25)

    def mensaje(self) -> str:
        return "Cofre Raro abierto. Ganas 25 puntos."


class CofreLegendario(Cofre):
    def __init__(self):
        super().__init__("Legendario", 50)

    def mensaje(self) -> str:
        return "Cofre Legendario abierto. Ganas 50 puntos."


class CofreMaldito(Cofre):
    def __init__(self):
        super().__init__("Maldito", -20)

    def mensaje(self) -> str:
        return "Cofre Maldito abierto. Pierdes 20 puntos."


class FabricaCofres:
    """Crea cofres positivos aleatorios o un cofre maldito."""

    @staticmethod
    def crear_cofre_valido() -> Cofre:
        clases = [CofreComun, CofreRaro, CofreLegendario]
        pesos = [50, 30, 20]
        clase_elegida = random.choices(clases, weights=pesos, k=1)[0]
        return clase_elegida()

    @staticmethod
    def crear_cofre_maldito() -> Cofre:
        return CofreMaldito()
