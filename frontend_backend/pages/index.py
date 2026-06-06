# index.py
# Este archivo construye la Página de Inicio de XP Movies con filtrado dinámico.

import reflex as rx
from frontend_backend.components.navbar import navbar
from frontend_backend.components.footer import footer
from frontend_backend.pages.mock_data import PELICULAS, PROXIMAS_PELICULAS
from frontend_backend.styles.theme import (
    NEGRO_FONDO, NEGRO_CARD, ROJO_PRINCIPAL, ROJO_HOVER,
    BLANCO, GRIS_TEXTO, GRIS_BORDE, AMARILLO_ESTRELLAS,
    BOTON_PRIMARIO, FUENTE_PRINCIPAL, FUENTE_SECUNDARIA,
    TITULO_SECCION, PAGINA_BASE
)


# ─── STATE ────────────────────────────────────────────────────────────
class IndexState(rx.State):
    categoria_seleccionada: str = "Todas"
    termino_busqueda: str = ""
    busqueda_temporal: str = ""

    def set_categoria(self, categoria: str):
        self.categoria_seleccionada = categoria

    def set_busqueda_temporal(self, val: str):
        self.busqueda_temporal = val

    def buscar(self):
        self.termino_busqueda = self.busqueda_temporal

    @rx.var
    def peliculas_filtradas(self) -> list[dict]:
        resultado = PELICULAS
        # Filtrar por categoría
        if self.categoria_seleccionada != "Todas":
            resultado = [p for p in resultado if p["genero"] == self.categoria_seleccionada]
        # Filtrar por búsqueda
        if self.termino_busqueda.strip():
            term = self.termino_busqueda.lower()
            resultado = [p for p in resultado if term in p["titulo"].lower() or term in p["descripcion"].lower()]
        return resultado


# ─── FUNCIÓN HELPER: Badge de clasificación ──────────────────────────
def clasificacion_badge(clasificacion: str) -> rx.Component:
    colores = {
        "PG": "#2ecc71",
        "PG-13": "#f39c12",
        "R": "#e74c3c",
    }
    color = colores.get(clasificacion, ROJO_PRINCIPAL)
    return rx.box(
        rx.text(
            clasificacion,
            color=BLANCO,
            font_size="0.7em",
            font_weight="bold",
            font_family=FUENTE_SECUNDARIA,
        ),
        background_color=color,
        border_radius="4px",
        padding_x="8px",
        padding_y="2px",
    )


# ─── TARJETA DE PELÍCULA ─────────────────────────────────────────────
def tarjeta_pelicula(pelicula: dict) -> rx.Component:
    return rx.box(
        # Imagen de la película
        rx.box(
            rx.image(
                src=pelicula["imagen"],
                width="100%",
                height="320px",
                object_fit="cover",
            ),
            # Badge de clasificación encima de la imagen
            rx.box(
                clasificacion_badge(pelicula["clasificacion"]),
                position="absolute",
                top="10px",
                right="10px",
            ),
            position="relative",
            overflow="hidden",
        ),

        # Información de la película
        rx.vstack(
            # Título
            rx.text(
                pelicula["titulo"],
                color=BLANCO,
                font_size="1.1em",
                font_weight="bold",
                font_family=FUENTE_PRINCIPAL,
                letter_spacing="1px",
                no_of_lines=1,
            ),
            # Género y duración
            rx.hstack(
                rx.text(
                    pelicula["genero"],
                    color=ROJO_PRINCIPAL,
                    font_size="0.8em",
                    font_family=FUENTE_SECUNDARIA,
                    font_weight="600",
                ),
                rx.text("•", color=GRIS_BORDE),
                rx.text(
                    pelicula["duracion"],
                    color=GRIS_TEXTO,
                    font_size="0.8em",
                    font_family=FUENTE_SECUNDARIA,
                ),
                spacing="2",
                align="center",
            ),
            # Calificación (Estrellas estáticas en base al valor)
            rx.hstack(
                rx.text(
                    "★",
                    color=AMARILLO_ESTRELLAS,
                    font_size="0.9em",
                ),
                rx.text(
                    f"{pelicula['calificacion']}/5",
                    color=GRIS_TEXTO,
                    font_size="0.8em",
                    font_family=FUENTE_SECUNDARIA,
                ),
                spacing="1",
                align="center",
            ),
            # Descripción corta
            rx.text(
                pelicula["descripcion"],
                color=GRIS_TEXTO,
                font_size="0.82em",
                font_family=FUENTE_SECUNDARIA,
                no_of_lines=2,
                line_height="1.5",
            ),
            # Botón Ver Película
            rx.link(
                rx.button(
                    "Ver Película",
                    width="100%",
                    **BOTON_PRIMARIO,
                ),
                href=f"/pelicula/{pelicula['id']}",
                width="100%",
            ),
            align_items="start",
            spacing="2",
            padding="16px",
            width="100%",
        ),

        # Estilos de la tarjeta completa
        background_color=NEGRO_CARD,
        border_radius="10px",
        overflow="hidden",
        border=f"1px solid {GRIS_BORDE}",
        width="280px",
        _hover={
            "border_color": ROJO_PRINCIPAL,
            "transform": "translateY(-4px)",
            "transition": "all 0.3s ease",
        },
        transition="all 0.3s ease",
    )


