# db.py — Conexión de XP Movies con Aiven MySQL
# ============================================================
# Uso:
#   from frontend_backend.db import get_peliculas, crear_reserva, ...
#
# Requiere instalar (agrega a pyproject.toml):
#   sqlalchemy>=2.0
#   pymysql>=1.1
#   python-dotenv>=1.0
#   cryptography>=42.0   ← requerido por PyMySQL para SSL
# ============================================================

import os
import ssl
from pathlib import Path
from contextlib import contextmanager
from dotenv import load_dotenv

from sqlalchemy import (
    create_engine, text,
    Column, Integer, String, Text, SmallInteger,
    Numeric, Boolean, Enum, DateTime, ForeignKey,
    TIMESTAMP,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sqlalchemy.pool import NullPool

# ── Cargar variables de entorno ───────────────────────────────────────────────
load_dotenv()  # Lee el archivo .env del directorio raíz del proyecto

AIVEN_HOST     = os.getenv("AIVEN_HOST",     "xpmovies-db-elvinarmando-45ad.l.aivencloud.com")
AIVEN_PORT     = int(os.getenv("AIVEN_PORT", "25616"))
AIVEN_USER     = os.getenv("AIVEN_USER",     "avnadmin")
AIVEN_PASSWORD = os.getenv("AIVEN_PASSWORD", "")   # ← Siempre leer desde .env
AIVEN_DATABASE = os.getenv("AIVEN_DATABASE", "defaultdb")
AIVEN_SSL_CA   = os.getenv("AIVEN_SSL_CA",   "ca.pem")

# ── Ruta absoluta al certificado SSL ─────────────────────────────────────────
_BASE_DIR = Path(__file__).resolve().parent.parent  # raíz del proyecto
SSL_CA_PATH = str(_BASE_DIR / AIVEN_SSL_CA)

# ── URL de conexión MySQL con PyMySQL ─────────────────────────────────────────
DATABASE_URL = (
    f"mysql+pymysql://{AIVEN_USER}:{AIVEN_PASSWORD}"
    f"@{AIVEN_HOST}:{AIVEN_PORT}/{AIVEN_DATABASE}"
)

# ── Motor SQLAlchemy con SSL ──────────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": SSL_CA_PATH,
        }
    },
    pool_pre_ping=True,   # Verifica la conexión antes de usarla
    pool_recycle=3600,    # Recicla conexiones cada 1 hora (evita timeouts de Aiven)
    echo=False,           # Cambia a True para ver las queries en consola (debug)
    poolclass=NullPool,   # Recomendado para apps con múltiples workers (Reflex)
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


# ═══════════════════════════════════════════════════════════════════════════════
# MODELOS ORM — Mapean exactamente las tablas del schema MySQL
# ═══════════════════════════════════════════════════════════════════════════════

class Genero(Base):
    __tablename__ = "generos"

    id     = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)

    # Relaciones
    peliculas          = relationship("Pelicula",        back_populates="genero")
    proximas_peliculas = relationship("ProximaPelicula", back_populates="genero")


class Pelicula(Base):
    __tablename__ = "peliculas"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    titulo        = Column(String(150), nullable=False)
    genero_id     = Column(Integer, ForeignKey("generos.id"), nullable=False)
    clasificacion = Column(Enum("G", "PG", "PG-13", "R", "NC-17"), nullable=False, default="PG-13")
    duracion_min  = Column(SmallInteger, nullable=False)
    anio          = Column(Integer, nullable=False)
    descripcion   = Column(Text, nullable=False)
    imagen_url    = Column(String(500), nullable=False)
    calificacion  = Column(Numeric(3, 1), nullable=False, default=0.0)
    estado        = Column(Enum("activa", "inactiva"), nullable=False, default="activa")
    creado_en     = Column(TIMESTAMP, nullable=False)

    # Relaciones
    genero   = relationship("Genero",   back_populates="peliculas")
    tandas   = relationship("Tanda",    back_populates="pelicula",  cascade="all, delete-orphan")
    reservas = relationship("Reserva",  back_populates="pelicula")


class Tanda(Base):
    __tablename__ = "tandas"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    pelicula_id = Column(Integer, ForeignKey("peliculas.id"), nullable=False)
    hora        = Column(String(8), nullable=False)   # "HH:MM:SS"
    activa      = Column(Boolean, nullable=False, default=True)

    # Relaciones
    pelicula = relationship("Pelicula", back_populates="tandas")
    reservas = relationship("Reserva",  back_populates="tanda")


