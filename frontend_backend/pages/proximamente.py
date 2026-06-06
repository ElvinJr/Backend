# proximamente.py
import reflex as rx
from frontend_backend.components.navbar import navbar
from frontend_backend.components.footer import footer
from frontend_backend.pages.mock_data import PROXIMAS_PELICULAS
from frontend_backend.styles.theme import (
    NEGRO_FONDO, NEGRO_CARD, ROJO_PRINCIPAL, BLANCO,
    GRIS_TEXTO, GRIS_BORDE, FUENTE_PRINCIPAL,
    FUENTE_SECUNDARIA, PAGINA_BASE
)


def tarjeta_proximamente(pelicula: dict) -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(src=pelicula["imagen"], width="100%",
                     height="380px", object_fit="cover",
                     filter="brightness(0.5)"),
            rx.box(
                rx.text("PRÓXIMAMENTE", color=ROJO_PRINCIPAL,
                        font_size="0.75em", font_weight="bold",
                        font_family=FUENTE_PRINCIPAL, letter_spacing="3px"),
                rx.text(pelicula["titulo"], color=BLANCO,
                        font_size="1.4em", font_weight="bold",
                        font_family=FUENTE_PRINCIPAL, letter_spacing="1px"),
                rx.hstack(
                    rx.text(pelicula["genero"], color=GRIS_TEXTO,
                            font_size="0.85em", font_family=FUENTE_SECUNDARIA),
                    rx.text("•", color=GRIS_BORDE),
                    rx.text(pelicula["clasificacion"], color=GRIS_TEXTO,
                            font_size="0.85em", font_family=FUENTE_SECUNDARIA),
                    spacing="2", align="center",
                ),
                rx.hstack(
                    rx.text("🗓️", font_size="0.9em"),
                    rx.text(f"Estreno: {pelicula['estreno']}",
                            color=BLANCO, font_size="0.9em",
                            font_family=FUENTE_SECUNDARIA, font_weight="600"),
                    spacing="2", align="center",
                ),
                position="absolute", bottom="0", left="0", right="0",
                padding="20px",
                background="linear-gradient(transparent, rgba(0,0,0,0.95))",
            ),
            position="relative", overflow="hidden",
        ),
        background_color=NEGRO_CARD, border_radius="10px",
        overflow="hidden", border=f"1px solid {GRIS_BORDE}",
        width="300px",
        _hover={"border_color": ROJO_PRINCIPAL,
                "transform": "translateY(-4px)",
                "transition": "all 0.3s ease"},
        transition="all 0.3s ease",
    )


def proximamente_page() -> rx.Component:
    return rx.box(
        navbar(),
        # Header
        rx.box(
            rx.vstack(
                rx.text("PRÓXIMAMENTE", color=BLANCO, font_size="3em",
                        font_weight="bold", font_family=FUENTE_PRINCIPAL,
                        letter_spacing="3px"),
                rx.text(
                    "Las películas que llegan muy pronto a XP Movies.",
                    color=GRIS_TEXTO, font_family=FUENTE_SECUNDARIA,
                    font_size="1em", text_align="center",
                ),
                align="center", spacing="2",
            ),
            background_color="#0D0D0D", padding_x="40px", padding_y="50px",
            text_align="center", border_bottom=f"1px solid {GRIS_BORDE}",
        ),
        # Tarjetas
        rx.box(
            rx.flex(
                *[tarjeta_proximamente(p) for p in PROXIMAS_PELICULAS],
                flex_wrap="wrap", gap="30px",
                justify_content="center", width="100%",
            ),
            padding_x="40px", padding_y="60px", width="100%",
        ),
        footer(),
        **PAGINA_BASE,
    )
