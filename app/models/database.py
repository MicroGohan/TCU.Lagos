"""
Módulo de base de datos - TCU Lagos
Gestiona la conexión y la inicialización del esquema SQLite.
"""
import sqlite3
import click
from flask import g


def get_db(app):
    """Retorna la conexión a la base de datos, creándola si no existe."""
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Cierra la conexión a la base de datos al finalizar la petición."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS estudiantes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula      TEXT    NOT NULL UNIQUE,
    nombre      TEXT    NOT NULL,
    apellido    TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE,
    telefono    TEXT,
    carrera     TEXT    NOT NULL,
    fecha_nac   TEXT,
    creado_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db(app):
    """Registra las funciones de base de datos y crea las tablas."""
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"])
        db.executescript(SCHEMA_SQL)
        db.commit()
        db.close()

    @app.cli.command("init-db")
    def init_db_command():
        """Recrea las tablas de la base de datos."""
        with app.app_context():
            db = sqlite3.connect(app.config["DATABASE"])
            db.executescript(SCHEMA_SQL)
            db.commit()
            db.close()
        click.echo("Base de datos inicializada.")