class Asiento(Base):
    __tablename__ = "asientos"

    id      = Column(Integer, primary_key=True, autoincrement=True)
    codigo  = Column(String(3), nullable=False, unique=True)   # "A1", "B8", etc.
    fila    = Column(String(1), nullable=False)
    columna = Column(Integer,   nullable=False)

    # Relaciones
    detalle_reservas = relationship("DetalleReserva", back_populates="asiento")


class Usuario(Base):
    __tablename__ = "usuarios"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    nombre        = Column(String(100), nullable=False)
    email         = Column(String(150), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    telefono      = Column(String(20),  nullable=True)
    activo        = Column(Boolean,     nullable=False, default=True)
    creado_en     = Column(TIMESTAMP,   nullable=False)

    # Relaciones
    reservas = relationship("Reserva", back_populates="usuario")


class Reserva(Base):
    __tablename__ = "reservas"

    id              = Column(Integer,       primary_key=True, autoincrement=True)
    usuario_id      = Column(Integer,       ForeignKey("usuarios.id"), nullable=True)
    pelicula_id     = Column(Integer,       ForeignKey("peliculas.id"), nullable=False)
    tanda_id        = Column(Integer,       ForeignKey("tandas.id"),    nullable=False)
    nombre_cliente  = Column(String(100),   nullable=False)
    email_cliente   = Column(String(150),   nullable=False)
    telefono        = Column(String(20),    nullable=False)
    total_asientos  = Column(Integer,       nullable=False, default=1)
    precio_unitario = Column(Numeric(10,2), nullable=False, default=350.00)
    # "total" es columna GENERATED en MySQL — no se declara en ORM
    estado          = Column(Enum("pendiente", "confirmada", "cancelada"),
                             nullable=False, default="pendiente")
    creado_en       = Column(TIMESTAMP, nullable=False)

    # Relaciones
    usuario          = relationship("Usuario",        back_populates="reservas")
    pelicula         = relationship("Pelicula",       back_populates="reservas")
    tanda            = relationship("Tanda",          back_populates="reservas")
    detalle_reservas = relationship("DetalleReserva", back_populates="reserva",
                                   cascade="all, delete-orphan")


class DetalleReserva(Base):
    __tablename__ = "detalle_reservas"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"),  nullable=False)
    asiento_id = Column(Integer, ForeignKey("asientos.id"), nullable=False)

    # Relaciones
    reserva = relationship("Reserva",  back_populates="detalle_reservas")
    asiento = relationship("Asiento",  back_populates="detalle_reservas")


class ProximaPelicula(Base):
    __tablename__ = "proximas_peliculas"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    titulo        = Column(String(150), nullable=False)
    genero_id     = Column(Integer, ForeignKey("generos.id"), nullable=False)
    clasificacion = Column(Enum("G", "PG", "PG-13", "R", "NC-17"), nullable=False, default="PG-13")
    imagen_url    = Column(String(500), nullable=False)
    fecha_estreno = Column(DateTime,    nullable=True)
    estreno_texto = Column(String(100), nullable=False, default="Próxima Semana")
    activa        = Column(Boolean,     nullable=False, default=True)

    # Relaciones
    genero = relationship("Genero", back_populates="proximas_peliculas")


# ═══════════════════════════════════════════════════════════════════════════════
# CONTEXTO DE SESIÓN — Úsalo con "with" para auto-cerrar la conexión
# ═══════════════════════════════════════════════════════════════════════════════

@contextmanager
def get_db() -> Session:
    """
    Proveedor de sesión de base de datos.
    
    Uso:
        with get_db() as db:
            peliculas = db.query(Pelicula).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES CRUD — Para usar desde los States de Reflex
# ═══════════════════════════════════════════════════════════════════════════════

# ── PRUEBA DE CONEXIÓN ────────────────────────────────────────────────────────

def probar_conexion() -> bool:
    """
    Ejecuta SELECT 1 para verificar que la conexión con Aiven funciona.
    Retorna True si la conexión es exitosa, False si falla.
    
    Uso desde terminal:
        python -c "from frontend_backend.db import probar_conexion; print(probar_conexion())"
    """
    try:
        with engine.connect() as conn:
            resultado = conn.execute(text("SELECT 1")).fetchone()
            print(f"✅ Conexión exitosa con Aiven MySQL: {resultado}")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False


# ── PELÍCULAS ─────────────────────────────────────────────────────────────────

def get_peliculas(solo_activas: bool = True) -> list[dict]:
    """
    Retorna la lista de películas con su género y tandas.
    Equivalente al PELICULAS de mock_data.py pero desde la BD.
    
    Retorna lista de dicts compatibles con el formato usado en el frontend:
    {id, titulo, genero, clasificacion, duracion, anio, descripcion, imagen, calificacion, tandas, estado}
    """
    with get_db() as db:
        query = db.query(Pelicula).join(Genero)
        if solo_activas:
            query = query.filter(Pelicula.estado == "activa")
        peliculas = query.order_by(Pelicula.id).all()

        resultado = []
        for p in peliculas:
            # Obtener tandas como lista de strings (formato original: "4:00 PM")
            tandas_str = []
            for t in sorted(p.tandas, key=lambda x: x.hora):
                if t.activa:
                    # Convertir "16:00:00" → "4:00 PM"
                    from datetime import datetime
                    hora_obj = datetime.strptime(t.hora, "%H:%M:%S")
                    tandas_str.append(hora_obj.strftime("%-I:%M %p").replace("AM", "AM").replace("PM", "PM"))

            resultado.append({
                "id":           p.id,
                "titulo":       p.titulo,
                "genero":       p.genero.nombre,
                "clasificacion":p.clasificacion,
                "duracion":     f"{p.duracion_min // 60}h {p.duracion_min % 60}min",
                "anio":         p.anio,
                "descripcion":  p.descripcion,
                "imagen":       p.imagen_url,
                "calificacion": float(p.calificacion),
                "tandas":       tandas_str,
                "estado":       p.estado,
            })
        return resultado


def get_pelicula_por_id(pelicula_id: int) -> dict | None:
    """Retorna una sola película por ID."""
    peliculas = get_peliculas(solo_activas=False)
    for p in peliculas:
        if p["id"] == pelicula_id:
            return p
    return None


# ── PRÓXIMAS PELÍCULAS ────────────────────────────────────────────────────────

def get_proximas_peliculas() -> list[dict]:
    """
    Retorna próximas películas.
    Equivalente al PROXIMAS_PELICULAS de mock_data.py pero desde la BD.
    """
    with get_db() as db:
        proximas = (
            db.query(ProximaPelicula)
            .join(Genero)
            .filter(ProximaPelicula.activa == True)
            .order_by(ProximaPelicula.id)
            .all()
        )
        return [
            {
                "id":            p.id,
                "titulo":        p.titulo,
                "genero":        p.genero.nombre,
                "clasificacion": p.clasificacion,
                "imagen":        p.imagen_url,
                "estreno":       p.estreno_texto,
            }
            for p in proximas
        ]


# ── ASIENTOS ──────────────────────────────────────────────────────────────────

def get_asientos_ocupados(tanda_id: int) -> list[str]:
    """
    Retorna los códigos de asientos ya reservados para una tanda específica.
    Úsalo en el mapa de asientos para mostrar cuáles están ocupados.
    
    Ejemplo: get_asientos_ocupados(1) → ["A1", "A5", "B3", "B4"]
    """
    with get_db() as db:
        reservas = (
            db.query(Reserva)
            .filter(
                Reserva.tanda_id == tanda_id,
                Reserva.estado.in_(["pendiente", "confirmada"]),
            )
            .all()
        )
        codigos = []
        for r in reservas:
            for dr in r.detalle_reservas:
                codigos.append(dr.asiento.codigo)
        return codigos


# ── USUARIOS ──────────────────────────────────────────────────────────────────

def registrar_usuario(nombre: str, email: str, password_plain: str,
                      telefono: str | None = None) -> dict:
    """
    Registra un nuevo usuario hasheando la contraseña con bcrypt.
    Retorna dict con id, nombre, email o lanza ValueError si el email ya existe.
    
    Requiere: pip install bcrypt
    """
    import bcrypt

    with get_db() as db:
        # Verificar si el email ya existe
        existe = db.query(Usuario).filter(Usuario.email == email).first()
        if existe:
            raise ValueError(f"El email '{email}' ya está registrado.")

        # Hashear contraseña
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_plain.encode("utf-8"), salt).decode("utf-8")

        nuevo = Usuario(
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            telefono=telefono,
        )
        db.add(nuevo)
        db.flush()  # Obtiene el ID sin hacer commit aún
        return {"id": nuevo.id, "nombre": nuevo.nombre, "email": nuevo.email}


def login_usuario(email: str, password_plain: str) -> dict | None:
    """
    Verifica credenciales. Retorna dict del usuario si son correctas, None si no.
    
    Requiere: pip install bcrypt
    """
    import bcrypt

    with get_db() as db:
        usuario = db.query(Usuario).filter(
            Usuario.email == email,
            Usuario.activo == True,
        ).first()

        if not usuario:
            return None

        if bcrypt.checkpw(password_plain.encode("utf-8"),
                          usuario.password_hash.encode("utf-8")):
            return {
                "id":       usuario.id,
                "nombre":   usuario.nombre,
                "email":    usuario.email,
                "telefono": usuario.telefono,
            }
        return None


# ── RESERVAS ──────────────────────────────────────────────────────────────────

def crear_reserva(
    pelicula_id:    int,
    tanda_id:       int,
    nombre_cliente: str,
    email_cliente:  str,
    telefono:       str,
    codigos_asientos: list[str],   # ej: ["B3", "B4"]
    usuario_id:     int | None = None,
    precio_unitario: float = 350.00,
) -> dict:
    """
    Crea una reserva completa con sus asientos seleccionados.
    Retorna dict con id, total y estado de la reserva creada.
    Lanza ValueError si algún asiento ya está ocupado.
    
    Ejemplo de uso desde ReservasState:
        resultado = crear_reserva(
            pelicula_id=1, tanda_id=1,
            nombre_cliente="Juan Pérez",
            email_cliente="juan@email.com",
            telefono="809-555-0001",
            codigos_asientos=["B3", "B4"],
        )
    """
    with get_db() as db:
        # 1. Verificar que los asientos existen
        asientos = (
            db.query(Asiento)
            .filter(Asiento.codigo.in_(codigos_asientos))
            .all()
        )
        if len(asientos) != len(codigos_asientos):
            encontrados = {a.codigo for a in asientos}
            no_encontrados = set(codigos_asientos) - encontrados
            raise ValueError(f"Asientos no encontrados: {no_encontrados}")

        # 2. Verificar que ningún asiento esté ya ocupado para esa tanda
        asientos_ocupados = get_asientos_ocupados(tanda_id)
        conflictos = [c for c in codigos_asientos if c in asientos_ocupados]
        if conflictos:
            raise ValueError(f"Los asientos {conflictos} ya están ocupados para esta tanda.")

        # 3. Crear la reserva
        nueva_reserva = Reserva(
            usuario_id=usuario_id,
            pelicula_id=pelicula_id,
            tanda_id=tanda_id,
            nombre_cliente=nombre_cliente,
            email_cliente=email_cliente,
            telefono=telefono,
            total_asientos=len(codigos_asientos),
            precio_unitario=precio_unitario,
            estado="confirmada",
        )
        db.add(nueva_reserva)
        db.flush()  # Genera el ID de la reserva

        # 4. Crear el detalle de asientos
        for asiento in asientos:
            detalle = DetalleReserva(
                reserva_id=nueva_reserva.id,
                asiento_id=asiento.id,
            )
            db.add(detalle)

        total = len(codigos_asientos) * precio_unitario
        return {
            "id":       nueva_reserva.id,
            "total":    total,
            "asientos": codigos_asientos,
            "estado":   "confirmada",
        }


def get_reservas_por_usuario(usuario_id: int) -> list[dict]:
    """Retorna el historial de reservas de un usuario."""
    with get_db() as db:
        reservas = (
            db.query(Reserva)
            .filter(Reserva.usuario_id == usuario_id)
            .order_by(Reserva.creado_en.desc())
            .all()
        )
        resultado = []
        for r in reservas:
            asientos_codigos = [dr.asiento.codigo for dr in r.detalle_reservas]
            resultado.append({
                "id":           r.id,
                "pelicula":     r.pelicula.titulo,
                "tanda":        r.tanda.hora,
                "asientos":     asientos_codigos,
                "total":        float(r.precio_unitario) * r.total_asientos,
                "estado":       r.estado,
                "creado_en":    str(r.creado_en),
            })
        return resultado
