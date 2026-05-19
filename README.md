# Cazador de Contrasenas

Juego interactivo en Python desarrollado con Programacion Orientada a Objetos, validacion estricta y manejo de excepciones personalizadas.

## Descripcion

El usuario asume el rol de un Cazador de 3 Contrasenas. En cada ronda debe ingresar una contrasena para intentar abrir un cofre y acumular puntos.

Si la contrasena cumple todas las reglas, el juego abre un cofre positivo aleatorio. Si no cumple alguna condicion, se abre un cofre Maldito y se restan puntos.

## Reglas de la contrasena

El programa solicita:

```text
Ingrese contrasena (minimo 8 caracteres):
```

La contrasena ingresada por el usuario:

- Debe tener minimo 8 caracteres.
- Puede tener mas de 8 caracteres.
- Puede mezclar letras, numeros y caracteres especiales.
- Debe contener al menos una letra mayuscula.
- Debe contener al menos una letra minuscula.
- Debe contener al menos un numero.
- Debe contener al menos un caracter especial de esta lista: `¿¡?=)(/¨*+-%&$#!`.
- No debe tener caracteres repetidos.

## Cofres y puntaje

- Comun: suma 10 puntos.
- Raro: suma 25 puntos.
- Legendario: suma 50 puntos.
- Maldito: resta 20 puntos cuando la contrasena es invalida.

## Clases principales

- `Contrasena`: valida que la contrasena cumpla las reglas obligatorias.
- `Cofre`: clase base para los cofres del juego.
- `CofreComun`, `CofreRaro`, `CofreLegendario`, `CofreMaldito`: representan los tipos de cofres.
- `FabricaCofres`: crea cofres positivos aleatorios o el cofre Maldito.
- `JuegoCazador`: administra rondas, puntaje, flujo del juego y manejo de excepciones.

## Excepciones personalizadas

- `ErrorLongitudInvalida`: cuando la contrasena tiene menos de 8 caracteres.
- `ErrorContrasenaInvalida`: cuando falta algun requisito o hay caracteres repetidos.
- `ErrorInesperado`: para errores no contemplados.

## Ejecucion

Desde la carpeta del proyecto:

```bash
python main.py
```

## Ejemplo de contrasena valida

```text
Abc123!?
```

Cumple porque tiene mayuscula, minusculas, numeros, caracter especial, minimo 8 caracteres y no repite caracteres.
