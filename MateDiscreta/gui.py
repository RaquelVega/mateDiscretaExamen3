"""
Interfaz Gráfica de Usuario (GUI) Moderna y Atractiva para RSA.
Proyecto MM2015 Matemática Discreta 1 - Universidad del Valle de Guatemala

Integrantes:
- Raquel Pamela Tejada Vega (Carné: 25469)
- José Carlos Argueta González (Carné: 25652)
- Asistente de IA: Antigravity (Google DeepMind - Gemini 3.8 Flash)
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox

from rsa_core import encriptar, desencriptar, ValidacionError


class ColorTheme:
    """Definición de temas visuales (Oscuro Tecnológico y Claro Ejecutivo)."""
    
    DARK = {
        "name": "dark",
        "bg_app": "#0f172a",          # Slate 900
        "bg_header": "#090d16",       # Ultra dark navy
        "bg_card": "#1e293b",         # Slate 800
        "bg_card_inner": "#151e2e",   # Slate 850
        "bg_input": "#0b1322",        # Darker input background
        "border": "#334155",          # Slate 700
        "fg_title": "#f8fafc",        # Slate 50
        "fg_text": "#e2e8f0",         # Slate 200
        "fg_subtext": "#94a3b8",      # Slate 400
        "primary": "#2563eb",         # Royal Blue
        "primary_hover": "#1d4ed8",
        "accent": "#0ea5e9",          # Sky blue
        "accent_bg": "#0c4a6e",
        "success": "#10b981",         # Emerald green
        "success_bg": "#064e3b",
        "warning": "#f59e0b",         # Amber
        "warning_bg": "#78350f",
        "danger": "#ef4444",          # Red
        "badge_bg": "#1e293b",
        "badge_fg": "#38bdf8",
        "table_row1": "#1e293b",
        "table_row2": "#172033",
        "table_selected": "#2563eb",
        "table_header_bg": "#0f172a",
        "table_header_fg": "#38bdf8",
        "status_bg": "#0b1120",
        "status_fg": "#94a3b8"
    }

    LIGHT = {
        "name": "light",
        "bg_app": "#f1f5f9",          # Slate 100
        "bg_header": "#1e293b",       # Slate 800
        "bg_card": "#ffffff",         # Pure White
        "bg_card_inner": "#f8fafc",   # Slate 50
        "bg_input": "#ffffff",        # White input
        "border": "#cbd5e1",          # Slate 300
        "fg_title": "#0f172a",        # Slate 900
        "fg_text": "#1e293b",         # Slate 800
        "fg_subtext": "#64748b",      # Slate 500
        "primary": "#1d4ed8",         # Blue 700
        "primary_hover": "#1e40af",
        "accent": "#0284c7",          # Sky 600
        "accent_bg": "#e0f2fe",
        "success": "#059669",         # Emerald 600
        "success_bg": "#d1fae5",
        "warning": "#d97706",         # Amber 600
        "warning_bg": "#fef3c7",
        "danger": "#dc2626",          # Red 600
        "badge_bg": "#e2e8f0",
        "badge_fg": "#0369a1",
        "table_row1": "#ffffff",
        "table_row2": "#f8fafc",
        "table_selected": "#bfdbfe",
        "table_header_bg": "#e2e8f0",
        "table_header_fg": "#1e3a8a",
        "status_bg": "#e2e8f0",
        "status_fg": "#475569"
    }


class RSAApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Intentar habilitar alta definición (DPI) en Windows
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        self.title("Sistema Criptográfico RSA • MM2015 Matemática Discreta 1")
        self.geometry("1100x780")
        self.minsize(960, 680)

        # Centrar ventana en pantalla
        self._centrar_ventana(1100, 780)

        # Tema actual: por defecto modo oscuro elegante
        self.tema = ColorTheme.DARK
        
        # Cache de widgets actualizables para cambio de tema
        self.widgets_coloreables = []

        self._configurar_estilos_ttk()
        self._construir_interfaz()
        self._aplicar_tema()

    def _centrar_ventana(self, ancho, alto):
        self.update_idletasks()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = max(0, (pantalla_ancho // 2) - (ancho // 2))
        y = max(0, (pantalla_alto // 2) - (alto // 2) - 20)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _configurar_estilos_ttk(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

    def _aplicar_tema(self):
        t = self.tema
        self.configure(bg=t["bg_app"])

        # Estilo de Notebook
        self.style.configure(
            "TNotebook",
            background=t["bg_app"],
            tabmargins=[12, 6, 12, 0]
        )
        self.style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 10, "bold"),
            padding=[18, 10],
            background=t["bg_card"],
            foreground=t["fg_subtext"],
            borderwidth=0
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", t["primary"])],
            foreground=[("selected", "#ffffff")]
        )

        # Estilo de botones TTK
        self.style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground="#ffffff",
            background=t["primary"],
            padding=[16, 8],
            relief="flat"
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", t["primary_hover"]), ("pressed", t["primary_hover"])]
        )

        self.style.configure(
            "Action.TButton",
            font=("Segoe UI", 9, "bold"),
            foreground="#ffffff",
            background=t["accent"],
            padding=[12, 6],
            relief="flat"
        )
        self.style.map(
            "Action.TButton",
            background=[("active", t["primary"]), ("pressed", t["primary"])]
        )

        self.style.configure(
            "Outline.TButton",
            font=("Segoe UI", 9),
            foreground=t["fg_text"],
            background=t["bg_card_inner"],
            padding=[10, 6],
            relief="flat"
        )
        self.style.map(
            "Outline.TButton",
            background=[("active", t["border"])]
        )

        # Tablas Treeview
        self.style.configure(
            "Treeview",
            font=("Consolas", 9),
            rowheight=26,
            background=t["table_row1"],
            fieldbackground=t["table_row1"],
            foreground=t["fg_text"],
            borderwidth=0
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background=t["table_header_bg"],
            foreground=t["table_header_fg"],
            padding=[4, 6]
        )
        self.style.map(
            "Treeview",
            background=[("selected", t["table_selected"])],
            foreground=[("selected", "#ffffff")]
        )

        # Recorrer widgets registrados para actualizar colores
        for item in self.widgets_coloreables:
            widget = item["widget"]
            prop = item["prop"]
            color_key = item["color_key"]
            try:
                widget.configure(**{prop: t[color_key]})
            except Exception:
                pass

        # Configurar tags de tablas para alternancia de filas y resaltado
        for tabla in (self.tabla_enc, self.tabla_dec):
            tabla.tag_configure("par", background=t["table_row1"])
            tabla.tag_configure("impar", background=t["table_row2"])
            tabla.tag_configure("relleno", background=t["warning_bg"], foreground="#fbbf24" if t["name"] == "dark" else "#78350f")

    def _registrar_color(self, widget, prop, color_key):
        self.widgets_coloreables.append({
            "widget": widget,
            "prop": prop,
            "color_key": color_key
        })

    def _alternar_tema(self):
        if self.tema["name"] == "dark":
            self.tema = ColorTheme.LIGHT
            self.btn_tema.config(text="🌙 Modo Oscuro")
        else:
            self.tema = ColorTheme.DARK
            self.btn_tema.config(text="☀️ Modo Claro")
        self._aplicar_tema()

    # =========================================================================
    # CONSTRUCCIÓN DE LA INTERFAZ
    # =========================================================================
    def _construir_interfaz(self):
        # 1. ENCABEZADO SUPERIOR MODERNO (HERO BANNER)
        header = tk.Frame(self, pady=12, padx=20)
        header.pack(fill="x", side="top")
        self._registrar_color(header, "bg", "bg_header")

        # Fila superior del header: Título + Botón de Tema
        top_row = tk.Frame(header)
        top_row.pack(fill="x")
        self._registrar_color(top_row, "bg", "bg_header")

        lbl_logo = tk.Label(
            top_row,
            text="🛡️ SISTEMA CRIPTOGRÁFICO RSA",
            font=("Segoe UI", 15, "bold"),
            anchor="w"
        )
        lbl_logo.pack(side="left")
        self._registrar_color(lbl_logo, "bg", "bg_header")
        self._registrar_color(lbl_logo, "fg", "fg_title")

        self.btn_tema = tk.Button(
            top_row,
            text="☀️ Modo Claro",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self._alternar_tema
        )
        self.btn_tema.pack(side="right")
        self._registrar_color(self.btn_tema, "bg", "border")
        self._registrar_color(self.btn_tema, "fg", "fg_title")

        lbl_curso = tk.Label(
            header,
            text="MM2015 Matemática Discreta 1 • Criptografía Asimétrica y Algoritmos Propios",
            font=("Segoe UI", 9),
            anchor="w"
        )
        lbl_curso.pack(anchor="w", pady=(2, 6))
        self._registrar_color(lbl_curso, "bg", "bg_header")
        self._registrar_color(lbl_curso, "fg", "fg_subtext")

        # Fila de etiquetas con los autores y modelo IA
        badges_frame = tk.Frame(header)
        badges_frame.pack(anchor="w")
        self._registrar_color(badges_frame, "bg", "bg_header")

        self._crear_badge(badges_frame, "👤 Raquel Pamela Tejada Vega", "Carné 25469")
        self._crear_badge(badges_frame, "👤 José Carlos Argueta González", "Carné 25652")
        self._crear_badge(badges_frame, "🤖 Asistente IA", "Antigravity • Gemini 3.8 Flash")

        # 2. NOTEBOOK CON PESTAÑAS
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=10)

        # Pestaña 1: Encriptar
        self.tab_enc = tk.Frame(self.notebook)
        self.notebook.add(self.tab_enc, text="  🔒 Encriptar Mensaje  ")
        self._registrar_color(self.tab_enc, "bg", "bg_app")
        self._construir_tab_encriptar()

        # Pestaña 2: Desencriptar
        self.tab_dec = tk.Frame(self.notebook)
        self.notebook.add(self.tab_dec, text="  🔓 Desencriptar Mensaje  ")
        self._registrar_color(self.tab_dec, "bg", "bg_app")
        self._construir_tab_desencriptar()

        # Pestaña 3: Información
        self.tab_info = tk.Frame(self.notebook)
        self.notebook.add(self.tab_info, text="  ℹ️ Especificaciones y Autores  ")
        self._registrar_color(self.tab_info, "bg", "bg_app")
        self._construir_tab_informacion()

        # 3. BARRA DE ESTADO INFERIOR
        self.status_bar = tk.Frame(self, padx=16, pady=6)
        self.status_bar.pack(fill="x", side="bottom")
        self._registrar_color(self.status_bar, "bg", "status_bg")

        self.status_dot = tk.Label(self.status_bar, text="●", font=("Segoe UI", 10), fg="#10b981")
        self.status_dot.pack(side="left", padx=(0, 6))
        self._registrar_color(self.status_dot, "bg", "status_bg")

        self.status_text = tk.Label(
            self.status_bar,
            text="Listo. Ingrese los parámetros y seleccione una operación.",
            font=("Segoe UI", 9)
        )
        self.status_text.pack(side="left")
        self._registrar_color(self.status_text, "bg", "status_bg")
        self._registrar_color(self.status_text, "fg", "status_fg")

    def _crear_badge(self, parent, titulo, subtitulo):
        pill = tk.Frame(parent, padx=8, pady=3, bd=1, relief="solid")
        pill.pack(side="left", padx=(0, 8))
        self._registrar_color(pill, "bg", "bg_card")
        self._registrar_color(pill, "highlightbackground", "border")
        self._registrar_color(pill, "highlightcolor", "border")

        lbl1 = tk.Label(pill, text=f"{titulo}: ", font=("Segoe UI", 8, "bold"))
        lbl1.pack(side="left")
        self._registrar_color(lbl1, "bg", "bg_card")
        self._registrar_color(lbl1, "fg", "fg_title")

        lbl2 = tk.Label(pill, text=subtitulo, font=("Segoe UI", 8))
        lbl2.pack(side="left")
        self._registrar_color(lbl2, "bg", "bg_card")
        self._registrar_color(lbl2, "fg", "fg_subtext")

    # =========================================================================
    # PESTAÑA: ENCRIPTAR
    # =========================================================================
    def _construir_tab_encriptar(self):
        container = tk.Frame(self.tab_enc)
        container.pack(fill="both", expand=True, padx=6, pady=6)
        self._registrar_color(container, "bg", "bg_app")

        # PANEL IZQUIERDO: Entradas y acciones
        panel_izq = tk.Frame(container, width=380, padx=14, pady=12, bd=1, relief="solid")
        panel_izq.pack(side="left", fill="y", padx=(0, 6))
        panel_izq.pack_propagate(False)
        self._registrar_color(panel_izq, "bg", "bg_card")
        self._registrar_color(panel_izq, "highlightbackground", "border")

        # Tarjeta 1: Parámetros RSA
        lbl_p1 = tk.Label(panel_izq, text="1. Parámetros RSA", font=("Segoe UI", 11, "bold"), anchor="w")
        lbl_p1.pack(fill="x", pady=(0, 4))
        self._registrar_color(lbl_p1, "bg", "bg_card")
        self._registrar_color(lbl_p1, "fg", "accent")

        card_params = tk.Frame(panel_izq, padx=10, pady=8, bd=1, relief="solid")
        card_params.pack(fill="x", pady=(0, 8))
        self._registrar_color(card_params, "bg", "bg_card_inner")
        self._registrar_color(card_params, "highlightbackground", "border")

        # Grid p, q, e
        for r, (txt, var_name, def_val) in enumerate([
            ("Primo p:", "txt_enc_p", "367"),
            ("Primo q:", "txt_enc_q", "373"),
            ("Exponente e:", "txt_enc_e", "17")
        ]):
            l = tk.Label(card_params, text=txt, font=("Segoe UI", 9, "bold"), anchor="w")
            l.grid(row=r, column=0, sticky="w", pady=3)
            self._registrar_color(l, "bg", "bg_card_inner")
            self._registrar_color(l, "fg", "fg_text")

            entry = tk.Entry(card_params, font=("Consolas", 10, "bold"), width=12, bd=1, relief="solid")
            entry.grid(row=r, column=1, sticky="w", padx=6, pady=3)
            entry.insert(0, def_val)
            setattr(self, var_name, entry)
            self._registrar_color(entry, "bg", "bg_input")
            self._registrar_color(entry, "fg", "fg_title")

        # Botón para cargar ejemplo oficial
        btn_cargar = tk.Button(
            card_params,
            text="📌 Cargar Ejemplo Oficial (p=367, q=373, e=17)",
            font=("Segoe UI", 8, "bold"),
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self._cargar_ejemplo_referencia
        )
        btn_cargar.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(6, 2))
        self._registrar_color(btn_cargar, "bg", "border")
        self._registrar_color(btn_cargar, "fg", "fg_title")

        # Tarjeta 2: Mensaje Original M
        lbl_p2 = tk.Label(panel_izq, text="2. Mensaje Original M", font=("Segoe UI", 11, "bold"), anchor="w")
        lbl_p2.pack(fill="x", pady=(8, 2))
        self._registrar_color(lbl_p2, "bg", "bg_card")
        self._registrar_color(lbl_p2, "fg", "accent")

        lbl_hint = tk.Label(
            panel_izq,
            text="Admite caracteres ASCII [32, 126] (conserva espacios y signos)",
            font=("Segoe UI", 8),
            anchor="w"
        )
        lbl_hint.pack(fill="x", pady=(0, 4))
        self._registrar_color(lbl_hint, "bg", "bg_card")
        self._registrar_color(lbl_hint, "fg", "fg_subtext")

        self.txt_enc_msg = tk.Text(
            panel_izq,
            height=4,
            font=("Consolas", 10),
            wrap="word",
            bd=1,
            relief="solid",
            padx=6,
            pady=6
        )
        self.txt_enc_msg.pack(fill="x", pady=(0, 4))
        self.txt_enc_msg.insert("1.0", "RSA")
        self.txt_enc_msg.bind("<KeyRelease>", self._actualizar_contador_caracteres)
        self._registrar_color(self.txt_enc_msg, "bg", "bg_input")
        self._registrar_color(self.txt_enc_msg, "fg", "fg_title")

        # Indicador dinámico de caracteres y relleno en vivo
        self.lbl_enc_contador = tk.Label(
            panel_izq,
            text="Longitud L = 3 (Impar: Requiere +1 espacio de relleno)",
            font=("Segoe UI", 8, "bold"),
            anchor="w"
        )
        self.lbl_enc_contador.pack(fill="x", pady=(0, 10))
        self._registrar_color(self.lbl_enc_contador, "bg", "bg_card")
        self._registrar_color(self.lbl_enc_contador, "fg", "warning")

        # Botones de Acción
        btn_encriptar = tk.Button(
            panel_izq,
            text="🔒 ENCRIPTAR MENSAJE",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self._accion_encriptar
        )
        btn_encriptar.pack(fill="x", pady=(0, 6))
        self._registrar_color(btn_encriptar, "bg", "primary")
        self._registrar_color(btn_encriptar, "fg", "fg_title")

        btn_transferir = tk.Button(
            panel_izq,
            text="➡️ Transferir C y L a Desencriptación",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=10,
            pady=6,
            cursor="hand2",
            command=self._transferir_a_desencriptar
        )
        btn_transferir.pack(fill="x", pady=(0, 6))
        self._registrar_color(btn_transferir, "bg", "accent_bg")
        self._registrar_color(btn_transferir, "fg", "accent")

        btn_limpiar = tk.Button(
            panel_izq,
            text="🧹 Limpiar Campos",
            font=("Segoe UI", 8),
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self._limpiar_encriptacion
        )
        btn_limpiar.pack(fill="x")
        self._registrar_color(btn_limpiar, "bg", "border")
        self._registrar_color(btn_limpiar, "fg", "fg_subtext")

        # PANEL DERECHO: Resultados y KPIs matemáticos
        panel_der = tk.Frame(container)
        panel_der.pack(side="right", fill="both", expand=True)
        self._registrar_color(panel_der, "bg", "bg_app")

        # Grid de Tarjetas KPI Matemáticas
        frame_kpis = tk.Frame(panel_der)
        frame_kpis.pack(fill="x", pady=(0, 8))
        self._registrar_color(frame_kpis, "bg", "bg_app")

        self.kpi_enc_n = self._crear_kpi_card(frame_kpis, "MÓDULO n (p · q)", "-", "126126 < n < 1000000", col=0)
        self.kpi_enc_phi = self._crear_kpi_card(frame_kpis, "EULER φ(n)", "-", "(p - 1)(q - 1)", col=1)
        self.kpi_enc_mcd = self._crear_kpi_card(frame_kpis, "MCD(e, φ)", "-", "Euclides Propio = 1", col=2)
        self.kpi_enc_pad = self._crear_kpi_card(frame_kpis, "RELLENO (PADDING)", "-", "Si L impar (+1 espacio)", col=3)

        # Caja destacada del Cifrado C
        card_cifrado = tk.Frame(panel_der, padx=12, pady=10, bd=1, relief="solid")
        card_cifrado.pack(fill="x", pady=(0, 8))
        self._registrar_color(card_cifrado, "bg", "bg_card")
        self._registrar_color(card_cifrado, "highlightbackground", "border")

        lbl_c_title = tk.Label(card_cifrado, text="Mensaje Cifrado C (Bloques de 6 dígitos):", font=("Segoe UI", 9, "bold"), anchor="w")
        lbl_c_title.pack(fill="x")
        self._registrar_color(lbl_c_title, "bg", "bg_card")
        self._registrar_color(lbl_c_title, "fg", "fg_subtext")

        row_c_val = tk.Frame(card_cifrado)
        row_c_val.pack(fill="x", pady=(4, 2))
        self._registrar_color(row_c_val, "bg", "bg_card")

        self.lbl_cifrado_out = tk.Entry(
            row_c_val,
            font=("Consolas", 12, "bold"),
            bd=1,
            relief="solid"
        )
        self.lbl_cifrado_out.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._registrar_color(self.lbl_cifrado_out, "bg", "bg_input")
        self._registrar_color(self.lbl_cifrado_out, "fg", "warning")

        self.btn_copiar_c = tk.Button(
            row_c_val,
            text="📋 Copiar C",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self._copiar_con_feedback(self.btn_copiar_c, self.lbl_cifrado_out.get(), "📋 Copiar C")
        )
        self.btn_copiar_c.pack(side="right")
        self._registrar_color(self.btn_copiar_c, "bg", "accent")
        self._registrar_color(self.btn_copiar_c, "fg", "fg_title")

        self.lbl_enc_detalle_l = tk.Label(card_cifrado, text="Longitud original L: -  |  Llave Pública (e, n): -", font=("Segoe UI", 8), anchor="w")
        self.lbl_enc_detalle_l.pack(fill="x")
        self._registrar_color(self.lbl_enc_detalle_l, "bg", "bg_card")
        self._registrar_color(self.lbl_enc_detalle_l, "fg", "fg_subtext")

        # Tabla de Desglose de Bloques
        card_tabla = tk.Frame(panel_der, padx=10, pady=10, bd=1, relief="solid")
        card_tabla.pack(fill="both", expand=True)
        self._registrar_color(card_tabla, "bg", "bg_card")
        self._registrar_color(card_tabla, "highlightbackground", "border")

        lbl_t_enc = tk.Label(
            card_tabla,
            text="Desglose por Bloques (Caracteres ➔ Códigos ASCII ➔ Bloque m ➔ c ≡ mᵉ mod n):",
            font=("Segoe UI", 9, "bold"),
            anchor="w"
        )
        lbl_t_enc.pack(fill="x", pady=(0, 6))
        self._registrar_color(lbl_t_enc, "bg", "bg_card")
        self._registrar_color(lbl_t_enc, "fg", "accent")

        cols = ("idx", "par", "ascii", "m_num", "c_calc", "c_str", "relleno")
        self.tabla_enc = ttk.Treeview(card_tabla, columns=cols, show="headings", height=7)
        self.tabla_enc.heading("idx", text="#")
        self.tabla_enc.heading("par", text="Pareja")
        self.tabla_enc.heading("ascii", text="Códigos ASCII")
        self.tabla_enc.heading("m_num", text="Bloque m (6 d.)")
        self.tabla_enc.heading("c_calc", text="c = mᵉ mod n")
        self.tabla_enc.heading("c_str", text="Cifrado (6 dígitos)")
        self.tabla_enc.heading("relleno", text="¿Relleno?")

        self.tabla_enc.column("idx", width=36, anchor="center")
        self.tabla_enc.column("par", width=80, anchor="center")
        self.tabla_enc.column("ascii", width=120, anchor="center")
        self.tabla_enc.column("m_num", width=130, anchor="center")
        self.tabla_enc.column("c_calc", width=130, anchor="center")
        self.tabla_enc.column("c_str", width=140, anchor="center")
        self.tabla_enc.column("relleno", width=90, anchor="center")

        scroll_y = ttk.Scrollbar(card_tabla, orient="vertical", command=self.tabla_enc.yview)
        self.tabla_enc.configure(yscrollcommand=scroll_y.set)
        self.tabla_enc.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

    # =========================================================================
    # PESTAÑA: DESENCRIPTAR
    # =========================================================================
    def _construir_tab_desencriptar(self):
        container = tk.Frame(self.tab_dec)
        container.pack(fill="both", expand=True, padx=6, pady=6)
        self._registrar_color(container, "bg", "bg_app")

        # PANEL IZQUIERDO: Entradas
        panel_izq = tk.Frame(container, width=380, padx=14, pady=12, bd=1, relief="solid")
        panel_izq.pack(side="left", fill="y", padx=(0, 6))
        panel_izq.pack_propagate(False)
        self._registrar_color(panel_izq, "bg", "bg_card")
        self._registrar_color(panel_izq, "highlightbackground", "border")

        lbl_p1 = tk.Label(panel_izq, text="1. Parámetros RSA", font=("Segoe UI", 11, "bold"), anchor="w")
        lbl_p1.pack(fill="x", pady=(0, 4))
        self._registrar_color(lbl_p1, "bg", "bg_card")
        self._registrar_color(lbl_p1, "fg", "accent")

        card_params = tk.Frame(panel_izq, padx=10, pady=8, bd=1, relief="solid")
        card_params.pack(fill="x", pady=(0, 8))
        self._registrar_color(card_params, "bg", "bg_card_inner")
        self._registrar_color(card_params, "highlightbackground", "border")

        for r, (txt, var_name, def_val) in enumerate([
            ("Primo p:", "txt_dec_p", "367"),
            ("Primo q:", "txt_dec_q", "373"),
            ("Exponente e:", "txt_dec_e", "17")
        ]):
            l = tk.Label(card_params, text=txt, font=("Segoe UI", 9, "bold"), anchor="w")
            l.grid(row=r, column=0, sticky="w", pady=3)
            self._registrar_color(l, "bg", "bg_card_inner")
            self._registrar_color(l, "fg", "fg_text")

            entry = tk.Entry(card_params, font=("Consolas", 10, "bold"), width=12, bd=1, relief="solid")
            entry.grid(row=r, column=1, sticky="w", padx=6, pady=3)
            entry.insert(0, def_val)
            setattr(self, var_name, entry)
            self._registrar_color(entry, "bg", "bg_input")
            self._registrar_color(entry, "fg", "fg_title")

        # Cifrado C
        lbl_p2 = tk.Label(panel_izq, text="2. Cifrado C (Bloques de 6 dígitos)", font=("Segoe UI", 11, "bold"), anchor="w")
        lbl_p2.pack(fill="x", pady=(6, 2))
        self._registrar_color(lbl_p2, "bg", "bg_card")
        self._registrar_color(lbl_p2, "fg", "accent")

        self.txt_dec_c = tk.Text(
            panel_izq,
            height=3,
            font=("Consolas", 10),
            wrap="word",
            bd=1,
            relief="solid",
            padx=6,
            pady=6
        )
        self.txt_dec_c.pack(fill="x", pady=(0, 6))
        self.txt_dec_c.insert("1.0", "026054 123875")
        self._registrar_color(self.txt_dec_c, "bg", "bg_input")
        self._registrar_color(self.txt_dec_c, "fg", "fg_title")

        # Longitud original L
        lbl_p3 = tk.Label(panel_izq, text="3. Longitud original L:", font=("Segoe UI", 11, "bold"), anchor="w")
        lbl_p3.pack(fill="x", pady=(4, 2))
        self._registrar_color(lbl_p3, "bg", "bg_card")
        self._registrar_color(lbl_p3, "fg", "accent")

        row_l = tk.Frame(panel_izq)
        row_l.pack(fill="x", pady=(0, 10))
        self._registrar_color(row_l, "bg", "bg_card")

        self.txt_dec_l = tk.Entry(row_l, font=("Consolas", 10, "bold"), width=12, bd=1, relief="solid")
        self.txt_dec_l.pack(side="left")
        self.txt_dec_l.insert(0, "3")
        self._registrar_color(self.txt_dec_l, "bg", "bg_input")
        self._registrar_color(self.txt_dec_l, "fg", "fg_title")

        lbl_l_hint = tk.Label(row_l, text=" (Para k bloques: 2k o 2k-1)", font=("Segoe UI", 8), anchor="w")
        lbl_l_hint.pack(side="left", padx=4)
        self._registrar_color(lbl_l_hint, "bg", "bg_card")
        self._registrar_color(lbl_l_hint, "fg", "fg_subtext")

        # Botones de Acción
        btn_desencriptar = tk.Button(
            panel_izq,
            text="🔓 DESENCRIPTAR MENSAJE",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self._accion_desencriptar
        )
        btn_desencriptar.pack(fill="x", pady=(0, 6))
        self._registrar_color(btn_desencriptar, "bg", "success")
        self._registrar_color(btn_desencriptar, "fg", "fg_title")

        btn_limpiar_dec = tk.Button(
            panel_izq,
            text="🧹 Limpiar Campos",
            font=("Segoe UI", 8),
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self._limpiar_desencriptacion
        )
        btn_limpiar_dec.pack(fill="x")
        self._registrar_color(btn_limpiar_dec, "bg", "border")
        self._registrar_color(btn_limpiar_dec, "fg", "fg_subtext")

        # PANEL DERECHO: Resultados de Desencriptación
        panel_der = tk.Frame(container)
        panel_der.pack(side="right", fill="both", expand=True)
        self._registrar_color(panel_der, "bg", "bg_app")

        # Grid de Tarjetas KPI Matemáticas
        frame_kpis_dec = tk.Frame(panel_der)
        frame_kpis_dec.pack(fill="x", pady=(0, 8))
        self._registrar_color(frame_kpis_dec, "bg", "bg_app")

        self.kpi_dec_n = self._crear_kpi_card(frame_kpis_dec, "MÓDULO n (p · q)", "-", "Calculado a partir de p y q", col=0)
        self.kpi_dec_phi = self._crear_kpi_card(frame_kpis_dec, "EULER φ(n)", "-", "(p - 1)(q - 1)", col=1)
        self.kpi_dec_d = self._crear_kpi_card(frame_kpis_dec, "CLAVE PRIVADA d", "-", "Euclides Extendido (e · d ≡ 1)", col=2, highlight=True)
        self.kpi_dec_pad = self._crear_kpi_card(frame_kpis_dec, "COHERENCIA L", "-", "Verificación de relleno", col=3)

        # Caja destacada del Mensaje Recuperado
        card_recuperado = tk.Frame(panel_der, padx=12, pady=10, bd=1, relief="solid")
        card_recuperado.pack(fill="x", pady=(0, 8))
        self._registrar_color(card_recuperado, "bg", "bg_card")
        self._registrar_color(card_recuperado, "highlightbackground", "border")

        lbl_m_title = tk.Label(card_recuperado, text="Mensaje Original Recuperado M:", font=("Segoe UI", 9, "bold"), anchor="w")
        lbl_m_title.pack(fill="x")
        self._registrar_color(lbl_m_title, "bg", "bg_card")
        self._registrar_color(lbl_m_title, "fg", "fg_subtext")

        row_m_val = tk.Frame(card_recuperado)
        row_m_val.pack(fill="x", pady=(4, 2))
        self._registrar_color(row_m_val, "bg", "bg_card")

        self.lbl_msg_recuperado = tk.Entry(
            row_m_val,
            font=("Consolas", 12, "bold"),
            bd=1,
            relief="solid"
        )
        self.lbl_msg_recuperado.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._registrar_color(self.lbl_msg_recuperado, "bg", "bg_input")
        self._registrar_color(self.lbl_msg_recuperado, "fg", "success")

        self.btn_copiar_m = tk.Button(
            row_m_val,
            text="📋 Copiar M",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self._copiar_con_feedback(self.btn_copiar_m, self.lbl_msg_recuperado.get(), "📋 Copiar M")
        )
        self.btn_copiar_m.pack(side="right")
        self._registrar_color(self.btn_copiar_m, "bg", "success")
        self._registrar_color(self.btn_copiar_m, "fg", "fg_title")

        self.lbl_dec_detalle_relleno = tk.Label(card_recuperado, text="Estado del relleno: -  |  Llave Privada (d, n): -", font=("Segoe UI", 8), anchor="w")
        self.lbl_dec_detalle_relleno.pack(fill="x")
        self._registrar_color(self.lbl_dec_detalle_relleno, "bg", "bg_card")
        self._registrar_color(self.lbl_dec_detalle_relleno, "fg", "fg_subtext")

        # Tabla de Desglose de Desencriptación
        card_tabla_dec = tk.Frame(panel_der, padx=10, pady=10, bd=1, relief="solid")
        card_tabla_dec.pack(fill="both", expand=True)
        self._registrar_color(card_tabla_dec, "bg", "bg_card")
        self._registrar_color(card_tabla_dec, "highlightbackground", "border")

        lbl_t_dec = tk.Label(
            card_tabla_dec,
            text="Desglose por Bloques (Bloque c ➔ m ≡ cᵈ mod n ➔ ASCII ➔ Caracteres recuperados):",
            font=("Segoe UI", 9, "bold"),
            anchor="w"
        )
        lbl_t_dec.pack(fill="x", pady=(0, 6))
        self._registrar_color(lbl_t_dec, "bg", "bg_card")
        self._registrar_color(lbl_t_dec, "fg", "accent")

        cols_dec = ("idx", "c_str", "m_num", "m_str", "ascii", "chars", "relleno")
        self.tabla_dec = ttk.Treeview(card_tabla_dec, columns=cols_dec, show="headings", height=7)
        self.tabla_dec.heading("idx", text="#")
        self.tabla_dec.heading("c_str", text="Bloque c (6 d.)")
        self.tabla_dec.heading("m_num", text="m = cᵈ mod n")
        self.tabla_dec.heading("m_str", text="m (6 dígitos)")
        self.tabla_dec.heading("ascii", text="Códigos ASCII")
        self.tabla_dec.heading("chars", text="Caracteres")
        self.tabla_dec.heading("relleno", text="¿Relleno?")

        self.tabla_dec.column("idx", width=36, anchor="center")
        self.tabla_dec.column("c_str", width=120, anchor="center")
        self.tabla_dec.column("m_num", width=130, anchor="center")
        self.tabla_dec.column("m_str", width=130, anchor="center")
        self.tabla_dec.column("ascii", width=120, anchor="center")
        self.tabla_dec.column("chars", width=90, anchor="center")
        self.tabla_dec.column("relleno", width=90, anchor="center")

        scroll_y_dec = ttk.Scrollbar(card_tabla_dec, orient="vertical", command=self.tabla_dec.yview)
        self.tabla_dec.configure(yscrollcommand=scroll_y_dec.set)
        self.tabla_dec.pack(side="left", fill="both", expand=True)
        scroll_y_dec.pack(side="right", fill="y")

    # =========================================================================
    # PESTAÑA: INFORMACIÓN Y AUTORES
    # =========================================================================
    def _construir_tab_informacion(self):
        container = tk.Frame(self.tab_info, padx=16, pady=16)
        container.pack(fill="both", expand=True)
        self._registrar_color(container, "bg", "bg_app")

        card_info = tk.Frame(container, padx=20, pady=20, bd=1, relief="solid")
        card_info.pack(fill="both", expand=True)
        self._registrar_color(card_info, "bg", "bg_card")
        self._registrar_color(card_info, "highlightbackground", "border")

        texto_info = (
            "====================================================================================\n"
            "PROYECTO DE CRIPTOGRAFÍA RSA • MM2015 MATEMÁTICA DISCRETA 1\n"
            "Universidad del Valle de Guatemala\n"
            "====================================================================================\n\n"
            "👥 INTEGRANTES DEL GRUPO:\n"
            "   • Raquel Pamela Tejada Vega — Carné: 25469\n"
            "   • José Carlos Argueta González — Carné: 25652\n"
            "   • Asistente de IA: Antigravity (Google DeepMind — Gemini 3.8 Flash)\n\n"
            "🛡️ ALGORITMOS MATEMÁTICOS PROPIOS (Sin librerías externas):\n"
            "   1. Máximo Común Divisor: Algoritmo de Euclides clásico por divisiones sucesivas (mcd).\n"
            "   2. Inverso Modular: Algoritmo Extendido de Euclides iterativo (inverso_modular) con 1 <= d < phi.\n"
            "   3. Exponenciación Modular: Algoritmo binario Square-and-Multiply (exponenciacion_modular)\n"
            "      reduciendo módulo n en cada multiplicación intermedia (sin pow modular nativo).\n"
            "   4. Comprobación de Primalidad: Test por división de tentativa optimizado (es_primo).\n\n"
            "📋 CONDICIONES Y RANGOS CUMPLIDOS:\n"
            "   • 126126 < n < 1000000 (Módulo n de 6 dígitos que cubre cualquier pareja de caracteres).\n"
            "   • Caracteres admitidos: Códigos ASCII [32, 126] (conserva espacios, signos y mayúsculas/minúsculas).\n"
            "   • Cada carácter se representa con 3 dígitos (ej. 'A' -> 065) y cada bloque con 6 dígitos.\n"
            "   • Relleno (Padding): Si L es impar, se agrega exactamente un espacio ASCII 032 al final,\n"
            "     y se retira exactamente dicho espacio en la desencriptación sin usar strip() destructivo.\n\n"
            "💡 CASO DE REFERENCIA OFICIAL (Verificado):\n"
            "   • Entradas: Mensaje='RSA', p=367, q=373, e=17\n"
            "   • Valores: n=136891, phi=136152, MCD(e, phi)=1, L=3 (impar, relleno -> 'RSA ')\n"
            "   • Bloques m: 082083 065032  ->  Cifrado C: 026054 123875  (cero inicial verificado)\n"
            "   • Exponente privado: d=8009  ->  Mensaje recuperado exacto: 'RSA'\n"
        )

        txt_widget = tk.Text(
            card_info,
            font=("Consolas", 10),
            wrap="word",
            padx=12,
            pady=12,
            bd=0
        )
        txt_widget.insert("1.0", texto_info)
        txt_widget.configure(state="disabled")
        txt_widget.pack(fill="both", expand=True)
        self._registrar_color(txt_widget, "bg", "bg_card_inner")
        self._registrar_color(txt_widget, "fg", "fg_text")

    # =========================================================================
    # COMPONENTE REUTILIZABLE: TARJETA KPI METRIC CARD
    # =========================================================================
    def _crear_kpi_card(self, parent, titulo, valor_inicial, subtitulo, col, highlight=False):
        card = tk.Frame(parent, padx=12, pady=8, bd=1, relief="solid")
        card.grid(row=0, column=col, sticky="nsew", padx=3)
        parent.grid_columnconfigure(col, weight=1)
        self._registrar_color(card, "bg", "bg_card")
        self._registrar_color(card, "highlightbackground", "border")

        lbl_t = tk.Label(card, text=titulo, font=("Segoe UI", 7, "bold"), anchor="w")
        lbl_t.pack(fill="x")
        self._registrar_color(lbl_t, "bg", "bg_card")
        self._registrar_color(lbl_t, "fg", "fg_subtext")

        lbl_val = tk.Label(
            card,
            text=valor_inicial,
            font=("Consolas", 12, "bold"),
            anchor="w"
        )
        lbl_val.pack(fill="x", pady=2)
        self._registrar_color(lbl_val, "bg", "bg_card")
        self._registrar_color(lbl_val, "fg", "accent" if not highlight else "success")

        lbl_sub = tk.Label(card, text=subtitulo, font=("Segoe UI", 7), anchor="w")
        lbl_sub.pack(fill="x")
        self._registrar_color(lbl_sub, "bg", "bg_card")
        self._registrar_color(lbl_sub, "fg", "fg_subtext")

        return {"card": card, "val": lbl_val, "sub": lbl_sub}

    # =========================================================================
    # LÓGICA DE CONTROLADORES Y ACCIONES
    # =========================================================================
    def _actualizar_contador_caracteres(self, event=None):
        msg = self.txt_enc_msg.get("1.0", "end-1c")
        L = len(msg)
        if L == 0:
            self.lbl_enc_contador.config(
                text="Mensaje vacío (Ingrese texto)",
                fg=self.tema["fg_subtext"]
            )
        elif L % 2 == 0:
            k = L // 2
            self.lbl_enc_contador.config(
                text=f"Longitud L = {L} (Par: Sin relleno necesario | {k} bloques)",
                fg=self.tema["success"]
            )
        else:
            k = (L + 1) // 2
            self.lbl_enc_contador.config(
                text=f"Longitud L = {L} (Impar: Se agregará 1 espacio de relleno | {k} bloques)",
                fg=self.tema["warning"]
            )

    def _cargar_ejemplo_referencia(self):
        self.txt_enc_p.delete(0, tk.END)
        self.txt_enc_p.insert(0, "367")

        self.txt_enc_q.delete(0, tk.END)
        self.txt_enc_q.insert(0, "373")

        self.txt_enc_e.delete(0, tk.END)
        self.txt_enc_e.insert(0, "17")

        self.txt_enc_msg.delete("1.0", tk.END)
        self.txt_enc_msg.insert("1.0", "RSA")

        self._actualizar_contador_caracteres()
        self._set_status("Ejemplo oficial cargado: p=367, q=373, e=17, M='RSA'", "success")

    def _accion_encriptar(self):
        try:
            p = self.txt_enc_p.get().strip()
            q = self.txt_enc_q.get().strip()
            e = self.txt_enc_e.get().strip()
            msg = self.txt_enc_msg.get("1.0", "end-1c")

            res = encriptar(msg, p, q, e)

            # Actualizar KPIs
            self.kpi_enc_n["val"].config(text=f"{res['n']:,}")
            self.kpi_enc_phi["val"].config(text=f"{res['phi']:,}")
            self.kpi_enc_mcd["val"].config(text="1 (Coprimos)")
            self.kpi_enc_pad["val"].config(
                text="Sí (+1 espacio)" if res["tuvo_relleno"] else "No (Par)"
            )

            # Mostrar Cifrado C
            self.lbl_cifrado_out.delete(0, tk.END)
            self.lbl_cifrado_out.insert(0, res["cifrado_completo"])

            self.lbl_enc_detalle_l.config(
                text=f"Longitud original L = {res['L']} caracteres  |  "
                     f"Llave Pública (e, n) = ({res['e']}, {res['n']})  |  "
                     f"Total de bloques: {len(res['bloques_cifrados'])}"
            )

            # Llenar tabla de bloques con colores alternados
            for item in self.tabla_enc.get_children():
                self.tabla_enc.delete(item)

            for idx, b in enumerate(res["bloques_detalle"]):
                tag = "relleno" if b["es_relleno"] else ("par" if idx % 2 == 0 else "impar")
                self.tabla_enc.insert(
                    "",
                    tk.END,
                    values=(
                        b["indice"],
                        b["texto_par"],
                        b["ascii_par"],
                        b["m_str"],
                        b["c_num"],
                        b["c_str"],
                        "⚠️ Espacio (032)" if b["es_relleno"] else "No"
                    ),
                    tags=(tag,)
                )

            self._set_status(f"✓ Encriptación exitosa: {len(res['bloques_cifrados'])} bloques generados.", "success")

        except ValidacionError as ve:
            messagebox.showerror("Error de Validación (Encriptación)", str(ve))
            self._set_status(f"Error de validación: {ve}", "danger")
        except Exception as ex:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error inesperado:\n{ex}")
            self._set_status(f"Error: {ex}", "danger")

    def _transferir_a_desencriptar(self):
        cifrado = self.lbl_cifrado_out.get().strip()
        p = self.txt_enc_p.get().strip()
        q = self.txt_enc_q.get().strip()
        e = self.txt_enc_e.get().strip()
        msg = self.txt_enc_msg.get("1.0", "end-1c")

        if not cifrado:
            messagebox.showwarning("Atención", "Primero debe encriptar un mensaje para transferir los datos.")
            return

        L = len(msg)

        self.txt_dec_p.delete(0, tk.END)
        self.txt_dec_p.insert(0, p)

        self.txt_dec_q.delete(0, tk.END)
        self.txt_dec_q.insert(0, q)

        self.txt_dec_e.delete(0, tk.END)
        self.txt_dec_e.insert(0, e)

        self.txt_dec_c.delete("1.0", tk.END)
        self.txt_dec_c.insert("1.0", cifrado)

        self.txt_dec_l.delete(0, tk.END)
        self.txt_dec_l.insert(0, str(L))

        self.notebook.select(self.tab_dec)
        self._set_status("Datos transferidos exitosamente a Desencriptación.", "accent")

    def _accion_desencriptar(self):
        try:
            p = self.txt_dec_p.get().strip()
            q = self.txt_dec_q.get().strip()
            e = self.txt_dec_e.get().strip()
            cifrado = self.txt_dec_c.get("1.0", "end-1c").strip()
            L = self.txt_dec_l.get().strip()

            res = desencriptar(cifrado, L, p, q, e)

            # Actualizar KPIs
            self.kpi_dec_n["val"].config(text=f"{res['n']:,}")
            self.kpi_dec_phi["val"].config(text=f"{res['phi']:,}")
            self.kpi_dec_d["val"].config(text=str(res["d"]))
            self.kpi_dec_pad["val"].config(
                text="Válido (Relleno retirado)" if res["tuvo_relleno"] else "Válido (Sin relleno)"
            )

            # Mostrar mensaje recuperado
            self.lbl_msg_recuperado.delete(0, tk.END)
            self.lbl_msg_recuperado.insert(0, res["mensaje_recuperado"])

            self.lbl_dec_detalle_relleno.config(
                text=f"Texto preliminar con relleno: {repr(res['texto_con_posible_relleno'])}  ➔  "
                     f"Mensaje exacto: {repr(res['mensaje_recuperado'])}  |  "
                     f"Llave Privada (d, n) = ({res['d']}, {res['n']})"
            )

            # Llenar tabla de bloques
            for item in self.tabla_dec.get_children():
                self.tabla_dec.delete(item)

            for idx, b in enumerate(res["bloques_detalle"]):
                tag = "relleno" if b["es_relleno"] else ("par" if idx % 2 == 0 else "impar")
                self.tabla_dec.insert(
                    "",
                    tk.END,
                    values=(
                        b["indice"],
                        b["c_str"],
                        b["m_num"],
                        b["m_str"],
                        b["ascii_par"],
                        b["texto_par"],
                        "⚠️ Espacio retirado" if b["es_relleno"] else "No"
                    ),
                    tags=(tag,)
                )

            self._set_status("✓ Desencriptación exitosa: Mensaje recuperado con exactitud.", "success")

        except ValidacionError as ve:
            messagebox.showerror("Error de Validación (Desencriptación)", str(ve))
            self._set_status(f"Error de validación: {ve}", "danger")
        except Exception as ex:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error inesperado:\n{ex}")
            self._set_status(f"Error: {ex}", "danger")

    def _copiar_con_feedback(self, boton, texto, texto_original):
        if not texto:
            return
        self.clipboard_clear()
        self.clipboard_append(texto)
        boton.config(text="✓ ¡Copiado!", bg="#10b981", fg="#ffffff")
        self.after(1500, lambda: boton.config(text=texto_original, bg=self.tema["accent"] if "C" in texto_original else self.tema["success"], fg="#ffffff"))
        self._set_status("Texto copiado al portapapeles.", "accent")

    def _set_status(self, mensaje, tipo="normal"):
        color_map = {
            "normal": ("●", self.tema["fg_subtext"]),
            "success": ("●", "#10b981"),
            "accent": ("●", "#0ea5e9"),
            "warning": ("●", "#f59e0b"),
            "danger": ("●", "#ef4444")
        }
        icono, color = color_map.get(tipo, ("●", self.tema["fg_subtext"]))
        self.status_dot.config(text=icono, fg=color)
        self.status_text.config(text=mensaje)

    def _limpiar_encriptacion(self):
        self.txt_enc_p.delete(0, tk.END)
        self.txt_enc_q.delete(0, tk.END)
        self.txt_enc_e.delete(0, tk.END)
        self.txt_enc_msg.delete("1.0", tk.END)
        self.lbl_cifrado_out.delete(0, tk.END)
        self.lbl_enc_detalle_l.config(text="Longitud original L: -  |  Llave Pública (e, n): -")
        self.kpi_enc_n["val"].config(text="-")
        self.kpi_enc_phi["val"].config(text="-")
        self.kpi_enc_mcd["val"].config(text="-")
        self.kpi_enc_pad["val"].config(text="-")
        for item in self.tabla_enc.get_children():
            self.tabla_enc.delete(item)
        self._actualizar_contador_caracteres()
        self._set_status("Campos de encriptación limpiados.", "normal")

    def _limpiar_desencriptacion(self):
        self.txt_dec_p.delete(0, tk.END)
        self.txt_dec_q.delete(0, tk.END)
        self.txt_dec_e.delete(0, tk.END)
        self.txt_dec_c.delete("1.0", tk.END)
        self.txt_dec_l.delete(0, tk.END)
        self.lbl_msg_recuperado.delete(0, tk.END)
        self.lbl_dec_detalle_relleno.config(text="Estado del relleno: -  |  Llave Privada (d, n): -")
        self.kpi_dec_n["val"].config(text="-")
        self.kpi_dec_phi["val"].config(text="-")
        self.kpi_dec_d["val"].config(text="-")
        self.kpi_dec_pad["val"].config(text="-")
        for item in self.tabla_dec.get_children():
            self.tabla_dec.delete(item)
        self._set_status("Campos de desencriptación limpiados.", "normal")


def ejecutar_gui():
    app = RSAApplication()
    app.mainloop()


if __name__ == "__main__":
    ejecutar_gui()
