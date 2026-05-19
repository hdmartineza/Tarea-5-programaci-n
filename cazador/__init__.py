"""API publica del paquete cazador."""

from cazador.cofres import (
    Cofre,
    CofreComun,
    CofreLegendario,
    CofreMaldito,
    CofreRaro,
    FabricaCofres,
)
from cazador.contrasena import Contrasena
from cazador.excepciones import (
    ErrorContrasenaInvalida,
    ErrorEntradaNoNumerica,
    ErrorInesperado,
    ErrorLongitudInvalida,
)
from cazador.juego import JuegoCazador

CofreBase = Cofre

__all__ = [
    "Cofre",
    "CofreBase",
    "CofreComun",
    "CofreLegendario",
    "CofreMaldito",
    "CofreRaro",
    "Contrasena",
    "ErrorContrasenaInvalida",
    "ErrorEntradaNoNumerica",
    "ErrorInesperado",
    "ErrorLongitudInvalida",
    "FabricaCofres",
    "JuegoCazador",
]
