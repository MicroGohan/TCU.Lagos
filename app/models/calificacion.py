"""
Modelo Calificacion - TCU Lagos
Encapsula operaciones sobre la tabla 'calificaciones'.
"""
from .database import get_db
from flask import g, current_app
import sqlite3

def _get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db

def get_by_estudiante(estudiante_id):
    db = _get_db()
    return db.execute(
        "SELECT * FROM calificaciones WHERE estudiante_id = ? ORDER BY anio_lectivo DESC, periodo DESC",
        (estudiante_id,)
    ).fetchall()

def get_by_id(calificacion_id):
    db = _get_db()
    return db.execute(
        "SELECT * FROM calificaciones WHERE id = ?", (calificacion_id,)
    ).fetchone()

def create(data):
    db = _get_db()
    cursor = db.execute(
        """INSERT INTO calificaciones (
            estudiante_id, anio_lectivo, periodo, estudios_sociales, ciencias, espanol,
            matematica, educacion_agricola, ingles, educacion_musical,
            educacion_religiosa, educacion_fisica, educacion_hogar,
            artes_industriales, artes_plasticas, frances, conducta, estado_final
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data["estudiante_id"], data.get("anio_lectivo"), data.get("periodo"),
            data.get("estudios_sociales"), data.get("ciencias"), data.get("espanol"),
            data.get("matematica"), data.get("educacion_agricola"), data.get("ingles"),
            data.get("educacion_musical"), data.get("educacion_religiosa"), data.get("educacion_fisica"),
            data.get("educacion_hogar"), data.get("artes_industriales"), data.get("artes_plasticas"),
            data.get("frances"), data.get("conducta"), data.get("estado_final")
        )
    )
    db.commit()
    return cursor.lastrowid

def update(calificacion_id, data):
    db = _get_db()
    db.execute(
        """UPDATE calificaciones SET
            anio_lectivo=?, periodo=?, estudios_sociales=?, ciencias=?, espanol=?,
            matematica=?, educacion_agricola=?, ingles=?, educacion_musical=?,
            educacion_religiosa=?, educacion_fisica=?, educacion_hogar=?,
            artes_industriales=?, artes_plasticas=?, frances=?, conducta=?, estado_final=?
        WHERE id=?""",
        (
            data.get("anio_lectivo"), data.get("periodo"), data.get("estudios_sociales"),
            data.get("ciencias"), data.get("espanol"), data.get("matematica"),
            data.get("educacion_agricola"), data.get("ingles"), data.get("educacion_musical"),
            data.get("educacion_religiosa"), data.get("educacion_fisica"), data.get("educacion_hogar"),
            data.get("artes_industriales"), data.get("artes_plasticas"), data.get("frances"),
            data.get("conducta"), data.get("estado_final"),
            calificacion_id
        )
    )
    db.commit()

def delete(calificacion_id):
    db = _get_db()
    db.execute("DELETE FROM calificaciones WHERE id = ?", (calificacion_id,))
    db.commit()