# ─── TARJETA COMING SOON ─────────────────────────────────────────────
def tarjeta_coming_soon(pelicula: dict) -> rx.Component:
    return rx.box(
        # Imagen con overlay oscuro
        rx.box(
            rx.image(
                src=pelicula["imagen"],
                width="100%",
                height="280px",
                object_fit="cover",
                filter="brightness(0.5)",
            ),
            # Texto "PRÓXIMAMENTE" encima de la imagen
            rx.box(
                rx.text(
                    "PRÓXIMAMENTE",
                    color=ROJO_PRINCIPAL,
                    font_size="0.75em",
                    font_weight="bold",
                    font_family=FUENTE_PRINCIPAL,
                    letter_spacing="3px",
                ),
                rx.text(
                    pelicula["titulo"],
                    color=BLANCO,
                    font_size="1.3em",
                    font_weight="bold",
                    font_family=FUENTE_PRINCIPAL,
                    letter_spacing="1px",
                ),
                rx.text(
                    f"Estreno: {pelicula['estreno']}",
                    color=GRIS_TEXTO,
                    font_size="0.85em",
                    font_family=FUENTE_SECUNDARIA,
                ),
                position="absolute",
                bottom="0",
                left="0",
                right="0",
                padding="16px",
                background="linear-gradient(transparent, rgba(0,0,0,0.9))",
            ),
            position="relative",
            overflow="hidden",
        ),

        border_radius="10px",
        overflow="hidden",
        border=f"1px solid {GRIS_BORDE}",
        width="280px",
        _hover={
            "border_color": ROJO_PRINCIPAL,
            "transform": "translateY(-4px)",
            "transition": "all 0.3s ease",
        },
        transition="all 0.3s ease",
    )


