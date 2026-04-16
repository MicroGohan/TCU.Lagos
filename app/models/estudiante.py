"""
Modelo Estudiante - TCU Lagos
Encapsula todas las operaciones CRUD sobre la tabla 'estudiantes'.
"""
import sqlite3
from flask import g, current_app


def _get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def get_all():
    """Retorna todos los estudiantes ordenados por apellido."""
    db = _get_db()
    return db.execute(
        "SELECT * FROM estudiantes ORDER BY apellido, nombre"
    ).fetchall()


def get_by_id(estudiante_id):
    """Retorna un estudiante por su id, o None si no existe."""
    db = _get_db()
    return db.execute(
        "SELECT * FROM estudiantes WHERE id = ?", (estudiante_id,)
    ).fetchone()


def create(cedula, nombre, apellido, sexo, fecha_nac, telefono):
    """Inserta un nuevo estudiante y retorna su id."""
    db = _get_db()
    cursor = db.execute(
        """INSERT INTO estudiantes
           (cedula, nombre, apellido, sexo, fecha_nac, telefono)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (cedula, nombre, apellido, sexo, fecha_nac, telefono),
    )
    db.commit()
    return cursor.lastrowid


def update(estudiante_id, cedula, nombre, apellido, sexo, fecha_nac, telefono):
    """Actualiza los datos de un estudiante existente."""
    db = _get_db()
    db.execute(
        """UPDATE estudiantes
           SET cedula=?, nombre=?, apellido=?, sexo=?,
               fecha_nac=?, telefono=?
           WHERE id=?""",
        (cedula, nombre, apellido, sexo, fecha_nac, telefono, estudiante_id),
    )
    db.commit()


def delete(estudiante_id):
    """Elimina un estudiante por su id."""
    db = _get_db()
    db.execute("DELETE FROM estudiantes WHERE id = ?", (estudiante_id,))
    db.commit()


def search(query):
    """Busca estudiantes por nombre, apellido o cédula."""
    like = f"%{query}%"
    db = _get_db()
    return db.execute(
        """SELECT * FROM estudiantes
           WHERE nombre LIKE ? OR apellido LIKE ? OR cedula LIKE ?
           ORDER BY apellido, nombre""",
        (like, like, like),
    ).fetchall()
