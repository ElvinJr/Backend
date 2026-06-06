# theme.py
# Este archivo define todos los colores y estilos que usaremos en XP Movies.

# ─── PALETA DE COLORES ───────────────────────────────────────────────
# Colores principales de XP Movies (negro con rojo oscuro)

NEGRO_FONDO = "#0A0A0A"          # Fondo principal de la página
NEGRO_CARD = "#111111"           # Fondo de las tarjetas de películas
NEGRO_NAVBAR = "#0D0D0D"         # Fondo de la barra de navegación
ROJO_PRINCIPAL = "#8B0000"       # Rojo oscuro principal (botones, acentos)
ROJO_HOVER = "#A50000"           # Rojo al pasar el mouse por encima
ROJO_CLARO = "#C0392B"           # Rojo más claro para detalles
BLANCO = "#FFFFFF"               # Texto principal
GRIS_TEXTO = "#AAAAAA"           # Texto secundario (descripciones, fechas)
GRIS_BORDE = "#222222"           # Bordes de tarjetas y divisores
AMARILLO_ESTRELLAS = "#FFD700"   # Color de las estrellas de calificación

# ─── ESTILOS DE TEXTO ────────────────────────────────────────────────
# Definimos tamaños y pesos de fuente para mantener consistencia

FUENTE_PRINCIPAL = "Bebas Neue"   # Fuente para títulos grandes
FUENTE_SECUNDARIA = "Inter"       # Fuente para texto normal

TITULO_GRANDE = {
    "font_size": "3em",
    "font_weight": "bold",
    "color": BLANCO,
    "font_family": FUENTE_PRINCIPAL,
    "letter_spacing": "2px",
}

TITULO_SECCION = {
    "font_size": "1.8em",
    "font_weight": "bold",
    "color": BLANCO,
    "font_family": FUENTE_PRINCIPAL,
    "letter_spacing": "1px",
}

TEXTO_NORMAL = {
    "font_size": "1em",
    "color": GRIS_TEXTO,
    "font_family": FUENTE_SECUNDARIA,
}

TEXTO_DESTACADO = {
    "font_size": "1em",
    "color": BLANCO,
    "font_family": FUENTE_SECUNDARIA,
    "font_weight": "600",
}

# ─── ESTILOS DE BOTONES ──────────────────────────────────────────────
# El botón principal rojo que se usará en toda la página

BOTON_PRIMARIO = {
    "background_color": ROJO_PRINCIPAL,
    "color": BLANCO,
    "border_radius": "6px",
    "padding": "10px 24px",
    "font_weight": "bold",
    "font_family": FUENTE_SECUNDARIA,
    "cursor": "pointer",
    "border": "none",
    "_hover": {"background_color": ROJO_HOVER},
}

BOTON_SECUNDARIO = {
    "background_color": "transparent",
    "color": BLANCO,
    "border_radius": "6px",
    "padding": "10px 24px",
    "font_weight": "bold",
    "font_family": FUENTE_SECUNDARIA,
    "cursor": "pointer",
    "border": f"1px solid {ROJO_PRINCIPAL}",
    "_hover": {"background_color": ROJO_PRINCIPAL},
}

# ─── ESTILOS DE PÁGINA ───────────────────────────────────────────────
# Estilo base que se aplica al fondo de todas las páginas

PAGINA_BASE = {
    "background_color": NEGRO_FONDO,
    "min_height": "100vh",
    "width": "100%",
    "font_family": FUENTE_SECUNDARIA,
}
