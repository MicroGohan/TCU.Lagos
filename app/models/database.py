"""
Módulo de base de datos - TCU Lagos
Gestiona la conexión y la inicialización del esquema SQLite.
"""
import sqlite3
import click
from flask import g, current_app


def get_db(app=None):
    """Retorna la conexión a la base de datos, creándola si no existe."""
    if app is None:
        app = current_app
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Cierra la conexión a la base de datos al finalizar la petición."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


SCHEMA_DROP_SQL = """
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS estudiantes;
DROP TABLE IF EXISTS calificaciones;
"""

SCHEMA_CREATE_SQL = """
CREATE TABLE IF NOT EXISTS usuarios (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    rol             TEXT NOT NULL CHECK(rol IN ('admin', 'direccion', 'docente')),
    nombre_completo TEXT NOT NULL,
    creado_en       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS estudiantes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula      TEXT    NOT NULL UNIQUE,
    nombre      TEXT    NOT NULL,
    apellido    TEXT    NOT NULL,
    sexo        TEXT,

    fecha_nac   TEXT,
    telefono    TEXT,
    creado_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS calificaciones (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id       INTEGER NOT NULL,
    anio_lectivo        INTEGER,
    periodo             TEXT,
    seccion             TEXT,
    estudios_sociales     INTEGER,
    ciencias            INTEGER,
    espanol             INTEGER,
    matematica          INTEGER,
    educacion_agricola  INTEGER,
    ingles              INTEGER,
    educacion_musical   INTEGER,
    educacion_religiosa INTEGER,
    educacion_fisica    INTEGER,
    educacion_hogar     INTEGER,
    artes_industriales  INTEGER,
    artes_plasticas     INTEGER,
    frances             INTEGER,
    conducta            INTEGER,
    estado_final        TEXT,
    FOREIGN KEY(estudiante_id) REFERENCES estudiantes(id)
);
"""


def init_db(app):
    """Registra las funciones de base de datos y crea las tablas."""
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"])
        db.executescript(SCHEMA_CREATE_SQL)
        db.commit()
        db.close()

    @app.cli.command("init-db")
    def init_db_command():
        """Recrea las tablas de la base de datos."""
        with app.app_context():
            db = sqlite3.connect(app.config["DATABASE"])
            db.executescript(SCHEMA_DROP_SQL)
            db.executescript(SCHEMA_CREATE_SQL)
            db.commit()
            db.close()
        click.echo("Base de datos inicializada.")
