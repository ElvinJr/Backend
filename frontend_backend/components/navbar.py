# navbar.py
import reflex as rx
from frontend_backend.styles.theme import (
    NEGRO_NAVBAR, ROJO_PRINCIPAL, BLANCO, GRIS_TEXTO,
    BOTON_PRIMARIO, BOTON_SECUNDARIO, FUENTE_PRINCIPAL, FUENTE_SECUNDARIA
)
from frontend_backend.components.auth_modal import AuthState, auth_modal


def navbar() -> rx.Component:
    return rx.box(
        # El modal va aquí para que esté disponible en todas las páginas
        auth_modal(),

        rx.hstack(
            # ── LOGO ──────────────────────────────────────────────
            rx.link(
                rx.hstack(
                    rx.text("XP", color=ROJO_PRINCIPAL, font_size="1.8em",
                            font_weight="bold", font_family=FUENTE_PRINCIPAL,
                            letter_spacing="2px"),
                    rx.text("MOVIES", color=BLANCO, font_size="1.8em",
                            font_weight="bold", font_family=FUENTE_PRINCIPAL,
                            letter_spacing="2px"),
                    spacing="1",
                ),
                href="/", text_decoration="none",
            ),

            # ── MENÚ ──────────────────────────────────────────────
            rx.hstack(
                rx.link("Inicio", href="/", color=GRIS_TEXTO,
                        font_family=FUENTE_SECUNDARIA, font_size="0.95em",
                        text_decoration="none", _hover={"color": BLANCO}),
                rx.link("Cartelera", href="/cartelera", color=GRIS_TEXTO,
                        font_family=FUENTE_SECUNDARIA, font_size="0.95em",
                        text_decoration="none", _hover={"color": BLANCO}),
                rx.link("Próximamente", href="/proximamente", color=GRIS_TEXTO,
                        font_family=FUENTE_SECUNDARIA, font_size="0.95em",
                        text_decoration="none", _hover={"color": BLANCO}),
                spacing="6",
                display=["none", "none", "flex"],
            ),

            # ── BOTONES DE SESIÓN ─────────────────────────────────
            # rx.cond muestra botones distintos según si hay sesión o no
            rx.cond(
                AuthState.usuario_logueado,

                # Usuario logueado: muestra nombre y botón cerrar sesión
                rx.hstack(
                    rx.text(
                        "👤 " + AuthState.nombre_usuario,
                        color=BLANCO,
                        font_family=FUENTE_SECUNDARIA,
                        font_size="0.9em",
                        font_weight="600",
                    ),
                    rx.button(
                        "Cerrar Sesión",
                        on_click=AuthState.cerrar_sesion,
                        background_color="transparent",
                        color=GRIS_TEXTO,
                        border=f"1px solid {GRIS_TEXTO}",
                        border_radius="6px",
                        padding="8px 16px",
                        font_size="0.85em",
                        font_family=FUENTE_SECUNDARIA,
                        cursor="pointer",
                        _hover={"color": BLANCO, "border_color": BLANCO},
                    ),
                    spacing="3", align="center",
                ),

                # Usuario NO logueado: muestra Registrarse e Iniciar Sesión
                rx.hstack(
                    rx.button(
                        "Registrarse",
                        on_click=AuthState.abrir_modal,
                        **BOTON_SECUNDARIO,
                        size="2",
                    ),
                    rx.button(
                        "Iniciar Sesión",
                        on_click=AuthState.abrir_modal,
                        **BOTON_PRIMARIO,
                        size="2",
                    ),
                    spacing="3",
                ),
            ),

            justify="between",
            align="center",
            width="100%",
            padding_x="40px",
            padding_y="16px",
        ),

        background_color=NEGRO_NAVBAR,
        width="100%",
        position="sticky",
        top="0",
        z_index="100",
        border_bottom="1px solid #1a1a1a",
    )
