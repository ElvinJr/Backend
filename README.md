# 🎬 XP Movies — Plataforma Web de Cine (Frontend en Reflex)

Este repositorio contiene la recreación del frontend de la plataforma **XP Movies**, reescrita para ejecutarse bajo el paquete `frontend_backend` y gestionada exclusivamente con **Reflex** y **Poetry**.

A diferencia de los cines tradicionales, XP Movies se especializa en presentar cada semana una cartelera cuidadosamente seleccionada con las **mejores películas de la historia del cine**, para que puedas verlas o revivirlas con la mejor calidad de imagen y sonido.

---

## 📋 Funcionalidades Migradas y Mejoradas

- 🎥 **Cartelera Semanal** con las mejores películas históricas.
- 🏷️ **Filtro Dinámico por Categorías** (Todas, Drama, Acción, Thriller, Ciencia Ficción) en el Inicio y la Cartelera, operando en tiempo real mediante el estado del framework.
- 🔍 **Buscador de Películas** funcional mediante estado reactivo.
- 🎞️ **Fichas de Películas** con detalles e itinerarios de tandas.
- 💺 **Reservas y Asientos Simplificados**: Maquetas de diseño visual que simulan el flujo de selección de asientos y totales, ideal para la integración en la siguiente fase.
- 🔐 **Autenticación Demo**: Modal simplificado para registrarse e iniciar sesión de demostración.
- 📱 **Diseño Responsive** totalmente adaptable a resoluciones móviles y de escritorio.

---

## 🛠️ Tecnologías y Dependencias

- **Reflex (v0.9.3+)**: Framework web completo en Python puro.
- **Poetry**: Gestor de entornos virtuales y dependencias.
- **Pytest**: Entorno de validación de pruebas unitarias.
- **Google Fonts**: Tipografías de diseño *Bebas Neue* e *Inter*.

---

## 🚀 Cómo Instalar y Ejecutar

### Requisitos Previos
- **Python 3.12** o superior
- **Poetry 2.x**

### Pasos de Instalación

1. **Instalar las dependencias del proyecto:**
   Desde la raíz del directorio `Backend`, ejecuta:
   ```bash
   poetry install
   ```
   *Nota: Esto creará automáticamente un entorno virtual seguro y descargará todas las librerías necesarias sin requerir `pip` global.*

2. **Ejecutar las pruebas unitarias básicas:**
   Para verificar la correcta instalación y funcionamiento del entorno:
   ```bash
   poetry run pytest
   ```

3. **Ejecutar el servidor de Reflex en desarrollo:**
   Inicia la aplicación con:
   ```bash
   poetry run reflex run
   ```

4. **Abrir en tu navegador:**
   Visita [http://localhost:3000](http://localhost:3000) para ver y probar la aplicación de forma interactiva.

---

## 📁 Estructura del Repositorio `Backend`

El repositorio está organizado siguiendo los estándares de empaquetado de Python y la estructura nativa de Reflex:

```text
Backend/
├── assets/                     # Recursos estáticos (favicon.ico, etc.)
├── frontend_backend/           # Paquete raíz de la aplicación web
│   ├── components/             # Componentes visuales globales y reutilizables
│   │   ├── auth_modal.py       # Modal de inicio y registro simplificado
│   │   ├── footer.py           # Pie de página de la plataforma
│   │   └── navbar.py           # Barra de navegación superior
│   ├── pages/                  # Páginas y vistas principales de la plataforma
│   │   ├── cartelera.py        # Página del catálogo completo con filtros
│   │   ├── index.py            # Página de Inicio con Hero, Cartelera y Contacto
│   │   ├── mock_data.py        # Datos de prueba de las películas
│   │   ├── pelicula.py         # Ficha detallada de la película y tandas
│   │   └── reservas.py         # Mockup de reserva de asientos
│   ├── styles/                 # Configuración de apariencia
│   │   └── theme.py            # Paleta de colores y variables CSS globales
│   └── frontend_backend.py     # Archivo principal de Reflex con definición de rutas
├── tests/                      # Suite de pruebas automatizadas
│   └── test_app.py             # Prueba básica de arranque de la aplicación
├── pyproject.toml              # Definición de dependencias de Poetry
├── rxconfig.py                 # Configuración global del motor de Reflex
└── README.md                   # Este archivo informativo
```

---

## 🎨 Paleta de Colores Corporativa

| Color | Hexadecimal | Propósito de Uso |
|:---|:---|:---|
| Negro Fondo | `#0A0A0A` | Fondo primario del cuerpo del sitio |
| Negro Componente | `#111111` | Fondos de tarjetas y contenedores de datos |
| Rojo Principal | `#8B0000` | Botones principales y llamadas a la acción |
| Rojo Hover | `#A50000` | Efectos hover al interactuar con el puntero |
| Blanco | `#FFFFFF` | Textos principales |
| Gris | `#AAAAAA` | Descripciones, fechas y textos secundarios |

---

*Proyecto Final — Desarrollo Web | Recreación con Reflex y Poetry*