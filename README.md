# 🎬 XP Movies — Plataforma Web de Cine

![XP Movies](https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1200\&h=400\&fit=crop)

## 📋 Descripción del Proyecto

**XP Movies** es una plataforma web de cine desarrollada con **Reflex** y **Python**, cuyo objetivo es ofrecer una experiencia única: en lugar de proyectar estrenos, cada semana presentamos una cartelera cuidadosamente seleccionada con las **mejores películas de la historia del cine**, para que los usuarios puedan descubrirlas o revivirlas con la mejor calidad de imagen y sonido.

Este repositorio contiene la **recreación del frontend**, desarrollada bajo el paquete `frontend_backend` y gestionada exclusivamente con **Reflex** y **Poetry**, preparada para integrarse posteriormente con un backend desarrollado en **FastAPI + MySQL**.

---

## ✨ Funcionalidades

* 🎥 **Cartelera Semanal** con una selección de películas clásicas e icónicas.
* 🏷️ **Filtros Dinámicos por Categoría** (Todas, Drama, Acción, Thriller y Ciencia Ficción).
* 🔍 **Buscador de Películas** mediante estado reactivo.
* 🎞️ **Vista Detallada de Películas** con información, horarios y tandas.
* 💺 **Sistema de Reservas y Asientos** con selección visual por sala.
* 🔐 **Autenticación Demo** mediante Login y Registro.
* 📱 **Diseño Responsive** para dispositivos móviles y escritorio.
* 🗓️ **Sección Próximamente** para futuros estrenos.
* ✅ **Pruebas Unitarias Básicas** usando Pytest.

---

## 🛠️ Tecnologías Utilizadas

### Frontend

| Tecnología   | Uso                              |
| ------------ | -------------------------------- |
| Reflex       | Framework web en Python          |
| Poetry       | Gestión de dependencias          |
| Python 3.12  | Lenguaje principal               |
| Pytest       | Pruebas unitarias                |
| Google Fonts | Tipografías (Bebas Neue e Inter) |

### Backend (Integración futura)

| Tecnología | Uso           |
| ---------- | ------------- |
| FastAPI    | API REST      |
| MySQL      | Base de datos |
| SQLAlchemy | ORM           |

---

## 🚀 Instalación y Ejecución

### Requisitos Previos

* Python 3.12 o superior
* Poetry 2.x
* Node.js 20 o superior
* Git

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/Backend.git
cd Backend
```

### 2️⃣ Instalar dependencias

```bash
poetry install
```

### 3️⃣ Ejecutar pruebas unitarias

```bash
poetry run pytest
```

### 4️⃣ Iniciar la aplicación

```bash
poetry run reflex run
```

### 5️⃣ Abrir en el navegador

```text
http://localhost:3000
```

---

## 📁 Estructura del Proyecto

```text
Backend/
├── assets/
│   └── favicon.ico
│
├── frontend_backend/
│   ├── components/
│   │   ├── auth_modal.py
│   │   ├── footer.py
│   │   └── navbar.py
│   │
│   ├── pages/
│   │   ├── index.py
│   │   ├── cartelera.py
│   │   ├── pelicula.py
│   │   ├── reservas.py
│   │   └── mock_data.py
│   │
│   ├── styles/
│   │   └── theme.py
│   │
│   └── frontend_backend.py
│
├── tests/
│   └── test_app.py
│
├── pyproject.toml
├── rxconfig.py
└── README.md
```

---

## 🌿 Flujo de Trabajo Git (GitFlow)

### Ramas principales

* `frontend` → Desarrollo del frontend.
* `backend` → Desarrollo del backend.
* `main` → Versión estable del proyecto.

### Convención de commits

```bash
feat: nueva funcionalidad
fix: corrección de errores
docs: documentación
refactor: mejora de código
style: cambios visuales
test: pruebas
```

---

## 🎨 Paleta de Colores Corporativa

| Color          | Hex       | Uso                    |
| -------------- | --------- | ---------------------- |
| Negro Fondo    | `#0A0A0A` | Fondo principal        |
| Negro Card     | `#111111` | Tarjetas y componentes |
| Rojo Principal | `#8B0000` | Botones y acentos      |
| Rojo Hover     | `#A50000` | Efecto hover           |
| Blanco         | `#FFFFFF` | Texto principal        |
| Gris Texto     | `#AAAAAA` | Texto secundario       |

---

## 👥 Créditos

| Rol                       | Responsable | Descripción                                                       |
| ------------------------- | ----------- | ----------------------------------------------------------------- |
| Frontend                  | Damian      | Diseño y desarrollo visual con Reflex                             |
| Backend y Integracion     | Elvin       | API REST, base de datos MySQL y conexión Frontend ↔ Base de Datos |

---

## 🔗 Enlaces Útiles

* Reflex Documentation
* Poetry Documentation
* GitHub Repository

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos y educativos.

© 2026 XP Movies. Todos los derechos reservados.