# ─── SECCIÓN HERO ────────────────────────────────────────────────────
def seccion_hero() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "LA MEJOR EXPERIENCIA",
                color=ROJO_PRINCIPAL,
                font_size="0.9em",
                font_weight="bold",
                font_family=FUENTE_PRINCIPAL,
                letter_spacing="4px",
            ),
            rx.text(
                "EN EL CINE",
                color=BLANCO,
                font_size="4.5em",
                font_weight="bold",
                font_family=FUENTE_PRINCIPAL,
                letter_spacing="3px",
                line_height="1",
                text_align="center",
            ),
            rx.text(
                "No somos un cine tradicional. Cada semana cubrimos una cartelera con las mejores películas de la historia del cine para que las disfrutes en la mejor calidad.",
                color=GRIS_TEXTO,
                font_size="1.1em",
                font_family=FUENTE_SECUNDARIA,
                text_align="center",
                max_width="500px",
            ),

            # Buscador funcional
            rx.hstack(
                rx.input(
                    placeholder="Buscar película...",
                    value=IndexState.busqueda_temporal,
                    on_change=IndexState.set_busqueda_temporal,
                    background_color="#1a1a1a",
                    color=BLANCO,
                    border=f"1px solid {GRIS_BORDE}",
                    border_radius="6px 0 0 6px",
                    padding="12px 16px",
                    width="320px",
                    font_family=FUENTE_SECUNDARIA,
                    _placeholder={"color": GRIS_TEXTO},
                    _focus={"border_color": ROJO_PRINCIPAL, "outline": "none"},
                ),
                rx.button(
                    "Buscar",
                    on_click=IndexState.buscar,
                    background_color=ROJO_PRINCIPAL,
                    color=BLANCO,
                    border_radius="0 6px 6px 0",
                    padding="12px 24px",
                    font_weight="bold",
                    font_family=FUENTE_SECUNDARIA,
                    cursor="pointer",
                    _hover={"background_color": ROJO_HOVER},
                ),
                spacing="0",
            ),

            spacing="5",
            align="center",
        ),

        background_image="url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1600&h=800&fit=crop')",
        background_size="cover",
        background_position="center",
        width="100%",
        min_height="550px",
        display="flex",
        align_items="center",
        justify_content="center",
        position="relative",
        _before={
            "content": '""',
            "position": "absolute",
            "top": "0",
            "left": "0",
            "right": "0",
            "bottom": "0",
            "background": "rgba(0,0,0,0.7)",
        },
    )


# ─── SECCIÓN CARTELERA CON FILTRO ────────────────────────────────────
def seccion_cartelera() -> rx.Component:
    categorias = ["Todas", "Drama", "Acción", "Thriller", "Ciencia Ficción"]
    
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    width="4px",
                    height="32px",
                    background_color=ROJO_PRINCIPAL,
                    border_radius="2px",
                ),
                rx.text(
                    "EN CARTELERA",
                    **TITULO_SECCION,
                ),
                spacing="3",
                align="center",
            ),
            rx.text(
                "Filtra la cartelera por categorías o realiza búsquedas arriba.",
                color=GRIS_TEXTO,
                font_family=FUENTE_SECUNDARIA,
                font_size="0.95em",
            ),

            # Fila de botones de categorías
            rx.hstack(
                *[
                    rx.button(
                        cat,
                        on_click=IndexState.set_categoria(cat),
                        background_color=rx.cond(
                            IndexState.categoria_seleccionada == cat,
                            ROJO_PRINCIPAL,
                            "transparent",
                        ),
                        color=BLANCO,
                        border=rx.cond(
                            IndexState.categoria_seleccionada == cat,
                            f"1px solid {ROJO_PRINCIPAL}",
                            f"1px solid {GRIS_BORDE}",
                        ),
                        padding="8px 16px",
                        font_size="0.9em",
                        font_weight="bold",
                        border_radius="6px",
                        cursor="pointer",
                        _hover={
                            "background_color": rx.cond(
                                IndexState.categoria_seleccionada == cat,
                                ROJO_HOVER,
                                "#1a1a1a",
                            )
                        },
                    )
                    for cat in categorias
                ],
                spacing="3",
                flex_wrap="wrap",
                margin_bottom="10px",
            ),

            # Grid dinámico de películas
            rx.flex(
                rx.foreach(
                    IndexState.peliculas_filtradas,
                    tarjeta_pelicula
                ),
                flex_wrap="wrap",
                gap="24px",
                justify_content="center",
                width="100%",
            ),

            spacing="6",
            align_items="start",
            width="100%",
        ),
        padding_x="40px",
        padding_y="60px",
        width="100%",
    )


