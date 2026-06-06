# reservas.py
import reflex as rx
from frontend_backend.components.navbar import navbar
from frontend_backend.components.footer import footer
from frontend_backend.components.auth_modal import AuthState
from frontend_backend.pages.mock_data import PELICULAS
from frontend_backend.styles.theme import (
    NEGRO_FONDO, NEGRO_CARD, ROJO_PRINCIPAL, ROJO_HOVER,
    BLANCO, GRIS_TEXTO, GRIS_BORDE, FUENTE_PRINCIPAL,
    FUENTE_SECUNDARIA, TITULO_SECCION, BOTON_PRIMARIO,
    BOTON_SECUNDARIO, PAGINA_BASE
)

FILAS = ["A", "B", "C", "D", "E"]
COLUMNAS = list(range(1, 9))
PRECIO_ASIENTO = 350


class ReservasState(rx.State):
    nombre: str = ""
    email: str = ""
    telefono: str = ""

    def set_nombre(self, value: str): self.nombre = value
    def set_email(self, value: str): self.email = value
    def set_telefono(self, value: str): self.telefono = value


def leyenda_asientos() -> rx.Component:
    def item(color, texto):
        return rx.hstack(
            rx.box(width="18px", height="18px", background_color=color,
                   border_radius="4px", flex_shrink="0"),
            rx.text(texto, color=GRIS_TEXTO, font_family=FUENTE_SECUNDARIA,
                    font_size="0.8em"),
            spacing="2", align="center",
        )
    return rx.hstack(
        item("#1a1a1a", "Disponible"),
        item(ROJO_PRINCIPAL, "Seleccionado"),
        item("#444444", "Ocupado"),
        spacing="4", justify_content="center",
    )


def mapa_asientos_estatico() -> rx.Component:
    # Genera una matriz de asientos estática (maqueta)
    # Algunos asientos específicos se verán seleccionados/ocupados para simular el diseño
    asientos_seleccionados_demo = ["B3", "B4"]
    asientos_ocupados_demo = ["A1", "A5", "C2", "D7"]

    def asiento_demo(fila: str, col: int) -> rx.Component:
        codigo = f"{fila}{col}"
        es_seleccionado = codigo in asientos_seleccionados_demo
        es_ocupado = codigo in asientos_ocupados_demo

        bg_color = rx.cond(
            es_ocupado,
            "#2a2a2a",
            rx.cond(es_seleccionado, ROJO_PRINCIPAL, "#1a1a1a")
        )
        border_color = rx.cond(
            es_seleccionado,
            ROJO_HOVER,
            GRIS_BORDE
        )
        text_color = rx.cond(
            es_ocupado,
            "#666666",
            rx.cond(es_seleccionado, BLANCO, GRIS_TEXTO)
        )

        return rx.box(
            rx.text(codigo, font_size="0.55em", color=text_color,
                    font_family=FUENTE_SECUNDARIA),
            width="38px", height="34px",
            background_color=bg_color,
            border_radius="5px 5px 3px 3px",
            border=f"1px solid {border_color}",
            display="flex", align_items="center", justify_content="center",
            cursor="default",
            title=f"Asiento {codigo} (Demo)",
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(width="4px", height="24px",
                       background_color=ROJO_PRINCIPAL, border_radius="2px"),
                rx.text("MAPA DE ASIENTOS (DEMO)", **TITULO_SECCION),
                spacing="3", align="center",
            ),
            rx.box(
                rx.text("🎬  PANTALLA", color=GRIS_TEXTO, font_size="0.85em",
                        font_family=FUENTE_PRINCIPAL, letter_spacing="4px"),
                width="100%", max_width="400px", text_align="center",
                padding_y="8px",
                background="linear-gradient(180deg, #333333 0%, #1a1a1a 100%)",
                border_radius="4px", margin_bottom="15px",
            ),
            leyenda_asientos(),
            rx.vstack(
                *[
                    rx.hstack(
                        rx.text(fila, color=GRIS_TEXTO, font_size="0.8em",
                                font_family=FUENTE_SECUNDARIA,
                                width="15px", text_align="center"),
                        *[asiento_demo(fila, col) for col in COLUMNAS],
                        spacing="2", align="center",
                    )
                    for fila in FILAS
                ],
                spacing="2",
            ),
            spacing="4", align="center", width="100%",
        ),
        background_color=NEGRO_CARD, border=f"1px solid {GRIS_BORDE}",
        border_radius="12px", padding="24px", overflow_x="auto",
    )


def formulario_contacto_estatico() -> rx.Component:
    def campo(label, placeholder, value, on_change, tipo="text"):
        return rx.vstack(
            rx.text(label, color=BLANCO, font_size="0.85em",
                    font_weight="600", font_family=FUENTE_SECUNDARIA),
            rx.input(
                placeholder=placeholder, value=value,
                on_change=on_change, type=tipo,
                background_color="#1a1a1a", color=BLANCO,
                border=f"1px solid {GRIS_BORDE}", border_radius="6px",
                padding="10px 14px", width="100%",
                font_family=FUENTE_SECUNDARIA, font_size="0.9em",
                _placeholder={"color": GRIS_TEXTO},
                _focus={"border_color": ROJO_PRINCIPAL, "outline": "none"},
            ),
            align_items="start", spacing="1", width="100%",
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(width="4px", height="24px",
                       background_color=ROJO_PRINCIPAL, border_radius="2px"),
                rx.text("DATOS DE RESERVA", **TITULO_SECCION),
                spacing="3", align="center",
            ),
            campo("Nombre completo", "Ej: Juan Pérez",
                  ReservasState.nombre, ReservasState.set_nombre),
            campo("Correo electrónico", "Ej: juan@email.com",
                  ReservasState.email, ReservasState.set_email, "email"),
            campo("Teléfono", "Ej: 809-555-0000",
                  ReservasState.telefono, ReservasState.set_telefono, "tel"),
            align_items="start", spacing="4", width="100%",
        ),
        background_color=NEGRO_CARD, border=f"1px solid {GRIS_BORDE}",
        border_radius="12px", padding="24px", width="100%",
    )


