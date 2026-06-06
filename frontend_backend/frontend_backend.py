# frontend_backend.py
import reflex as rx
from frontend_backend.pages.index import index_page
from frontend_backend.pages.cartelera import cartelera_page
from frontend_backend.pages.proximamente import proximamente_page
from frontend_backend.pages.pelicula import (
    pelicula_1, pelicula_2, pelicula_3, pelicula_4,
    pelicula_5, pelicula_6, pelicula_7, pelicula_8,
)
from frontend_backend.pages.reservas import (
    reservas_1_1, reservas_1_2, reservas_1_3,
    reservas_2_1, reservas_2_2, reservas_2_3,
    reservas_3_1, reservas_3_2, reservas_3_3,
    reservas_4_1, reservas_4_2, reservas_4_3,
    reservas_5_1, reservas_5_2, reservas_5_3,
    reservas_6_1, reservas_6_2, reservas_6_3,
    reservas_7_1, reservas_7_2, reservas_7_3,
    reservas_8_1, reservas_8_2, reservas_8_3,
)

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap",
    ],
)

app.add_page(index_page, route="/")
app.add_page(cartelera_page, route="/cartelera")
app.add_page(proximamente_page, route="/proximamente")

app.add_page(pelicula_1, route="/pelicula/1")
app.add_page(pelicula_2, route="/pelicula/2")
app.add_page(pelicula_3, route="/pelicula/3")
app.add_page(pelicula_4, route="/pelicula/4")
app.add_page(pelicula_5, route="/pelicula/5")
app.add_page(pelicula_6, route="/pelicula/6")
app.add_page(pelicula_7, route="/pelicula/7")
app.add_page(pelicula_8, route="/pelicula/8")

app.add_page(reservas_1_1, route="/reservas/1/1")
app.add_page(reservas_1_2, route="/reservas/1/2")
app.add_page(reservas_1_3, route="/reservas/1/3")
app.add_page(reservas_2_1, route="/reservas/2/1")
app.add_page(reservas_2_2, route="/reservas/2/2")
app.add_page(reservas_2_3, route="/reservas/2/3")
app.add_page(reservas_3_1, route="/reservas/3/1")
app.add_page(reservas_3_2, route="/reservas/3/2")
app.add_page(reservas_3_3, route="/reservas/3/3")
app.add_page(reservas_4_1, route="/reservas/4/1")
app.add_page(reservas_4_2, route="/reservas/4/2")
app.add_page(reservas_4_3, route="/reservas/4/3")
app.add_page(reservas_5_1, route="/reservas/5/1")
app.add_page(reservas_5_2, route="/reservas/5/2")
app.add_page(reservas_5_3, route="/reservas/5/3")
app.add_page(reservas_6_1, route="/reservas/6/1")
app.add_page(reservas_6_2, route="/reservas/6/2")
app.add_page(reservas_6_3, route="/reservas/6/3")
app.add_page(reservas_7_1, route="/reservas/7/1")
app.add_page(reservas_7_2, route="/reservas/7/2")
app.add_page(reservas_7_3, route="/reservas/7/3")
app.add_page(reservas_8_1, route="/reservas/8/1")
app.add_page(reservas_8_2, route="/reservas/8/2")
app.add_page(reservas_8_3, route="/reservas/8/3")
