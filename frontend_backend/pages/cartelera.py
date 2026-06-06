# cartelera.py
import reflex as rx
from frontend_backend.components.navbar import navbar
from frontend_backend.components.footer import footer
from frontend_backend.pages.mock_data import PELICULAS
from frontend_backend.styles.theme import (
    NEGRO_FONDO, NEGRO_CARD, ROJO_PRINCIPAL, ROJO_HOVER, BLANCO,
    GRIS_TEXTO, GRIS_BORDE, AMARILLO_ESTRELLAS, BOTON_PRIMARIO,
    FUENTE_PRINCIPAL, FUENTE_SECUNDARIA, TITULO_SECCION, PAGINA_BASE
)


# ─── STATE ────────────────────────────────────────────────────────────
class CarteleraState(rx.State):
    categoria_seleccionada: str = "Todas"

    def set_categoria(self, categoria: str):
        self.categoria_seleccionada = categoria

    @rx.var
    def peliculas_filtradas(self) -> list[dict]:
        if self.categoria_seleccionada == "Todas":
            return PELICULAS
        return [p for p in PELICULAS if p["genero"] == self.categoria_seleccionada]


def clasificacion_badge(clasificacion: str) -> rx.Component:
    colores = {"PG": "#2ecc71", "PG-13": "#f39c12", "R": "#e74c3c"}
    color = colores.get(clasificacion, ROJO_PRINCIPAL)
    return rx.box(
        rx.text(clasificacion, color=BLANCO, font_size="0.7em",
                font_weight="bold", font_family=FUENTE_SECUNDARIA),
        background_color=color, border_radius="4px",
        padding_x="8px", padding_y="2px",
    )


def tarjeta_pelicula(pelicula: dict) -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(src=pelicula["imagen"], width="100%",
                     height="320px", object_fit="cover"),
            rx.box(
                clasificacion_badge(pelicula["clasificacion"]),
                position="absolute", top="10px", right="10px",
            ),
            position="relative", overflow="hidden",
        ),
        rx.vstack(
            rx.text(pelicula["titulo"], color=BLANCO, font_size="1.1em",
                    font_weight="bold", font_family=FUENTE_PRINCIPAL,
                    letter_spacing="1px", no_of_lines=1),
            rx.hstack(
                rx.text(pelicula["genero"], color=ROJO_PRINCIPAL,
                        font_size="0.8em", font_family=FUENTE_SECUNDARIA,
                        font_weight="600"),
                rx.text("•", color=GRIS_BORDE),
                rx.text(pelicula["duracion"], color=GRIS_TEXTO,
                        font_size="0.8em", font_family=FUENTE_SECUNDARIA),
                spacing="2", align="center",
            ),
            rx.hstack(
                rx.text("★", color=AMARILLO_ESTRELLAS, font_size="0.9em"),
                rx.text(f"{pelicula['calificacion']}/5",
                        color=GRIS_TEXTO, font_size="0.8em",
                        font_family=FUENTE_SECUNDARIA),
                spacing="1", align="center",
            ),
            rx.text(pelicula["descripcion"], color=GRIS_TEXTO,
                    font_size="0.82em", font_family=FUENTE_SECUNDARIA,
                    no_of_lines=2, line_height="1.5"),
            rx.link(
                rx.button("Ver Película", width="100%", **BOTON_PRIMARIO),
                href=f"/pelicula/{pelicula['id']}", width="100%",
            ),
            align_items="start", spacing="2", padding="16px", width="100%",
        ),
        background_color=NEGRO_CARD, border_radius="10px",
        overflow="hidden", border=f"1px solid {GRIS_BORDE}",
        width="280px",
        _hover={"border_color": ROJO_PRINCIPAL,
                "transform": "translateY(-4px)",
                "transition": "all 0.3s ease"},
        transition="all 0.3s ease",
    )


def cartelera_page() -> rx.Component:
    categorias = ["Todas", "Drama", "Acción", "Thriller", "Ciencia Ficción"]

    return rx.box(
        navbar(),
        # Header
        rx.box(
            rx.vstack(
                rx.text("CARTELERA", color=BLANCO, font_size="3em",
                        font_weight="bold", font_family=FUENTE_PRINCIPAL,
                        letter_spacing="3px"),
                rx.text(
                    "Cada semana seleccionamos las mejores películas de la historia del cine.",
                    color=GRIS_TEXTO, font_family=FUENTE_SECUNDARIA,
                    font_size="1em", text_align="center",
                ),
                align="center", spacing="2",
            ),
            background_color="#0D0D0D", padding_x="40px", padding_y="50px",
            text_align="center", border_bottom=f"1px solid {GRIS_BORDE}",
        ),
        # Selector de Categorías
        rx.box(
            rx.vstack(
                rx.hstack(
                    *[
                        rx.button(
                            cat,
                            on_click=CarteleraState.set_categoria(cat),
                            background_color=rx.cond(
                                CarteleraState.categoria_seleccionada == cat,
                                ROJO_PRINCIPAL,
                                "transparent",
                            ),
                            color=BLANCO,
                            border=rx.cond(
                                CarteleraState.categoria_seleccionada == cat,
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
                                    CarteleraState.categoria_seleccionada == cat,
                                    ROJO_HOVER,
                                    "#1a1a1a",
                                )
                            },
                        )
                        for cat in categorias
                    ],
                    spacing="3",
                    flex_wrap="wrap",
                    justify="center",
                    width="100%",
                ),
                align="center",
                width="100%",
            ),
            padding_top="40px",
            width="100%",
        ),
        # Grid de películas filtrado
        rx.box(
            rx.flex(
                rx.foreach(
                    CarteleraState.peliculas_filtradas,
                    tarjeta_pelicula
                ),
                flex_wrap="wrap", gap="24px",
                justify_content="center", width="100%",
            ),
            padding_x="40px", padding_y="40px", width="100%",
        ),
        footer(),
        **PAGINA_BASE,
    )