# ─── SECCIÓN COMING SOON ─────────────────────────────────────────────
def seccion_coming_soon() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    width="4px",
                    height="32px",
                    background_color=ROJO_PRINCIPAL,
                    border_radius="2px",
                ),
                rx.text(
                    "PRÓXIMAMENTE",
                    **TITULO_SECCION,
                ),
                spacing="3",
                align="center",
            ),
            rx.text(
                "Las películas que se vienen muy pronto",
                color=GRIS_TEXTO,
                font_family=FUENTE_SECUNDARIA,
                font_size="0.95em",
            ),
            rx.flex(
                *[tarjeta_coming_soon(p) for p in PROXIMAS_PELICULAS],
                flex_wrap="wrap",
                gap="24px",
                justify_content="center",
                width="100%",
            ),
            spacing="6",
            align_items="start",
            width="100%",
        ),
        padding_x="40px",
        padding_y="60px",
        background_color="#0D0D0D",
        width="100%",
    )


# ─── SECCIÓN CONTACTO ────────────────────────────────────────────────
def seccion_contacto() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    width="4px",
                    height="32px",
                    background_color=ROJO_PRINCIPAL,
                    border_radius="2px",
                ),
                rx.text(
                    "CONTACTO",
                    **TITULO_SECCION,
                ),
                spacing="3",
                align="center",
            ),
            rx.flex(
                # Tarjeta: Ubicación
                rx.vstack(
                    rx.text("📍", font_size="2em"),
                    rx.text(
                        "Ubicación",
                        color=BLANCO,
                        font_weight="bold",
                        font_family=FUENTE_PRINCIPAL,
                        font_size="1.1em",
                    ),
                    rx.text(
                        "C. Arzobispo Nouel 210, Santo Domingo 10210, República Dominicana",
                        color=GRIS_TEXTO,
                        font_family=FUENTE_SECUNDARIA,
                        font_size="0.9em",
                        text_align="center",
                    ),
                    align="center",
                    spacing="2",
                    background_color=NEGRO_CARD,
                    padding="30px",
                    border_radius="10px",
                    border=f"1px solid {GRIS_BORDE}",
                    width="250px",
                ),
                # Tarjeta: Horario
                rx.vstack(
                    rx.text("🕐", font_size="2em"),
                    rx.text(
                        "Horario",
                        color=BLANCO,
                        font_weight="bold",
                        font_family=FUENTE_PRINCIPAL,
                        font_size="1.1em",
                    ),
                    rx.text(
                        "Lunes a Domingo\n12:00 PM – 12:00 AM",
                        color=GRIS_TEXTO,
                        font_family=FUENTE_SECUNDARIA,
                        font_size="0.9em",
                        text_align="center",
                        white_space="pre-line",
                    ),
                    align="center",
                    spacing="2",
                    background_color=NEGRO_CARD,
                    padding="30px",
                    border_radius="10px",
                    border=f"1px solid {GRIS_BORDE}",
                    width="250px",
                ),
                # Tarjeta: Teléfono
                rx.vstack(
                    rx.text("📞", font_size="2em"),
                    rx.text(
                        "Teléfono",
                        color=BLANCO,
                        font_weight="bold",
                        font_family=FUENTE_PRINCIPAL,
                        font_size="1.1em",
                    ),
                    rx.text(
                        "(829) 216-3712",
                        color=GRIS_TEXTO,
                        font_family=FUENTE_SECUNDARIA,
                        font_size="0.9em",
                        text_align="center",
                    ),
                    align="center",
                    spacing="2",
                    background_color=NEGRO_CARD,
                    padding="30px",
                    border_radius="10px",
                    border=f"1px solid {GRIS_BORDE}",
                    width="250px",
                ),
                flex_wrap="wrap",
                gap="24px",
                justify_content="center",
                width="100%",
            ),
            spacing="6",
            align_items="start",
            width="100%",
        ),
        padding_x="40px",
        padding_y="60px",
        width="100%",
    )


# ─── PÁGINA COMPLETA ─────────────────────────────────────────────────
def index_page() -> rx.Component:
    return rx.box(
        navbar(),
        seccion_hero(),
        seccion_cartelera(),
        seccion_coming_soon(),
        seccion_contacto(),
        footer(),
        **PAGINA_BASE,
    )
