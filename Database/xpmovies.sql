-- =============================================================
-- XP MOVIES — Script de Base de Datos
-- Compatible con MySQL 8.4
-- Generado a partir del análisis del proyecto Reflex
-- =============================================================

-- Crear y seleccionar la base de datos
CREATE DATABASE IF NOT EXISTS xpmovies
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE xpmovies;

-- =============================================================
-- TABLA: generos
-- Fuente: categorías de los botones de filtro en cartelera.py
-- Valores: Todas, Drama, Acción, Thriller, Ciencia Ficción, Romance
-- =============================================================
CREATE TABLE IF NOT EXISTS generos (
    id        INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    nombre    VARCHAR(50)     NOT NULL UNIQUE,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

-- =============================================================
-- TABLA: peliculas
-- Fuente: lista PELICULAS en mock_data.py (8 películas activas)
-- =============================================================
CREATE TABLE IF NOT EXISTS peliculas (
    id             INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    titulo         VARCHAR(150)    NOT NULL,
    genero_id      INT UNSIGNED    NOT NULL,
    clasificacion  ENUM('G','PG','PG-13','R','NC-17') NOT NULL DEFAULT 'PG-13',
    duracion_min   SMALLINT UNSIGNED NOT NULL COMMENT 'Duración en minutos',
    anio           YEAR            NOT NULL,
    descripcion    TEXT            NOT NULL,
    imagen_url     VARCHAR(500)    NOT NULL,
    calificacion   DECIMAL(3,1)    NOT NULL DEFAULT 0.0
                   CHECK (calificacion BETWEEN 0.0 AND 5.0),
    estado         ENUM('activa','inactiva') NOT NULL DEFAULT 'activa',
    creado_en      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_peliculas_genero
        FOREIGN KEY (genero_id) REFERENCES generos(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =============================================================
-- TABLA: tandas
-- Fuente: campo "tandas" de cada película en mock_data.py
-- Cada película tiene 3 tandas diarias
-- =============================================================
CREATE TABLE IF NOT EXISTS tandas (
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    pelicula_id INT UNSIGNED    NOT NULL,
    hora        TIME            NOT NULL COMMENT 'Ej: 16:00:00',
    activa      BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id),
    CONSTRAINT fk_tandas_pelicula
        FOREIGN KEY (pelicula_id) REFERENCES peliculas(id)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- =============================================================
-- TABLA: asientos
-- Fuente: FILAS = ["A","B","C","D","E"] y COLUMNAS = 1..8
-- de reservas.py — 5 filas × 8 columnas = 40 asientos por sala
-- =============================================================
CREATE TABLE IF NOT EXISTS asientos (
    id       INT UNSIGNED NOT NULL AUTO_INCREMENT,
    codigo   CHAR(3)      NOT NULL UNIQUE COMMENT 'Ej: A1, B8, E4',
    fila     CHAR(1)      NOT NULL,
    columna  TINYINT      NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

-- =============================================================
-- TABLA: usuarios
-- Fuente: AuthState en auth_modal.py
-- Campos: nombre, email, contraseña
-- =============================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id             INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    nombre         VARCHAR(100)    NOT NULL,
    email          VARCHAR(150)    NOT NULL UNIQUE,
    password_hash  VARCHAR(255)    NOT NULL COMMENT 'bcrypt hash',
    telefono       VARCHAR(20)     NULL,
    activo         BOOLEAN         NOT NULL DEFAULT TRUE,
    creado_en      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

-- =============================================================
-- TABLA: reservas
-- Fuente: ReservasState en reservas.py
-- Campos del formulario: nombre, email, teléfono
-- + película y tanda seleccionadas
-- Precio por asiento: RD$ 350 (PRECIO_ASIENTO en reservas.py)
-- =============================================================
CREATE TABLE IF NOT EXISTS reservas (
    id              INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    usuario_id      INT UNSIGNED    NULL COMMENT 'NULL si reserva como invitado',
    pelicula_id     INT UNSIGNED    NOT NULL,
    tanda_id        INT UNSIGNED    NOT NULL,
    nombre_cliente  VARCHAR(100)    NOT NULL,
    email_cliente   VARCHAR(150)    NOT NULL,
    telefono        VARCHAR(20)     NOT NULL,
    total_asientos  TINYINT         NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10,2)   NOT NULL DEFAULT 350.00,
    total           DECIMAL(10,2)   NOT NULL
                    GENERATED ALWAYS AS (total_asientos * precio_unitario) STORED,
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
) ENGINE=InnoDB;

-- =============================================================
-- TABLA: detalle_reservas
-- Fuente: mapa de asientos en reservas.py (asientos B3, B4 demo)
-- Relaciona cada reserva con los asientos específicos elegidos
-- =============================================================
CREATE TABLE IF NOT EXISTS detalle_reservas (
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
) ENGINE=InnoDB;

-- =============================================================
-- TABLA: proximas_peliculas
-- Fuente: lista PROXIMAS_PELICULAS en mock_data.py
-- Películas con estado "Próxima Semana"
-- =============================================================
CREATE TABLE IF NOT EXISTS proximas_peliculas (
    id             INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    titulo         VARCHAR(150)    NOT NULL,
    genero_id      INT UNSIGNED    NOT NULL,
    clasificacion  ENUM('G','PG','PG-13','R','NC-17') NOT NULL DEFAULT 'PG-13',
    imagen_url     VARCHAR(500)    NOT NULL,
    fecha_estreno  DATE            NULL COMMENT 'NULL = fecha por confirmar',
    estreno_texto  VARCHAR(100)    NOT NULL DEFAULT 'Próxima Semana',
    activa         BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id),
    CONSTRAINT fk_proximas_genero
        FOREIGN KEY (genero_id) REFERENCES generos(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;


-- =============================================================
-- DATOS DE EJEMPLO
-- =============================================================

-- ── Géneros ──────────────────────────────────────────────────
INSERT INTO generos (nombre) VALUES
    ('Drama'),
    ('Acción'),
    ('Thriller'),
    ('Ciencia Ficción'),
    ('Romance');

-- ── Películas activas (exactamente del mock_data.py) ─────────
INSERT INTO peliculas
    (titulo, genero_id, clasificacion, duracion_min, anio, descripcion, imagen_url, calificacion, estado)
VALUES
    (
        'El Padrino',
        (SELECT id FROM generos WHERE nombre = 'Drama'),
        'R', 175, 1972,
        'La historia de la familia Corleone, una de las más poderosas del crimen organizado en Nueva York.',
        'https://i.pinimg.com/1200x/74/f4/65/74f465d3ada4455e2f6defbe0fe11f67.jpg',
        5.0, 'activa'
    ),
    (
        'Batman: El Caballero de la Noche',
        (SELECT id FROM generos WHERE nombre = 'Acción'),
        'PG-13', 152, 2008,
        'Batman enfrenta al Joker, un criminal caótico que busca sumir Gotham City en el anarquismo total.',
        'https://i.pinimg.com/736x/88/c8/20/88c8204e1017437290af9db9a02d83f6.jpg',
        5.0, 'activa'
    ),
    (
        'Fight Club',
        (SELECT id FROM generos WHERE nombre = 'Thriller'),
        'R', 139, 1999,
        'Un oficinista insomne forma un club de peleas clandestino con un carismático vendedor de jabón.',
        'https://i.pinimg.com/736x/4b/5c/cb/4b5ccbe420a9061ea4564e82e0261548.jpg',
        4.8, 'activa'
    ),
    (
        'Interstellar',
        (SELECT id FROM generos WHERE nombre = 'Ciencia Ficción'),
        'PG-13', 169, 2014,
        'Un grupo de astronautas viaja a través de un agujero de gusano en busca de un nuevo hogar para la humanidad.',
        'https://i.pinimg.com/736x/3f/09/dd/3f09ddcc1d3c3740f6a74e63d57fba61.jpg',
        4.9, 'activa'
    ),
    (
        'The Truman Show',
        (SELECT id FROM generos WHERE nombre = 'Drama'),
        'PG', 103, 1998,
        'Un hombre descubre que toda su vida ha sido un programa de televisión transmitido en vivo al mundo entero.',
        'https://i.pinimg.com/1200x/e4/be/be/e4bebef03bf3c5a258f2069c25d1d1bc.jpg',
        4.7, 'activa'
    ),
    (
        'The Butterfly Effect',
        (SELECT id FROM generos WHERE nombre = 'Ciencia Ficción'),
        'R', 113, 2004,
        'Un joven descubre que puede viajar al pasado a través de sus recuerdos, pero cada cambio tiene consecuencias devastadoras.',
        'https://i.pinimg.com/1200x/0b/21/17/0b2117529ba390b93dee98df45d30304.jpg',
        4.5, 'activa'
    ),
    (
        'Forrest Gump',
        (SELECT id FROM generos WHERE nombre = 'Drama'),
        'PG-13', 142, 1994,
        'La extraordinaria historia de un hombre de Alabama cuya vida simple se cruza con los grandes eventos históricos del siglo XX.',
        'https://i.pinimg.com/1200x/13/98/2a/13982aedfb82420cbcf1b44f616539f4.jpg',
        4.9, 'activa'
    ),
    (
        'The Matrix',
        (SELECT id FROM generos WHERE nombre = 'Ciencia Ficción'),
        'R', 136, 1999,
        'Un hacker descubre que la realidad que conoce es una simulación creada por máquinas que esclavizan a la humanidad.',
        'https://i.pinimg.com/736x/62/f2/41/62f241fd34d94f303a71df7fc7274fbb.jpg',
        4.8, 'activa'
    );

-- ── Tandas (3 por película, igual que en mock_data.py) ────────
-- El Padrino (id=1): 4:00 PM, 7:00 PM, 10:00 PM
INSERT INTO tandas (pelicula_id, hora) VALUES
    (1, '16:00:00'), (1, '19:00:00'), (1, '22:00:00'),
-- Batman (id=2): 3:30 PM, 6:30 PM, 9:30 PM
    (2, '15:30:00'), (2, '18:30:00'), (2, '21:30:00'),
-- Fight Club (id=3): 5:00 PM, 8:00 PM, 11:00 PM
    (3, '17:00:00'), (3, '20:00:00'), (3, '23:00:00'),
-- Interstellar (id=4): 4:30 PM, 7:30 PM, 10:30 PM
    (4, '16:30:00'), (4, '19:30:00'), (4, '22:30:00'),
-- The Truman Show (id=5): 3:00 PM, 6:00 PM, 9:00 PM
    (5, '15:00:00'), (5, '18:00:00'), (5, '21:00:00'),
-- The Butterfly Effect (id=6): 4:00 PM, 7:00 PM, 10:00 PM
    (6, '16:00:00'), (6, '19:00:00'), (6, '22:00:00'),
-- Forrest Gump (id=7): 3:30 PM, 6:30 PM, 9:30 PM
    (7, '15:30:00'), (7, '18:30:00'), (7, '21:30:00'),
-- The Matrix (id=8): 5:00 PM, 8:00 PM, 11:00 PM
    (8, '17:00:00'), (8, '20:00:00'), (8, '23:00:00');

-- ── Asientos (FILAS A-E × COLUMNAS 1-8 = 40 asientos) ────────
-- Generados exactamente como en reservas.py
INSERT INTO asientos (codigo, fila, columna) VALUES
    ('A1','A',1),('A2','A',2),('A3','A',3),('A4','A',4),
    ('A5','A',5),('A6','A',6),('A7','A',7),('A8','A',8),
    ('B1','B',1),('B2','B',2),('B3','B',3),('B4','B',4),
    ('B5','B',5),('B6','B',6),('B7','B',7),('B8','B',8),
    ('C1','C',1),('C2','C',2),('C3','C',3),('C4','C',4),
    ('C5','C',5),('C6','C',6),('C7','C',7),('C8','C',8),
    ('D1','D',1),('D2','D',2),('D3','D',3),('D4','D',4),
    ('D5','D',5),('D6','D',6),('D7','D',7),('D8','D',8),
    ('E1','E',1),('E2','E',2),('E3','E',3),('E4','E',4),
    ('E5','E',5),('E6','E',6),('E7','E',7),('E8','E',8);

-- ── Usuarios de prueba ────────────────────────────────────────
-- Contraseñas hasheadas con bcrypt (valor demo, no usar en producción)
INSERT INTO usuarios (nombre, email, password_hash, telefono) VALUES
    ('Juan Pérez',    'juan@email.com',    '$2b$12$demo_hash_juan_placeholder',    '809-555-0001'),
    ('María García',  'maria@email.com',   '$2b$12$demo_hash_maria_placeholder',   '829-555-0002'),
    ('Carlos López',  'carlos@email.com',  '$2b$12$demo_hash_carlos_placeholder',  '849-555-0003');

-- ── Próximas películas (exactamente de PROXIMAS_PELICULAS) ────
INSERT INTO proximas_peliculas
    (titulo, genero_id, clasificacion, imagen_url, estreno_texto)
VALUES
    (
        '10 Things I Hate About You',
        (SELECT id FROM generos WHERE nombre = 'Romance'),
        'PG-13',
        'https://i.pinimg.com/736x/fc/31/09/fc3109b7595900ec3709e4400db213ef.jpg',
        'Próxima Semana'
    ),
    (
        'La La Land',
        (SELECT id FROM generos WHERE nombre = 'Romance'),
        'PG',
        'https://i.pinimg.com/1200x/1a/5d/0f/1a5d0f456e6d4e474b3465ad030b1fdb.jpg',
        'Próxima Semana'
    ),
    (
        'The Notebook',
        (SELECT id FROM generos WHERE nombre = 'Romance'),
        'PG-13',
        'https://i.pinimg.com/736x/0a/8a/52/0a8a52c74e5e3d88d26925018c741be6.jpg',
        'Próxima Semana'
    );

-- ── Reservas de ejemplo (demo del mapa de asientos) ──────────
INSERT INTO reservas
    (usuario_id, pelicula_id, tanda_id, nombre_cliente, email_cliente, telefono, total_asientos, precio_unitario, estado)
VALUES
    (
        1,          -- Juan Pérez
        1,          -- El Padrino
        1,          -- Tanda 4:00 PM
        'Juan Pérez', 'juan@email.com', '809-555-0001',
        2, 350.00, 'confirmada'
    ),
    (
        2,          -- María García
        2,          -- Batman
        5,          -- Tanda 6:30 PM
        'María García', 'maria@email.com', '829-555-0002',
        1, 350.00, 'confirmada'
    ),
    (
        NULL,       -- Invitado (sin cuenta)
        4,          -- Interstellar
        11,         -- Tanda 4:30 PM
        'Pedro Rodríguez', 'pedro@email.com', '849-555-9999',
        3, 350.00, 'pendiente'
    );

-- ── Detalle de asientos por reserva ──────────────────────────
-- Reserva 1 → asientos B3, B4 (como en el demo de reservas.py)
INSERT INTO detalle_reservas (reserva_id, asiento_id)
VALUES
    (1, (SELECT id FROM asientos WHERE codigo = 'B3')),
    (1, (SELECT id FROM asientos WHERE codigo = 'B4'));

-- Reserva 2 → asiento C5
INSERT INTO detalle_reservas (reserva_id, asiento_id)
VALUES
    (2, (SELECT id FROM asientos WHERE codigo = 'C5'));

-- Reserva 3 → asientos A2, A3, A4
INSERT INTO detalle_reservas (reserva_id, asiento_id)
VALUES
    (3, (SELECT id FROM asientos WHERE codigo = 'A2')),
    (3, (SELECT id FROM asientos WHERE codigo = 'A3')),
    (3, (SELECT id FROM asientos WHERE codigo = 'A4'));


-- =============================================================
-- VERIFICACIÓN: Consultas de prueba
-- =============================================================

-- Ver todas las películas activas con su género
SELECT p.id, p.titulo, g.nombre AS genero, p.clasificacion,
       p.duracion_min, p.anio, p.calificacion
FROM peliculas p
JOIN generos g ON p.genero_id = g.id
WHERE p.estado = 'activa'
ORDER BY p.id;

-- Ver el itinerario completo (película + tandas)
SELECT p.titulo, t.hora, t.id AS tanda_id
FROM tandas t
JOIN peliculas p ON t.pelicula_id = p.id
ORDER BY p.id, t.hora;

-- Ver reservas con detalle de asientos
SELECT r.id AS reserva_id, r.nombre_cliente, p.titulo,
       t.hora AS tanda, a.codigo AS asiento, r.total, r.estado
FROM reservas r
JOIN peliculas p ON r.pelicula_id = p.id
JOIN tandas t ON r.tanda_id = t.id
JOIN detalle_reservas dr ON dr.reserva_id = r.id
JOIN asientos a ON dr.asiento_id = a.id
ORDER BY r.id;

-- Ver próximas películas
SELECT pp.titulo, g.nombre AS genero, pp.clasificacion, pp.estreno_texto
FROM proximas_peliculas pp
JOIN generos g ON pp.genero_id = g.id;
