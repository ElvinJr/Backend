# pelicula.py
import reflex as rx
from frontend_backend.components.navbar import navbar
from frontend_backend.components.footer import footer
from frontend_backend.pages.mock_data import PELICULAS
from frontend_backend.styles.theme import (
    NEGRO_FONDO, NEGRO_CARD, ROJO_PRINCIPAL, ROJO_HOVER,
    BLANCO, GRIS_TEXTO, GRIS_BORDE, AMARILLO_ESTRELLAS,
    BOTON_PRIMARIO, BOTON_SECUNDARIO, FUENTE_PRINCIPAL,
    FUENTE_SECUNDARIA, TITULO_SECCION, PAGINA_BASE
)


class PeliculaState(rx.State):
    pelicula_id: int = 1

    @rx.var
    def pelicula_actual(self) -> dict:
        for p in PELICULAS:
            if p["id"] == self.pelicula_id:
                return p
        return PELICULAS[0]

    def set_pelicula(self, pid: int):
        self.pelicula_id = pid


def badge_clasificacion(clasificacion: str) -> rx.Component:
    colores = {"PG": "#2ecc71", "PG-13": "#f39c12", "R": "#e74c3c"}
    color = colores.get(clasificacion, ROJO_PRINCIPAL)
    return rx.box(
        rx.text(clasificacion, color=BLANCO, font_size="0.85em",
                font_weight="bold", font_family=FUENTE_SECUNDARIA),
        background_color=color, border_radius="4px",
        padding_x="10px", padding_y="4px", display="inline-block",
    )


def hero_pelicula(pelicula: dict) -> rx.Component:
    return rx.box(
        rx.box(
            rx.vstack(
                rx.text(pelicula["genero"].upper(), color=ROJO_PRINCIPAL,
                        font_size="0.9em", font_weight="bold",
                        font_family=FUENTE_PRINCIPAL, letter_spacing="4px"),
                rx.text(pelicula["titulo"].upper(), color=BLANCO,
                        font_size="3.5em", font_weight="bold",
                        font_family=FUENTE_PRINCIPAL, letter_spacing="2px",
                        line_height="1", text_align="center"),
                rx.hstack(
                    rx.text(str(pelicula["anio"]), color=GRIS_TEXTO,
                            font_family=FUENTE_SECUNDARIA, font_size="0.95em"),
                    rx.text("•", color=GRIS_BORDE),
                    rx.text(pelicula["duracion"], color=GRIS_TEXTO,
                            font_family=FUENTE_SECUNDARIA, font_size="0.95em"),
                    rx.text("•", color=GRIS_BORDE),
                    badge_clasificacion(pelicula["clasificacion"]),
                    spacing="3", align="center",
                ),
                rx.hstack(
                    rx.text("★", color=AMARILLO_ESTRELLAS, font_size="1.2em"),
                    rx.text(f"{pelicula['calificacion']}/5",
                            color=GRIS_TEXTO, font_family=FUENTE_SECUNDARIA),
                    spacing="2", align="center",
                ),
                # Botón de reservar va a la primera tanda por defecto
                rx.link(
                    rx.button("🎬  Reservar Asientos", **BOTON_PRIMARIO, size="3"),
                    href=f"/reservas/{pelicula['id']}/1",
                ),
                spacing="4", align="center",
            ),
            position="absolute", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            background="rgba(0,0,0,0.75)",
        ),
        background_image=f"url('{pelicula['imagen']}')",
        background_size="cover", background_position="center top",
        width="100%", height="550px", position="relative",
    )


def seccion_descripcion(pelicula: dict) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.box(
                rx.image(src=pelicula["imagen"], width="300px", height="450px",
                         object_fit="cover", border_radius="10px",
                         border=f"2px solid {GRIS_BORDE}"),
                flex_shrink="0",
            ),
            rx.vstack(
                rx.hstack(
                    rx.box(width="4px", height="32px",
                           background_color=ROJO_PRINCIPAL, border_radius="2px"),
                    rx.text("DESCRIPCIÓN GENERAL", **TITULO_SECCION),
                    spacing="3", align="center",
                ),
                rx.text(pelicula["descripcion"], color=GRIS_TEXTO,
                        font_family=FUENTE_SECUNDARIA, font_size="1em",
                        line_height="1.8"),
                rx.box(
                    rx.text("¿Por qué esta película?", color=BLANCO,
                            font_weight="bold", font_family=FUENTE_PRINCIPAL,
                            font_size="1.1em", letter_spacing="1px",
                            margin_bottom="8px"),
                    rx.text(
                        "En XP Movies no proyectamos estrenos. Nos especializamos en traer "
                        "cada semana una cartelera cuidadosamente seleccionada con las mejores "
                        "películas de la historia del cine, para que puedas verlas o revivirlas "
                        "con la mejor calidad de imagen y sonido.",
                        color=GRIS_TEXTO, font_family=FUENTE_SECUNDARIA,
                        font_size="0.9em", line_height="1.8",
                    ),
                    background_color=NEGRO_CARD,
                    border_left=f"3px solid {ROJO_PRINCIPAL}",
                    border_radius="0 8px 8px 0", padding="20px",
                    margin_top="10px",
                ),
                align_items="start", spacing="4", flex="1",
            ),
            gap="50px", flex_wrap="wrap", align_items="start", width="100%",
        ),
        padding_x="40px", padding_y="60px", width="100%",
    )


