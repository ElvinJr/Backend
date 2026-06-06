"""
Script para crear todas las tablas de XP Movies en Aiven (defaultdb).
Ejecutar UNA SOLA VEZ: poetry run python init_db.py
"""
import os
import sys
from dotenv import load_dotenv
import pymysql

load_dotenv()

PASS = os.getenv("AIVEN_PASSWORD", "")
HOST = os.getenv("AIVEN_HOST", "xpmovies-db-elvinarmando-45ad.l.aivencloud.com")
PORT = int(os.getenv("AIVEN_PORT", "25616"))
USER = os.getenv("AIVEN_USER", "avnadmin")
DB   = os.getenv("AIVEN_DATABASE", "defaultdb")

# DDL statements (CREATE TABLE - autocommit, no transaccional)
DDL_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS generos (
        id        INT UNSIGNED    NOT NULL AUTO_INCREMENT,
        nombre    VARCHAR(50)     NOT NULL UNIQUE,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB""",

    """CREATE TABLE IF NOT EXISTS peliculas (
        id             INT UNSIGNED    NOT NULL AUTO_INCREMENT,
        titulo         VARCHAR(150)    NOT NULL,
        genero_id      INT UNSIGNED    NOT NULL,
        clasificacion  ENUM('G','PG','PG-13','R','NC-17') NOT NULL DEFAULT 'PG-13',
        duracion_min   SMALLINT UNSIGNED NOT NULL,
        anio           YEAR            NOT NULL,
        descripcion    TEXT            NOT NULL,
        imagen_url     VARCHAR(500)    NOT NULL,
        calificacion   DECIMAL(3,1)    NOT NULL DEFAULT 0.0,
        estado         ENUM('activa','inactiva') NOT NULL DEFAULT 'activa',
        creado_en      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        CONSTRAINT fk_peliculas_genero
            FOREIGN KEY (genero_id) REFERENCES generos(id)
            ON UPDATE CASCADE ON DELETE RESTRICT
    ) ENGINE=InnoDB""",

    """CREATE TABLE IF NOT EXISTS tandas (
        id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
        pelicula_id INT UNSIGNED    NOT NULL,
        hora        TIME            NOT NULL,
        activa      BOOLEAN         NOT NULL DEFAULT TRUE,
        PRIMARY KEY (id),
        CONSTRAINT fk_tandas_pelicula
            FOREIGN KEY (pelicula_id) REFERENCES peliculas(id)
            ON UPDATE CASCADE ON DELETE CASCADE
    ) ENGINE=InnoDB""",

    """CREATE TABLE IF NOT EXISTS asientos (
        id       INT UNSIGNED NOT NULL AUTO_INCREMENT,
        codigo   CHAR(3)      NOT NULL UNIQUE,
        fila     CHAR(1)      NOT NULL,
        columna  TINYINT      NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB""",

    """CREATE TABLE IF NOT EXISTS usuarios (
        id             INT UNSIGNED    NOT NULL AUTO_INCREMENT,
        nombre         VARCHAR(100)    NOT NULL,
        email          VARCHAR(150)    NOT NULL UNIQUE,
        password_hash  VARCHAR(255)    NOT NULL,
        telefono       VARCHAR(20)     NULL,
        activo         BOOLEAN         NOT NULL DEFAULT TRUE,
        creado_en      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB""",

    """CREATE TABLE IF NOT EXISTS reservas (
        id              INT UNSIGNED    NOT NULL AUTO_INCREMENT,
        usuario_id      INT UNSIGNED    NULL,
        pelicula_id     INT UNSIGNED    NOT NULL,
        tanda_id        INT UNSIGNED    NOT NULL,
        nombre_cliente  VARCHAR(100)    NOT NULL,
        email_cliente   VARCHAR(150)    NOT NULL,
        telefono        VARCHAR(20)     NOT NULL,
        total_asientos  TINYINT         NOT NULL DEFAULT 1,
        precio_unitario DECIMAL(10,2)   NOT NULL DEFAULT 350.00,
        total           DECIMAL(10,2)   NOT NULL DEFAULT 0.00,
        estado          ENUM('pendiente','confirmada','cancelada') NOT NULL DEFAULT 'pendiente',
        creado_en       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        CONSTRAINT fk_reservas_usuario
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            ON UPDATE CASCADE ON DELETE SET NULL,
        CONSTRAINT fk_reservas_pelicula
            FOREIGN KEY (pelicula_id) REFERENCES peliculas(id)
            ON UPDATE CASCADE ON DELETE RESTRICT,
        CONSTRAINT fk_reservas_tanda
            FOREIGN KEY (tanda_id) REFERENCES tandas(id)
            ON UPDATE CASCADE ON DELETE RESTRICT
    ) ENGINE=InnoDB""",

    """CREATE TABLE IF NOT EXISTS detalle_reservas (
        id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
        reserva_id  INT UNSIGNED NOT NULL,
        asiento_id  INT UNSIGNED NOT NULL,
        PRIMARY KEY (id),
        UNIQUE KEY uq_reserva_asiento (reserva_id, asiento_id),
        CONSTRAINT fk_detalle_reserva
            FOREIGN KEY (reserva_id) REFERENCES reservas(id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT fk_detalle_asiento
            FOREIGN KEY (asiento_id) REFERENCES asientos(id)
            ON UPDATE CASCADE ON DELETE RESTRICT
    ) ENGINE=InnoDB""",

    """CREATE TABLE IF NOT EXISTS proximas_peliculas (
        id             INT UNSIGNED    NOT NULL AUTO_INCREMENT,
        titulo         VARCHAR(150)    NOT NULL,
        genero_id      INT UNSIGNED    NOT NULL,
        clasificacion  ENUM('G','PG','PG-13','R','NC-17') NOT NULL DEFAULT 'PG-13',
        imagen_url     VARCHAR(500)    NOT NULL,
        fecha_estreno  DATE            NULL,
        estreno_texto  VARCHAR(100)    NOT NULL DEFAULT 'Proxima Semana',
        activa         BOOLEAN         NOT NULL DEFAULT TRUE,
        PRIMARY KEY (id),
        CONSTRAINT fk_proximas_genero
            FOREIGN KEY (genero_id) REFERENCES generos(id)
            ON UPDATE CASCADE ON DELETE RESTRICT
    ) ENGINE=InnoDB""",
]

# DML statements (INSERT - transaccional)
DML_STATEMENTS = [
    # Generos
    "INSERT IGNORE INTO generos (nombre) VALUES ('Drama')",
    "INSERT IGNORE INTO generos (nombre) VALUES ('Accion')",
    "INSERT IGNORE INTO generos (nombre) VALUES ('Thriller')",
    "INSERT IGNORE INTO generos (nombre) VALUES ('Ciencia Ficcion')",
    "INSERT IGNORE INTO generos (nombre) VALUES ('Romance')",

    # Peliculas
    """INSERT IGNORE INTO peliculas (titulo, genero_id, clasificacion, duracion_min, anio, descripcion, imagen_url, calificacion, estado)
       VALUES ('El Padrino', (SELECT id FROM generos WHERE nombre='Drama'), 'R', 175, 1972,
               'La historia de la familia Corleone, una de las mas poderosas del crimen organizado en Nueva York.',
               'https://i.pinimg.com/1200x/74/f4/65/74f465d3ada4455e2f6defbe0fe11f67.jpg', 5.0, 'activa')""",
    """INSERT IGNORE INTO peliculas (titulo, genero_id, clasificacion, duracion_min, anio, descripcion, imagen_url, calificacion, estado)
       VALUES ('Batman: El Caballero de la Noche', (SELECT id FROM generos WHERE nombre='Accion'), 'PG-13', 152, 2008,
               'Batman enfrenta al Joker, un criminal caotico que busca sumir Gotham City en el anarquismo total.',
               'https://i.pinimg.com/736x/88/c8/20/88c8204e1017437290af9db9a02d83f6.jpg', 5.0, 'activa')""",
    """INSERT IGNORE INTO peliculas (titulo, genero_id, clasificacion, duracion_min, anio, descripcion, imagen_url, calificacion, estado)
       VALUES ('Fight Club', (SELECT id FROM generos WHERE nombre='Thriller'), 'R', 139, 1999,
               'Un oficinista insomne forma un club de peleas clandestino con un carismatico vendedor de jabon.',
               'https://i.pinimg.com/736x/4b/5c/cb/4b5ccbe420a9061ea4564e82e0261548.jpg', 4.8, 'activa')""",
    """INSERT IGNORE INTO peliculas (titulo, genero_id, clasificacion, duracion_min, anio, descripcion, imagen_url, calificacion, estado)
       VALUES ('Interstellar', (SELECT id FROM generos WHERE nombre='Ciencia Ficcion'), 'PG-13', 169, 2014,
               'Un grupo de astronautas viaja a traves de un agujero de gusano en busca de un nuevo hogar para la humanidad.',
               'https://i.pinimg.com/736x/3f/09/dd/3f09ddcc1d3c3740f6a74e63d57fba61.jpg', 4.9, 'activa')""",
    """INSERT IGNORE INTO peliculas (titulo, genero_id, clasificacion, duracion_min, anio, descripcion, imagen_url, calificacion, estado)
       VALUES ('The Truman Show', (SELECT id FROM generos WHERE nombre='Drama'), 'PG', 103, 1998,
               'Un hombre descubre que toda su vida ha sido un programa de television transmitido en vivo al mundo entero.',
               'https://i.pinimg.com/1200x/e4/be/be/e4bebef03bf3c5a258f2069c25d1d1bc.jpg', 4.7, 'activa')""",
    """INSERT IGNORE INTO peliculas (titulo, genero_id, clasificacion, duracion_min, anio, descripcion, imagen_url, calificacion, estado)
       VALUES ('The Butterfly Effect', (SELECT id FROM generos WHERE nombre='Ciencia Ficcion'), 'R', 113, 2004,
               'Un joven descubre que puede viajar al pasado, pero cada cambio tiene consecuencias devastadoras.',
               'https://i.pinimg.com/1200x/0b/21/17/0b2117529ba390b93dee98df45d30304.jpg', 4.5, 'activa')""",
    """INSERT IGNORE INTO peliculas (titulo, genero_id, clasificacion, duracion_min, anio, descripcion, imagen_url, calificacion, estado)
       VALUES ('Forrest Gump', (SELECT id FROM generos WHERE nombre='Drama'), 'PG-13', 142, 1994,
               'La extraordinaria historia de un hombre de Alabama cuya vida simple se cruza con los grandes eventos historicos del siglo XX.',
               'https://i.pinimg.com/1200x/13/98/2a/13982aedfb82420cbcf1b44f616539f4.jpg', 4.9, 'activa')""",
    """INSERT IGNORE INTO peliculas (titulo, genero_id, clasificacion, duracion_min, anio, descripcion, imagen_url, calificacion, estado)
       VALUES ('The Matrix', (SELECT id FROM generos WHERE nombre='Ciencia Ficcion'), 'R', 136, 1999,
               'Un hacker descubre que la realidad que conoce es una simulacion creada por maquinas que esclavizan a la humanidad.',
               'https://i.pinimg.com/736x/62/f2/41/62f241fd34d94f303a71df7fc7274fbb.jpg', 4.8, 'activa')""",

    # Tandas
    "INSERT IGNORE INTO tandas (pelicula_id, hora) VALUES (1,'16:00:00'),(1,'19:00:00'),(1,'22:00:00')",
    "INSERT IGNORE INTO tandas (pelicula_id, hora) VALUES (2,'15:30:00'),(2,'18:30:00'),(2,'21:30:00')",
    "INSERT IGNORE INTO tandas (pelicula_id, hora) VALUES (3,'17:00:00'),(3,'20:00:00'),(3,'23:00:00')",
    "INSERT IGNORE INTO tandas (pelicula_id, hora) VALUES (4,'16:30:00'),(4,'19:30:00'),(4,'22:30:00')",
    "INSERT IGNORE INTO tandas (pelicula_id, hora) VALUES (5,'15:00:00'),(5,'18:00:00'),(5,'21:00:00')",
    "INSERT IGNORE INTO tandas (pelicula_id, hora) VALUES (6,'16:00:00'),(6,'19:00:00'),(6,'22:00:00')",
    "INSERT IGNORE INTO tandas (pelicula_id, hora) VALUES (7,'15:30:00'),(7,'18:30:00'),(7,'21:30:00')",
    "INSERT IGNORE INTO tandas (pelicula_id, hora) VALUES (8,'17:00:00'),(8,'20:00:00'),(8,'23:00:00')",

    # Asientos A-E x 1-8
    "INSERT IGNORE INTO asientos (codigo, fila, columna) VALUES ('A1','A',1),('A2','A',2),('A3','A',3),('A4','A',4),('A5','A',5),('A6','A',6),('A7','A',7),('A8','A',8)",
    "INSERT IGNORE INTO asientos (codigo, fila, columna) VALUES ('B1','B',1),('B2','B',2),('B3','B',3),('B4','B',4),('B5','B',5),('B6','B',6),('B7','B',7),('B8','B',8)",
    "INSERT IGNORE INTO asientos (codigo, fila, columna) VALUES ('C1','C',1),('C2','C',2),('C3','C',3),('C4','C',4),('C5','C',5),('C6','C',6),('C7','C',7),('C8','C',8)",
    "INSERT IGNORE INTO asientos (codigo, fila, columna) VALUES ('D1','D',1),('D2','D',2),('D3','D',3),('D4','D',4),('D5','D',5),('D6','D',6),('D7','D',7),('D8','D',8)",
    "INSERT IGNORE INTO asientos (codigo, fila, columna) VALUES ('E1','E',1),('E2','E',2),('E3','E',3),('E4','E',4),('E5','E',5),('E6','E',6),('E7','E',7),('E8','E',8)",

    # Proximas peliculas
    """INSERT IGNORE INTO proximas_peliculas (titulo, genero_id, clasificacion, imagen_url, estreno_texto)
       VALUES ('10 Things I Hate About You', (SELECT id FROM generos WHERE nombre='Romance'), 'PG-13',
               'https://i.pinimg.com/736x/fc/31/09/fc3109b7595900ec3709e4400db213ef.jpg', 'Proxima Semana')""",
    """INSERT IGNORE INTO proximas_peliculas (titulo, genero_id, clasificacion, imagen_url, estreno_texto)
       VALUES ('La La Land', (SELECT id FROM generos WHERE nombre='Romance'), 'PG',
               'https://i.pinimg.com/1200x/1a/5d/0f/1a5d0f456e6d4e474b3465ad030b1fdb.jpg', 'Proxima Semana')""",
    """INSERT IGNORE INTO proximas_peliculas (titulo, genero_id, clasificacion, imagen_url, estreno_texto)
       VALUES ('The Notebook', (SELECT id FROM generos WHERE nombre='Romance'), 'PG-13',
               'https://i.pinimg.com/736x/0a/8a/52/0a8a52c74e5e3d88d26925018c741be6.jpg', 'Proxima Semana')""",
]


def main():
    print(f"Conectando a {HOST}:{PORT}/{DB}...")
    # autocommit=True para que los CREATE TABLE (DDL) surtan efecto inmediatamente
    conn = pymysql.connect(
        host=HOST, port=PORT, user=USER, password=PASS,
        database=DB, ssl={"ssl_disabled": False},
        connect_timeout=15, autocommit=True,
    )
    cur = conn.cursor()

    # 1. Crear tablas (DDL - autocommit)
    print("\n--- Creando tablas ---")
    for stmt in DDL_STATEMENTS:
        tabla = stmt.strip().split("\n")[0][:60]
        try:
            cur.execute(stmt)
            print(f"  [OK] {tabla.strip()}")
        except Exception as e:
            print(f"  [ERROR] {e}")
            conn.close()
            sys.exit(1)

    # 2. Insertar datos (DML - manual commit)
    conn.autocommit(False)
    print("\n--- Insertando datos de ejemplo ---")
    try:
        for stmt in DML_STATEMENTS:
            label = stmt.strip()[:55].replace("\n", " ")
            try:
                cur.execute(stmt)
                print(f"  [OK] {label}...")
            except Exception as e:
                print(f"  [WARN] {e} | SQL: {label[:80]}")
        conn.commit()
        print("  [COMMIT OK]")
    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] Rollback. Detalle: {e}")
        conn.close()
        sys.exit(1)

    # 3. Verificacion final
    conn.autocommit(True)
    print("\n--- Verificacion ---")
    tablas = ["generos", "peliculas", "tandas", "asientos",
              "proximas_peliculas", "usuarios", "reservas", "detalle_reservas"]
    for tabla in tablas:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            print(f"  {tabla}: {count} registros")
        except Exception as e:
            print(f"  {tabla}: ERROR - {e}")

    conn.close()
    print("\n[OK] Base de datos inicializada correctamente en Aiven.")


if __name__ == "__main__":
    main()
