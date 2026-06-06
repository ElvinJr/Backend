# auth_modal.py
import reflex as rx
from frontend_backend.styles.theme import (
    NEGRO_CARD, ROJO_PRINCIPAL, ROJO_HOVER,
    BLANCO, GRIS_TEXTO, GRIS_BORDE, FUENTE_PRINCIPAL,
    FUENTE_SECUNDARIA, BOTON_PRIMARIO, BOTON_SECUNDARIO
)


class AuthState(rx.State):
    modal_abierto: bool = False
    modo: str = "login"
    usuario_logueado: bool = False  # Mantenido como estático (fase 2 interactivo)
    nombre_usuario: str = "Usuario Demo"

    def abrir_modal(self):
        self.modal_abierto = True
        self.modo = "login"

    def cerrar_modal(self):
        self.modal_abierto = False

    def cambiar_modo(self, nuevo_modo: str):
        self.modo = nuevo_modo

    def simular_login(self):
        # Simula un login simple para permitir visualización en reservas
        self.usuario_logueado = True
        self.modal_abierto = False

    def cerrar_sesion(self):
        self.usuario_logueado = False


def campo_auth(label, placeholder, tipo="text"):
    return rx.vstack(
        rx.text(label, color=BLANCO, font_size="0.85em",
                font_weight="600", font_family=FUENTE_SECUNDARIA),
        rx.input(
            placeholder=placeholder, type=tipo,
            background_color="#1a1a1a", color=BLANCO,
            border=f"1px solid {GRIS_BORDE}", border_radius="6px",
            padding="11px 14px", width="100%",
            font_family=FUENTE_SECUNDARIA, font_size="0.9em",
            _placeholder={"color": GRIS_TEXTO},
            _focus={"border_color": ROJO_PRINCIPAL, "outline": "none"},
        ),
        align_items="start", spacing="1", width="100%",
    )


def formulario_login():
    return rx.vstack(
        rx.vstack(
            rx.text("BIENVENIDO", color=BLANCO, font_size="1.8em",
                    font_weight="bold", font_family=FUENTE_PRINCIPAL,
                    letter_spacing="2px"),
            rx.text("Inicia sesión para reservar tus asientos (Demo)",
                    color=GRIS_TEXTO, font_size="0.85em",
                    font_family=FUENTE_SECUNDARIA),
            spacing="1", align="center",
        ),
        rx.box(width="50px", height="3px",
               background_color=ROJO_PRINCIPAL, border_radius="2px"),
        campo_auth("Correo electrónico", "tu@email.com", "email"),
        campo_auth("Contraseña", "••••••••", "password"),
        # Permite hacer login de prueba en la demo
        rx.button("Iniciar Sesión (Demo)", on_click=AuthState.simular_login, **BOTON_PRIMARIO, width="100%", size="3"),
        rx.hstack(
            rx.divider(border_color=GRIS_BORDE, flex="1"),
            rx.text("o", color=GRIS_TEXTO, font_size="0.8em",
                    font_family=FUENTE_SECUNDARIA, padding_x="10px"),
            rx.divider(border_color=GRIS_BORDE, flex="1"),
            width="100%", align="center",
        ),
        rx.hstack(
            rx.text("¿No tienes cuenta?", color=GRIS_TEXTO,
                    font_size="0.85em", font_family=FUENTE_SECUNDARIA),
            rx.text("Regístrate aquí", color=ROJO_PRINCIPAL,
                    font_size="0.85em", font_family=FUENTE_SECUNDARIA,
                    font_weight="600", cursor="pointer",
                    text_decoration="underline",
                    on_click=AuthState.cambiar_modo("registro"),
                    _hover={"color": ROJO_HOVER}),
            spacing="2", justify="center",
        ),
        spacing="4", width="100%", align="center",
    )


def formulario_registro():
    return rx.vstack(
        rx.vstack(
            rx.text("CREAR CUENTA", color=BLANCO, font_size="1.8em",
                    font_weight="bold", font_family=FUENTE_PRINCIPAL,
                    letter_spacing="2px"),
            rx.text("Regístrate para empezar a reservar (Demo)",
                    color=GRIS_TEXTO, font_size="0.85em",
                    font_family=FUENTE_SECUNDARIA),
            spacing="1", align="center",
        ),
        rx.box(width="50px", height="3px",
               background_color=ROJO_PRINCIPAL, border_radius="2px"),
        campo_auth("Nombre completo", "Juan Pérez"),
        campo_auth("Correo electrónico", "tu@email.com", "email"),
        campo_auth("Contraseña", "••••••••", "password"),
        campo_auth("Confirmar contraseña", "••••••••", "password"),
        rx.button("Crear Cuenta (Demo)", on_click=AuthState.simular_login, **BOTON_PRIMARIO, width="100%", size="3"),
        rx.hstack(
            rx.text("¿Ya tienes cuenta?", color=GRIS_TEXTO,
                    font_size="0.85em", font_family=FUENTE_SECUNDARIA),
            rx.text("Inicia sesión", color=ROJO_PRINCIPAL,
                    font_size="0.85em", font_family=FUENTE_SECUNDARIA,
                    font_weight="600", cursor="pointer",
                    text_decoration="underline",
                    on_click=AuthState.cambiar_modo("login"),
                    _hover={"color": ROJO_HOVER}),
            spacing="2", justify="center",
        ),
        spacing="4", width="100%", align="center",
    )


def auth_modal():
    return rx.cond(
        AuthState.modal_abierto,
        rx.box(
            # Fondo oscuro detrás del modal
            rx.box(
                position="fixed",
                top="0", left="0", right="0", bottom="0",
                background="rgba(0,0,0,0.85)",
                z_index="200",
                on_click=AuthState.cerrar_modal,
            ),
            # Caja del modal
            rx.box(
                rx.box(
                    rx.text("✕", color=GRIS_TEXTO, font_size="1.2em",
                            cursor="pointer", on_click=AuthState.cerrar_modal,
                            _hover={"color": BLANCO}),
                    position="absolute", top="16px", right="20px",
                ),
                rx.hstack(
                    rx.text("XP", color=ROJO_PRINCIPAL, font_size="1.4em",
                            font_weight="bold", font_family=FUENTE_PRINCIPAL,
                            letter_spacing="2px"),
                    rx.text("MOVIES", color=BLANCO, font_size="1.4em",
                            font_weight="bold", font_family=FUENTE_PRINCIPAL,
                            letter_spacing="2px"),
                    spacing="1", justify="center", margin_bottom="20px",
                ),
                rx.cond(
                    AuthState.modo == "login",
                    formulario_login(),
                    formulario_registro(),
                ),
                background_color=NEGRO_CARD,
                border=f"1px solid {GRIS_BORDE}",
                border_radius="14px",
                padding="36px",
                width="420px",
                max_width="95vw",
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="201",
            ),
        ),
        rx.fragment(),
    )
