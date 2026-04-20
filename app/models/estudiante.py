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


def get_all_with_enrollment():
    """Retorna todos los estudiantes con su sección y año lectivo (si tienen), ordenados por año y sección."""
    db = _get_db()
    return db.execute(
        """SELECT e.*, c.anio_lectivo, c.seccion 
           FROM estudiantes e 
           LEFT JOIN calificaciones c ON e.id = c.estudiante_id 
           ORDER BY c.anio_lectivo DESC, c.seccion ASC, e.apellido, e.nombre"""
    ).fetchall()


def search_with_enrollment(query):
    """Busca estudiantes con múltiples filtros cruzados, incluyendo año, sección y nacimiento."""
    like = f"%{query}%"
    db = _get_db()
    return db.execute(
        """SELECT e.*, c.anio_lectivo, c.seccion 
           FROM estudiantes e 
           LEFT JOIN calificaciones c ON e.id = c.estudiante_id 
           WHERE e.nombre LIKE ? 
              OR e.apellido LIKE ? 
              OR e.cedula LIKE ? 
              OR strftime('%Y', e.fecha_nac) LIKE ?
              OR CAST(c.anio_lectivo AS TEXT) LIKE ?
              OR c.seccion LIKE ?
           ORDER BY c.anio_lectivo DESC, c.seccion ASC, e.apellido, e.nombre""",
        (like, like, like, like, like, like),
    ).fetchall()

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