def resumen_pago_estatico(pelicula: dict, tanda: str) -> rx.Component:
    def fila(etiqueta, valor):
        return rx.hstack(
            rx.text(etiqueta, color=GRIS_TEXTO, font_family=FUENTE_SECUNDARIA,
                    font_size="0.85em"),
            rx.text(valor, color=BLANCO, font_family=FUENTE_SECUNDARIA,
                    font_size="0.85em", font_weight="600"),
            justify="between", width="100%",
            border_bottom=f"1px solid {GRIS_BORDE}", padding_y="8px",
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(width="4px", height="24px",
                       background_color=ROJO_PRINCIPAL, border_radius="2px"),
                rx.text("RESUMEN DE PAGO", **TITULO_SECCION),
                spacing="3", align="center",
            ),
            fila("Película", pelicula["titulo"]),
            fila("Tanda", tanda),
            fila("Asientos", "B3, B4 (Demo)"),
            fila("Cantidad", "2 asiento(s)"),
            fila("Precio por asiento", f"RD$ {PRECIO_ASIENTO}"),
            rx.hstack(
                rx.text("TOTAL", color=BLANCO, font_family=FUENTE_PRINCIPAL,
                        font_size="1.1em", font_weight="bold",
                        letter_spacing="1px"),
                rx.text(
                    "RD$ 700",
                    color=ROJO_PRINCIPAL, font_family=FUENTE_PRINCIPAL,
                    font_size="1.3em", font_weight="bold",
                ),
                justify="between", width="100%", padding_top="10px",
            ),
            rx.button(
                "Confirmar Reserva (Demo)", **BOTON_PRIMARIO,
                width="100%", size="3", margin_top="10px",
            ),
            align_items="start", spacing="2", width="100%",
        ),
        background_color=NEGRO_CARD, border=f"1px solid {GRIS_BORDE}",
        border_radius="12px", padding="24px", width="100%",
    )


def reservas_page(pelicula: dict, tanda: str) -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.text("RESERVA TUS ASIENTOS", color=BLANCO,
                        font_size="2.5em", font_weight="bold",
                        font_family=FUENTE_PRINCIPAL, letter_spacing="2px"),
                rx.text(
                    f"{pelicula['titulo']}  •  {tanda}",
                    color=GRIS_TEXTO, font_family=FUENTE_SECUNDARIA,
                    font_size="1em",
                ),
                align="center", spacing="2",
            ),
            background_color="#0D0D0D", padding_x="40px", padding_y="40px",
            text_align="center", border_bottom=f"1px solid {GRIS_BORDE}",
        ),

        # En esta maqueta simplificada, mostramos el mapa directamente
        rx.box(
            rx.flex(
                rx.box(mapa_asientos_estatico(), flex="2", min_width="300px"),
                rx.vstack(
                    formulario_contacto_estatico(),
                    resumen_pago_estatico(pelicula, tanda),
                    spacing="6", flex="1", min_width="300px",
                ),
                gap="30px", flex_wrap="wrap",
                align_items="start", width="100%",
            ),
            padding_x="40px", padding_y="50px", width="100%",
        ),

        footer(),
        **PAGINA_BASE,
    )


def _pagina(pid: int, tidx: int) -> rx.Component:
    p = PELICULAS[pid - 1]
    tanda = p["tandas"][tidx]
    return reservas_page(p, tanda)

# 3 tandas por cada una de las 8 películas
def reservas_1_1(): return _pagina(1, 0)
def reservas_1_2(): return _pagina(1, 1)
def reservas_1_3(): return _pagina(1, 2)
def reservas_2_1(): return _pagina(2, 0)
def reservas_2_2(): return _pagina(2, 1)
def reservas_2_3(): return _pagina(2, 2)
def reservas_3_1(): return _pagina(3, 0)
def reservas_3_2(): return _pagina(3, 1)
def reservas_3_3(): return _pagina(3, 2)
def reservas_4_1(): return _pagina(4, 0)
def reservas_4_2(): return _pagina(4, 1)
def reservas_4_3(): return _pagina(4, 2)
def reservas_5_1(): return _pagina(5, 0)
def reservas_5_2(): return _pagina(5, 1)
def reservas_5_3(): return _pagina(5, 2)
def reservas_6_1(): return _pagina(6, 0)
def reservas_6_2(): return _pagina(6, 1)
def reservas_6_3(): return _pagina(6, 2)
def reservas_7_1(): return _pagina(7, 0)
def reservas_7_2(): return _pagina(7, 1)
def reservas_7_3(): return _pagina(7, 2)
def reservas_8_1(): return _pagina(8, 0)
def reservas_8_2(): return _pagina(8, 1)
def reservas_8_3(): return _pagina(8, 2)
