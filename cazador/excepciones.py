"""Excepciones personalizadas del juego Cazador de Contrasenas."""


class ErrorLongitudInvalida(Exception):
    """Se lanza cuando la longitud ingresada no cumple el minimo permitido."""

    def __init__(self, longitud_ingresada: int, minimo: int = 8):
        mensaje = (
            f"Longitud invalida: {longitud_ingresada}. "
            f"La longitud minima permitida es {minimo} caracteres."
        )
        super().__init__(mensaje)


class ErrorEntradaNoNumerica(Exception):
    """Se lanza cuando el usuario escribe un dato no numerico."""

    def __init__(self, valor_recibido: str):
        mensaje = f"Entrada invalida: '{valor_recibido}' no es un numero entero."
        super().__init__(mensaje)


class ErrorContrasenaInvalida(Exception):
    """Se lanza cuando una contrasena no cumple las reglas obligatorias."""

    def __init__(self, razon: str):
        super().__init__(f"Contrasena invalida: {razon}")


class ErrorInesperado(Exception):
    """Se lanza como proteccion ante errores no contemplados."""

    def __init__(self, detalle: str = "Ocurrio un error inesperado."):
        super().__init__(f"Error inesperado: {detalle}")
