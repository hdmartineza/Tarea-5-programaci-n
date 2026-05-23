"""Entorno grafico del juego Cazador de Contrasenas."""

import tkinter as tk
from tkinter import ttk

try:
    import winsound
except ImportError:
    winsound = None

from cazador.cofres import FabricaCofres
from cazador.contrasena import Contrasena
from cazador.excepciones import ErrorContrasenaInvalida, ErrorLongitudInvalida


class EntornoGrafico:
    """Interfaz visual para ejecutar el juego."""

    COLORES_COFRE = {
        "Comun": "#38bdf8",
        "Raro": "#a78bfa",
        "Legendario": "#facc15",
        "Maldito": "#fb7185",
    }

    RANGOS = [
        (100, "Leyenda de Cofres"),
        (60, "Maestro Cazador"),
        (30, "Cazador Experto"),
        (10, "Explorador"),
        (0, "Aprendiz"),
        (-9999, "Maldito"),
    ]

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Cazador de Contrasenas")
        self.ventana.geometry("1040x700")
        self.ventana.minsize(900, 620)
        self.ventana.configure(bg="#101828")

        self.puntaje = 0
        self.rondas = 0
        self.animando = False
        self.mostrar_clave = tk.BooleanVar(value=False)
        self.reglas_labels = {}

        self._configurar_estilos()
        self._construir_interfaz()
        self._actualizar_analisis()

    def _configurar_estilos(self) -> None:
        self.estilo = ttk.Style(self.ventana)
        self.estilo.theme_use("clam")

        self.estilo.configure("Panel.TFrame", background="#182033", borderwidth=0)
        self.estilo.configure(
            "Titulo.TLabel",
            background="#101828",
            foreground="#f8fafc",
            font=("Segoe UI", 29, "bold"),
        )
        self.estilo.configure(
            "Subtitulo.TLabel",
            background="#101828",
            foreground="#cbd5e1",
            font=("Segoe UI", 11),
        )
        self.estilo.configure(
            "PanelTitulo.TLabel",
            background="#182033",
            foreground="#e2e8f0",
            font=("Segoe UI", 15, "bold"),
        )
        self.estilo.configure(
            "PanelTexto.TLabel",
            background="#182033",
            foreground="#cbd5e1",
            font=("Segoe UI", 10),
        )
        self.estilo.configure(
            "Dato.TLabel",
            background="#182033",
            foreground="#f8fafc",
            font=("Segoe UI", 24, "bold"),
        )
        self.estilo.configure(
            "DatoNombre.TLabel",
            background="#182033",
            foreground="#94a3b8",
            font=("Segoe UI", 10, "bold"),
        )
        self.estilo.configure(
            "Cazador.TButton",
            background="#f59e0b",
            foreground="#111827",
            borderwidth=0,
            focusthickness=0,
            font=("Segoe UI", 12, "bold"),
            padding=(16, 12),
        )
        self.estilo.map(
            "Cazador.TButton",
            background=[("active", "#fbbf24"), ("pressed", "#d97706")],
        )
        self.estilo.configure(
            "Secundario.TButton",
            background="#334155",
            foreground="#e2e8f0",
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padding=(12, 9),
        )
        self.estilo.map(
            "Secundario.TButton",
            background=[("active", "#475569"), ("pressed", "#1e293b")],
        )
        self.estilo.configure(
            "TCheckbutton",
            background="#182033",
            foreground="#cbd5e1",
            font=("Segoe UI", 9),
        )

    def _construir_interfaz(self) -> None:
        contenedor = tk.Frame(self.ventana, bg="#101828")
        contenedor.pack(fill="both", expand=True, padx=28, pady=24)
        contenedor.columnconfigure(0, weight=3)
        contenedor.columnconfigure(1, weight=2)
        contenedor.rowconfigure(1, weight=1)

        encabezado = tk.Frame(contenedor, bg="#101828")
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))
        encabezado.columnconfigure(0, weight=1)

        ttk.Label(
            encabezado,
            text="Cazador de Contrasenas",
            style="Titulo.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            encabezado,
            text="Rompe el sello de los cofres creando claves poderosas.",
            style="Subtitulo.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.etiqueta_rango_superior = tk.Label(
            encabezado,
            text="Rango: Aprendiz",
            bg="#f59e0b",
            fg="#111827",
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=8,
        )
        self.etiqueta_rango_superior.grid(row=0, column=1, rowspan=2, sticky="e")

        zona_juego = ttk.Frame(contenedor, style="Panel.TFrame")
        zona_juego.grid(row=1, column=0, sticky="nsew", padx=(0, 18))
        zona_juego.columnconfigure(0, weight=1)

        self._crear_panel_entrada(zona_juego)
        self._crear_panel_resultado(zona_juego)
        self._crear_panel_historial(zona_juego)
        self._crear_panel_lateral(contenedor)

    def _crear_panel_entrada(self, padre: ttk.Frame) -> None:
        panel = tk.Frame(padre, bg="#182033", padx=24, pady=22)
        panel.grid(row=0, column=0, sticky="ew")
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="Forja tu contrasena", style="PanelTitulo.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            panel,
            text="Escribe y mira como cambia la fuerza de tu clave antes de abrir el cofre.",
            style="PanelTexto.TLabel",
            wraplength=620,
        ).grid(row=1, column=0, sticky="w", pady=(6, 14))

        fila = tk.Frame(panel, bg="#182033")
        fila.grid(row=2, column=0, sticky="ew")
        fila.columnconfigure(0, weight=1)

        self.entrada = tk.Entry(
            fila,
            show="*",
            bg="#0f172a",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            relief="flat",
            font=("Segoe UI", 16),
            highlightthickness=2,
            highlightbackground="#334155",
            highlightcolor="#f59e0b",
        )
        self.entrada.grid(row=0, column=0, sticky="ew", ipady=12, padx=(0, 12))
        self.entrada.bind("<Return>", lambda _evento: self.jugar_ronda())
        self.entrada.bind("<KeyRelease>", lambda _evento: self._actualizar_analisis())
        self.entrada.focus_set()

        self.boton_abrir = ttk.Button(
            fila,
            text="Abrir cofre",
            style="Cazador.TButton",
            command=self.jugar_ronda,
        )
        self.boton_abrir.grid(row=0, column=1, sticky="e")

        self.barra_fuerza = tk.Canvas(
            panel,
            bg="#0f172a",
            height=18,
            highlightthickness=0,
            bd=0,
        )
        self.barra_fuerza.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        self.barra_fuerza.bind(
            "<Configure>",
            lambda _evento: self._actualizar_analisis(),
        )

        self.etiqueta_fuerza = tk.Label(
            panel,
            text="Fortaleza: sin clave",
            bg="#182033",
            fg="#94a3b8",
            font=("Segoe UI", 10, "bold"),
        )
        self.etiqueta_fuerza.grid(row=4, column=0, sticky="w", pady=(6, 0))

        opciones = tk.Frame(panel, bg="#182033")
        opciones.grid(row=5, column=0, sticky="w", pady=(12, 0))
        ttk.Checkbutton(
            opciones,
            text="Mostrar contrasena",
            variable=self.mostrar_clave,
            command=self._alternar_visibilidad,
        ).pack(side="left")
        ttk.Button(
            opciones,
            text="Generar valida",
            style="Secundario.TButton",
            command=self.generar_contrasena,
        ).pack(side="left", padx=(14, 0))
        ttk.Button(
            opciones,
            text="Reiniciar partida",
            style="Secundario.TButton",
            command=self.reiniciar,
        ).pack(side="left", padx=(14, 0))

    def _crear_panel_resultado(self, padre: ttk.Frame) -> None:
        panel = tk.Frame(padre, bg="#111827", padx=24, pady=22)
        panel.grid(row=1, column=0, sticky="ew", padx=18, pady=18)
        panel.columnconfigure(1, weight=1)

        self.canvas_cofre = tk.Canvas(
            panel,
            width=150,
            height=130,
            bg="#111827",
            highlightthickness=0,
            bd=0,
        )
        self.canvas_cofre.grid(row=0, column=0, rowspan=3, sticky="n", padx=(0, 22))
        self._dibujar_cofre("Comun", abierto=False)

        self.tipo_cofre = tk.Label(
            panel,
            text="Esperando tu intento",
            bg="#111827",
            fg="#f8fafc",
            font=("Segoe UI", 18, "bold"),
        )
        self.tipo_cofre.grid(row=0, column=1, sticky="w")

        self.mensaje_resultado = tk.Label(
            panel,
            text="Ingresa una contrasena para descubrir que cofre aparece.",
            bg="#111827",
            fg="#cbd5e1",
            font=("Segoe UI", 11),
            wraplength=560,
            justify="left",
        )
        self.mensaje_resultado.grid(row=1, column=1, sticky="w", pady=(8, 0))

        self.puntos_ronda = tk.Label(
            panel,
            text="Ronda +0",
            bg="#111827",
            fg="#94a3b8",
            font=("Segoe UI", 12, "bold"),
        )
        self.puntos_ronda.grid(row=2, column=1, sticky="w", pady=(14, 0))

    def _crear_panel_historial(self, padre: ttk.Frame) -> None:
        panel = tk.Frame(padre, bg="#182033", padx=24, pady=18)
        panel.grid(row=2, column=0, sticky="nsew")
        padre.rowconfigure(2, weight=1)

        ttk.Label(panel, text="Registro de la aventura", style="PanelTitulo.TLabel").pack(
            anchor="w"
        )

        self.historial = tk.Listbox(
            panel,
            bg="#0f172a",
            fg="#e2e8f0",
            selectbackground="#334155",
            selectforeground="#f8fafc",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=("Consolas", 10),
            height=8,
        )
        self.historial.pack(fill="both", expand=True, pady=(12, 0))

    def _crear_panel_lateral(self, contenedor: tk.Frame) -> None:
        lateral = ttk.Frame(contenedor, style="Panel.TFrame")
        lateral.grid(row=1, column=1, sticky="nsew")
        lateral.columnconfigure(0, weight=1)

        marcador = tk.Frame(lateral, bg="#182033", padx=22, pady=22)
        marcador.grid(row=0, column=0, sticky="ew")
        marcador.columnconfigure((0, 1), weight=1)

        ttk.Label(marcador, text="Puntaje", style="DatoNombre.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(marcador, text="Rondas", style="DatoNombre.TLabel").grid(
            row=0, column=1, sticky="w"
        )

        self.etiqueta_puntaje = ttk.Label(marcador, text="0", style="Dato.TLabel")
        self.etiqueta_puntaje.grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.etiqueta_rondas = ttk.Label(marcador, text="0", style="Dato.TLabel")
        self.etiqueta_rondas.grid(row=1, column=1, sticky="w", pady=(6, 0))

        self.etiqueta_rango = tk.Label(
            marcador,
            text="Aprendiz",
            bg="#0f172a",
            fg="#facc15",
            font=("Segoe UI", 11, "bold"),
            padx=12,
            pady=8,
        )
        self.etiqueta_rango.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(16, 0))

        reglas = tk.Frame(lateral, bg="#182033", padx=22, pady=20)
        reglas.grid(row=1, column=0, sticky="nsew", pady=(18, 0))
        lateral.rowconfigure(1, weight=1)

        ttk.Label(reglas, text="Sello de seguridad", style="PanelTitulo.TLabel").pack(
            anchor="w"
        )

        self._crear_regla(reglas, "longitud", "Minimo 8 caracteres")
        self._crear_regla(reglas, "mayuscula", "Una letra mayuscula")
        self._crear_regla(reglas, "minuscula", "Una letra minuscula")
        self._crear_regla(reglas, "numero", "Un numero")
        self._crear_regla(reglas, "especial", f"Un simbolo: {Contrasena.ESPECIALES}")
        self._crear_regla(reglas, "sin_repetidos", "Sin caracteres repetidos")

        premios = tk.Frame(lateral, bg="#0f172a", padx=18, pady=16)
        premios.grid(row=2, column=0, sticky="ew", pady=(18, 0))
        tk.Label(
            premios,
            text="Cofres: Comun +10 | Raro +25 | Legendario +50 | Maldito -20",
            bg="#0f172a",
            fg="#f8fafc",
            font=("Segoe UI", 10, "bold"),
            wraplength=300,
            justify="left",
        ).pack(anchor="w")

    def _crear_regla(self, padre: tk.Frame, clave: str, texto: str) -> None:
        etiqueta = tk.Label(
            padre,
            text=f"[ ] {texto}",
            bg="#182033",
            fg="#94a3b8",
            font=("Segoe UI", 10, "bold"),
            justify="left",
            wraplength=310,
        )
        etiqueta.pack(anchor="w", pady=5)
        self.reglas_labels[clave] = etiqueta

    def _alternar_visibilidad(self) -> None:
        self.entrada.configure(show="" if self.mostrar_clave.get() else "*")

    def _validar_contrasena(self, clave: str) -> None:
        if len(clave) < Contrasena.LONGITUD_MINIMA:
            raise ErrorLongitudInvalida(len(clave), Contrasena.LONGITUD_MINIMA)

        contrasena = Contrasena(len(clave))
        contrasena.validar(clave)

    def _estado_reglas(self, clave: str) -> dict[str, bool]:
        return {
            "longitud": len(clave) >= Contrasena.LONGITUD_MINIMA,
            "mayuscula": any(caracter.isupper() for caracter in clave),
            "minuscula": any(caracter.islower() for caracter in clave),
            "numero": any(caracter.isdigit() for caracter in clave),
            "especial": any(caracter in Contrasena.ESPECIALES for caracter in clave),
            "sin_repetidos": len(clave) > 0 and len(clave) == len(set(clave)),
        }

    def _actualizar_analisis(self) -> None:
        clave = self.entrada.get().strip() if hasattr(self, "entrada") else ""
        estados = self._estado_reglas(clave)
        cumplidas = sum(1 for activa in estados.values() if activa)
        total = len(estados)

        textos = {
            "longitud": "Minimo 8 caracteres",
            "mayuscula": "Una letra mayuscula",
            "minuscula": "Una letra minuscula",
            "numero": "Un numero",
            "especial": f"Un simbolo: {Contrasena.ESPECIALES}",
            "sin_repetidos": "Sin caracteres repetidos",
        }

        for nombre, activa in estados.items():
            prefijo = "[x]" if activa else "[ ]"
            color = "#86efac" if activa else "#94a3b8"
            self.reglas_labels[nombre].configure(
                text=f"{prefijo} {textos[nombre]}",
                fg=color,
            )

        porcentaje = cumplidas / total if total else 0
        if not clave:
            nivel, color = "sin clave", "#475569"
        elif porcentaje < 0.5:
            nivel, color = "debil", "#fb7185"
        elif porcentaje < 0.85:
            nivel, color = "media", "#f59e0b"
        elif porcentaje < 1:
            nivel, color = "fuerte", "#38bdf8"
        else:
            nivel, color = "perfecta", "#86efac"

        self.etiqueta_fuerza.configure(
            text=f"Fortaleza: {nivel} ({cumplidas}/{total})",
            fg=color,
        )
        self._dibujar_barra_fuerza(porcentaje, color)

    def _dibujar_barra_fuerza(self, porcentaje: float, color: str) -> None:
        self.barra_fuerza.delete("all")
        ancho = max(self.barra_fuerza.winfo_width(), 260)
        alto = 18
        relleno = int(ancho * porcentaje)

        self.barra_fuerza.create_rectangle(0, 0, ancho, alto, fill="#0f172a", outline="")
        self.barra_fuerza.create_rectangle(0, 0, relleno, alto, fill=color, outline="")
        for marca in range(1, 6):
            x = int(ancho * marca / 6)
            self.barra_fuerza.create_line(x, 0, x, alto, fill="#1e293b")

    def generar_contrasena(self) -> None:
        generador = Contrasena(10)
        clave = generador.generar()
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, clave)
        self._actualizar_analisis()
        self.mensaje_resultado.configure(
            text="Se genero una contrasena valida. Puedes abrir el cofre o modificarla."
        )

    def jugar_ronda(self) -> None:
        if self.animando:
            return

        clave = self.entrada.get().strip()
        if not clave:
            self._mostrar_resultado(
                nombre="Maldito",
                puntos=0,
                mensaje="Primero escribe una contrasena para retar al cofre.",
                registrar=False,
                animar=False,
            )
            return

        try:
            self._validar_contrasena(clave)
            cofre = FabricaCofres.crear_cofre_valido()
            mensaje = "Contrasena valida. " + cofre.mensaje()
        except (ErrorLongitudInvalida, ErrorContrasenaInvalida) as error:
            cofre = FabricaCofres.crear_cofre_maldito()
            mensaje = f"{error} {cofre.mensaje()}"

        puntos = cofre.abrir()
        self.puntaje += puntos
        self.rondas += 1
        self._actualizar_marcador()
        self._mostrar_resultado(cofre.nombre, puntos, mensaje, animar=True)
        self.entrada.delete(0, tk.END)
        self._actualizar_analisis()

    def _mostrar_resultado(
        self,
        nombre: str,
        puntos: int,
        mensaje: str,
        registrar: bool = True,
        animar: bool = True,
    ) -> None:
        color = self.COLORES_COFRE.get(nombre, "#f8fafc")
        signo = "+" if puntos > 0 else ""

        self.tipo_cofre.configure(text="Abriendo cofre...", fg=color)
        self.mensaje_resultado.configure(text=mensaje)
        self.puntos_ronda.configure(text=f"Ronda {signo}{puntos}", fg=color)

        if registrar:
            resumen = f"Ronda {self.rondas:02d} | {nombre:<11} | {signo}{puntos:>3} pts | Total {self.puntaje}"
            self.historial.insert(0, resumen)

        if animar:
            self._animar_cofre(nombre, color)
        else:
            self.tipo_cofre.configure(text=f"Cofre {nombre}", fg=color)
            self._dibujar_cofre(nombre, abierto=True)

        self._reproducir_sonido(nombre)

    def _dibujar_cofre(self, nombre: str, abierto: bool = False, desplazamiento: int = 0) -> None:
        color = self.COLORES_COFRE.get(nombre, "#38bdf8")
        borde = "#f8fafc" if nombre == "Legendario" else "#0f172a"
        brillo = "#fff7ad" if nombre == "Legendario" else color
        y = 10 + desplazamiento

        self.canvas_cofre.delete("all")
        if abierto:
            self.canvas_cofre.create_oval(30, y + 2, 120, y + 40, fill=brillo, outline="")
            self.canvas_cofre.create_rectangle(
                40,
                y + 20,
                110,
                y + 52,
                fill=color,
                outline=borde,
                width=3,
            )
            self.canvas_cofre.create_line(
                42,
                y + 50,
                24,
                y + 26,
                fill=borde,
                width=4,
            )
            self.canvas_cofre.create_line(
                108,
                y + 50,
                126,
                y + 26,
                fill=borde,
                width=4,
            )
        else:
            self.canvas_cofre.create_arc(
                28,
                y + 10,
                122,
                y + 86,
                start=0,
                extent=180,
                fill=color,
                outline=borde,
                width=3,
            )

        self.canvas_cofre.create_rectangle(
            22,
            y + 50,
            128,
            y + 112,
            fill=color,
            outline=borde,
            width=3,
        )
        self.canvas_cofre.create_rectangle(
            66,
            y + 62,
            84,
            y + 88,
            fill="#facc15",
            outline="#78350f",
            width=2,
        )
        self.canvas_cofre.create_line(22, y + 72, 128, y + 72, fill="#0f172a", width=3)
        self.canvas_cofre.create_line(44, y + 50, 44, y + 112, fill="#0f172a", width=2)
        self.canvas_cofre.create_line(106, y + 50, 106, y + 112, fill="#0f172a", width=2)

        if nombre == "Maldito":
            self.canvas_cofre.create_text(
                75,
                y + 88,
                text="!",
                fill="#111827",
                font=("Segoe UI", 16, "bold"),
            )
        elif nombre == "Legendario":
            self.canvas_cofre.create_text(
                75,
                y + 34,
                text="*",
                fill="#111827",
                font=("Segoe UI", 22, "bold"),
            )

    def _animar_cofre(self, nombre: str, color: str, paso: int = 0) -> None:
        self.animando = True
        self.boton_abrir.state(["disabled"])
        offsets = [0, -5, 5, -4, 4, -2, 2, 0]

        if paso < len(offsets):
            self._dibujar_cofre(nombre, abierto=False, desplazamiento=offsets[paso])
            self.ventana.after(70, lambda: self._animar_cofre(nombre, color, paso + 1))
            return

        self._dibujar_cofre(nombre, abierto=True)
        self.tipo_cofre.configure(text=f"Cofre {nombre}", fg=color)
        self.animando = False
        self.boton_abrir.state(["!disabled"])

    def _reproducir_sonido(self, nombre: str) -> None:
        if winsound is None:
            return

        tonos = {
            "Comun": (660, 90),
            "Raro": (780, 110),
            "Legendario": (980, 140),
            "Maldito": (260, 160),
        }
        frecuencia, duracion = tonos.get(nombre, (600, 90))
        try:
            winsound.Beep(frecuencia, duracion)
        except RuntimeError:
            pass

    def _rango_actual(self) -> str:
        for minimo, nombre in self.RANGOS:
            if self.puntaje >= minimo:
                return nombre
        return "Aprendiz"

    def _actualizar_marcador(self) -> None:
        rango = self._rango_actual()
        self.etiqueta_puntaje.configure(text=str(self.puntaje))
        self.etiqueta_rondas.configure(text=str(self.rondas))
        self.etiqueta_rango.configure(text=rango)
        self.etiqueta_rango_superior.configure(text=f"Rango: {rango}")

    def reiniciar(self) -> None:
        self.puntaje = 0
        self.rondas = 0
        self.animando = False
        self._actualizar_marcador()
        self.historial.delete(0, tk.END)
        self.entrada.delete(0, tk.END)
        self.boton_abrir.state(["!disabled"])
        self._mostrar_resultado(
            nombre="Comun",
            puntos=0,
            mensaje="Partida reiniciada. Ingresa una nueva contrasena.",
            registrar=False,
            animar=False,
        )
        self.tipo_cofre.configure(text="Esperando tu intento", fg="#f8fafc")
        self.puntos_ronda.configure(text="Ronda +0", fg="#94a3b8")
        self._dibujar_cofre("Comun", abierto=False)
        self._actualizar_analisis()

    def ejecutar(self) -> None:
        self.ventana.mainloop()


def iniciar_entorno_grafico() -> None:
    """Arranca el juego en modo grafico."""
    EntornoGrafico().ejecutar()
