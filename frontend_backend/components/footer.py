# footer.py
# Este archivo construye el pie de página que aparecerá en todas las páginas.

import reflex as rx
from frontend_backend.styles.theme import (
    NEGRO_NAVBAR, ROJO_PRINCIPAL, BLANCO, GRIS_TEXTO,
    GRIS_BORDE, FUENTE_PRINCIPAL, FUENTE_SECUNDARIA
)


def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            # ── FILA SUPERIOR DEL FOOTER ──────────────────────────
            rx.hstack(
                # Columna 1: Logo y descripción
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "XP",
                            color=ROJO_PRINCIPAL,
                            font_size="1.5em",
                            font_weight="bold",
                            font_family=FUENTE_PRINCIPAL,
                        ),
                        rx.text(
                            "MOVIES",
                            color=BLANCO,
                            font_size="1.5em",
                            font_weight="bold",
                            font_family=FUENTE_PRINCIPAL,
                        ),
                        spacing="1",
                    ),
                    rx.text(
                        "Tu destino favorito para el mejor cine.",
                        color=GRIS_TEXTO,
                        font_size="0.85em",
                        font_family=FUENTE_SECUNDARIA,
                        max_width="220px",
                    ),
                    align_items="start",
                    spacing="3",
                ),

                # Columna 2: Navegación
                rx.vstack(
                    rx.text(
                        "NAVEGACIÓN",
                        color=BLANCO,
                        font_size="0.8em",
                        font_weight="bold",
                        font_family=FUENTE_PRINCIPAL,
                        letter_spacing="1px",
                    ),
                    rx.link("Inicio", href="/", color=GRIS_TEXTO,
                            font_family=FUENTE_SECUNDARIA,
                            font_size="0.9em", text_decoration="none",
                            _hover={"color": BLANCO}),
                    rx.link("Cartelera", href="/cartelera", color=GRIS_TEXTO,
                            font_family=FUENTE_SECUNDARIA,
                            font_size="0.9em", text_decoration="none",
                            _hover={"color": BLANCO}),
                    rx.link("Próximamente", href="/proximamente", color=GRIS_TEXTO,
                            font_family=FUENTE_SECUNDARIA,
                            font_size="0.9em", text_decoration="none",
                            _hover={"color": BLANCO}),
                    align_items="start",
                    spacing="2",
                ),

                # Columna 3: Legal
                rx.vstack(
                    rx.text(
                        "LEGAL",
                        color=BLANCO,
                        font_size="0.8em",
                        font_weight="bold",
                        font_family=FUENTE_PRINCIPAL,
                        letter_spacing="1px",
                    ),
                    rx.link("Términos de uso", href="#", color=GRIS_TEXTO,
                            font_family=FUENTE_SECUNDARIA,
                            font_size="0.9em", text_decoration="none",
                            _hover={"color": BLANCO}),
                    rx.link("Privacidad", href="#", color=GRIS_TEXTO,
                            font_family=FUENTE_SECUNDARIA,
                            font_size="0.9em", text_decoration="none",
                            _hover={"color": BLANCO}),
                    align_items="start",
                    spacing="2",
                ),

                justify="between",
                width="100%",
                flex_wrap="wrap",  # En móvil las columnas se apilan
                gap="40px",
            ),

            # ── LÍNEA DIVISORA ────────────────────────────────────
            rx.divider(border_color=GRIS_BORDE),

            # ── FILA INFERIOR: COPYRIGHT ──────────────────────────
            rx.hstack(
                rx.text(
                    "© 2025 XP Movies. Todos los derechos reservados.",
                    color=GRIS_TEXTO,
                    font_size="0.8em",
                    font_family=FUENTE_SECUNDARIA,
                ),
                justify="center",
                width="100%",
            ),

            spacing="6",
            width="100%",
        ),

        # Estilos del contenedor principal del footer
        background_color=NEGRO_NAVBAR,
        width="100%",
        padding_x="40px",
        padding_y="40px",
        border_top=f"1px solid {GRIS_BORDE}",
        margin_top="auto",
    )