def seccion_detalles(pelicula: dict) -> rx.Component:
    def fila(etiqueta, valor):
        return rx.hstack(
            rx.text(etiqueta, color=GRIS_TEXTO, font_family=FUENTE_SECUNDARIA,
                    font_size="0.9em", width="140px", flex_shrink="0"),
            rx.text(valor, color=BLANCO, font_family=FUENTE_SECUNDARIA,
                    font_size="0.9em", font_weight="600"),
            border_bottom=f"1px solid {GRIS_BORDE}",
            padding_y="12px", width="100%",
        )
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(width="4px", height="32px",
                       background_color=ROJO_PRINCIPAL, border_radius="2px"),
                rx.text("DETALLES", **TITULO_SECCION),
                spacing="3", align="center",
            ),
            rx.box(
                fila("Título", pelicula["titulo"]),
                fila("Año", str(pelicula["anio"])),
                fila("Género", pelicula["genero"]),
                fila("Duración", pelicula["duracion"]),
                fila("Clasificación", pelicula["clasificacion"]),
                fila("Calificación", f"{pelicula['calificacion']}/5"),
                width="100%", max_width="600px",
            ),
            align_items="start", spacing="5", width="100%",
        ),
        background_color="#0D0D0D", padding_x="40px",
        padding_y="60px", width="100%",
    )


def seccion_itinerario(pelicula: dict) -> rx.Component:
    def tarjeta_tanda(tanda: str, idx: int) -> rx.Component:
        return rx.box(
            rx.vstack(
                rx.text("🎬", font_size="2em"),
                rx.text(tanda, color=BLANCO, font_size="1.3em",
                        font_weight="bold", font_family=FUENTE_PRINCIPAL,
                        letter_spacing="1px"),
                rx.text("Asientos disponibles", color=GRIS_TEXTO,
                        font_size="0.8em", font_family=FUENTE_SECUNDARIA),
                rx.link(
                    rx.button("Seleccionar", **BOTON_PRIMARIO, width="100%"),
                    href=f"/reservas/{pelicula['id']}/{idx + 1}",
                    width="100%",
                ),
                align="center", spacing="3", width="100%",
            ),
            background_color=NEGRO_CARD, border=f"1px solid {GRIS_BORDE}",
            border_radius="10px", padding="24px", width="200px",
            _hover={"border_color": ROJO_PRINCIPAL,
                    "transform": "translateY(-4px)",
                    "transition": "all 0.3s ease"},
            transition="all 0.3s ease",
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(width="4px", height="32px",
                       background_color=ROJO_PRINCIPAL, border_radius="2px"),
                rx.text("ITINERARIO DE TANDAS", **TITULO_SECCION),
                spacing="3", align="center",
            ),
            rx.text("Selecciona la tanda de tu preferencia para reservar tus asientos",
                    color=GRIS_TEXTO, font_family=FUENTE_SECUNDARIA,
                    font_size="0.95em"),
            rx.flex(
                *[tarjeta_tanda(t, i) for i, t in enumerate(pelicula["tandas"])],
                gap="24px", flex_wrap="wrap",
                justify_content="center", width="100%",
            ),
            align_items="start", spacing="5", width="100%",
        ),
        padding_x="40px", padding_y="60px", width="100%",
    )


def seccion_relacionadas(pelicula_actual_id: int) -> rx.Component:
    otras = [p for p in PELICULAS if p["id"] != pelicula_actual_id][:3]

    def mini_tarjeta(p: dict) -> rx.Component:
        return rx.link(
            rx.box(
                rx.image(src=p["imagen"], width="100%", height="200px",
                         object_fit="cover"),
                rx.box(
                    rx.text(p["titulo"], color=BLANCO,
                            font_family=FUENTE_PRINCIPAL, font_size="1em",
                            letter_spacing="1px", no_of_lines=1),
                    rx.text(p["genero"], color=ROJO_PRINCIPAL,
                            font_family=FUENTE_SECUNDARIA, font_size="0.8em"),
                    padding="12px",
                ),
                background_color=NEGRO_CARD, border_radius="10px",
                overflow="hidden", border=f"1px solid {GRIS_BORDE}",
                width="220px",
                _hover={"border_color": ROJO_PRINCIPAL,
                        "transform": "translateY(-4px)",
                        "transition": "all 0.3s ease"},
                transition="all 0.3s ease",
            ),
            href=f"/pelicula/{p['id']}",
            text_decoration="none",
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(width="4px", height="32px",
                       background_color=ROJO_PRINCIPAL, border_radius="2px"),
                rx.text("TAMBIÉN EN CARTELERA", **TITULO_SECCION),
                spacing="3", align="center",
            ),
            rx.flex(
                *[mini_tarjeta(p) for p in otras],
                gap="24px", flex_wrap="wrap",
                justify_content="center", width="100%",
            ),
            align_items="start", spacing="5", width="100%",
        ),
        background_color="#0D0D0D", padding_x="40px",
        padding_y="60px", width="100%",
    )


def pelicula_page_by_index(idx: int) -> rx.Component:
    return rx.box(
        navbar(),
        hero_pelicula(PELICULAS[idx]),
        seccion_descripcion(PELICULAS[idx]),
        seccion_detalles(PELICULAS[idx]),
        seccion_itinerario(PELICULAS[idx]),
        seccion_relacionadas(PELICULAS[idx]["id"]),
        footer(),
        **PAGINA_BASE
    )

def pelicula_1(): return pelicula_page_by_index(0)
def pelicula_2(): return pelicula_page_by_index(1)
def pelicula_3(): return pelicula_page_by_index(2)
def pelicula_4(): return pelicula_page_by_index(3)
def pelicula_5(): return pelicula_page_by_index(4)
def pelicula_6(): return pelicula_page_by_index(5)
def pelicula_7(): return pelicula_page_by_index(6)
def pelicula_8(): return pelicula_page_by_index(7)
