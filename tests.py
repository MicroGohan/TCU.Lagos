"""
Pruebas unitarias - TCU Lagos
Sistema de Gestión de Estudiantes
"""
import pytest
import sqlite3
import os
from app import create_app
from app.models.database import SCHEMA_SQL


@pytest.fixture
def app():
    """Crea una instancia de la app configurada para pruebas."""
    test_db = "/tmp/test_tcu_lagos.db"
    application = create_app()
    application.config.update({
        "TESTING": True,
        "DATABASE": test_db,
    })

    # Crear tablas en la BD de prueba
    db = sqlite3.connect(test_db)
    db.executescript(SCHEMA_SQL)
    db.commit()
    db.close()

    yield application

    # Limpiar BD de prueba
    if os.path.exists(test_db):
        os.remove(test_db)


@pytest.fixture
def client(app):
    return app.test_client()


# ── Tests de rutas ─────────────────────────────────────────────

class TestIndex:
    def test_index_returns_200(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_index_shows_title(self, client):
        r = client.get("/")
        assert b"Estudiantes Registrados" in r.data

    def test_index_empty_state(self, client):
        r = client.get("/")
        assert b"No hay estudiantes registrados" in r.data


class TestCrearEstudiante:
    def test_get_form_returns_200(self, client):
        r = client.get("/estudiantes/nuevo")
        assert r.status_code == 200

    def test_create_student_redirects(self, client):
        r = client.post("/estudiantes/nuevo", data={
            "cedula": "1-1111-1111",
            "nombre": "Ana",
            "apellido": "López",
            "email": "ana@test.com",
            "carrera": "Educación",
        })
        assert r.status_code == 302

    def test_create_student_shows_success(self, client):
        r = client.post("/estudiantes/nuevo", data={
            "cedula": "1-2222-2222",
            "nombre": "Luis",
            "apellido": "Mora",
            "email": "luis@test.com",
            "carrera": "Ingeniería en Sistemas",
        }, follow_redirects=True)
        assert b"exitosamente" in r.data

    def test_create_student_missing_fields(self, client):
        r = client.post("/estudiantes/nuevo", data={
            "cedula": "",
            "nombre": "",
            "apellido": "",
            "email": "",
            "carrera": "",
        }, follow_redirects=True)
        assert b"obligatori" in r.data

    def test_duplicate_cedula_shows_error(self, client):
        data = {
            "cedula": "1-3333-3333",
            "nombre": "Pedro",
            "apellido": "Castro",
            "email": "pedro@test.com",
            "carrera": "Contabilidad",
        }
        client.post("/estudiantes/nuevo", data=data)
        data["email"] = "pedro2@test.com"
        r = client.post("/estudiantes/nuevo", data=data, follow_redirects=True)
        assert b"ya est" in r.data


class TestDetalleEstudiante:
    def _create(self, client):
        client.post("/estudiantes/nuevo", data={
            "cedula": "1-4444-4444",
            "nombre": "Sofía",
            "apellido": "Vargas",
            "email": "sofia@test.com",
            "carrera": "Medicina",
        })

    def test_detail_returns_200(self, client):
        self._create(client)
        r = client.get("/estudiantes/1")
        assert r.status_code == 200

    def test_detail_shows_name(self, client):
        self._create(client)
        r = client.get("/estudiantes/1")
        assert "Sofía".encode() in r.data

    def test_detail_not_found_redirects(self, client):
        r = client.get("/estudiantes/999", follow_redirects=True)
        assert b"no encontrado" in r.data


class TestEditarEstudiante:
    def _create(self, client):
        client.post("/estudiantes/nuevo", data={
            "cedula": "1-5555-5555",
            "nombre": "Roberto",
            "apellido": "Jiménez",
            "email": "roberto@test.com",
            "carrera": "Derecho",
        })

    def test_edit_form_returns_200(self, client):
        self._create(client)
        r = client.get("/estudiantes/1/editar")
        assert r.status_code == 200

    def test_edit_updates_student(self, client):
        self._create(client)
        r = client.post("/estudiantes/1/editar", data={
            "cedula": "1-5555-5555",
            "nombre": "Roberto Carlos",
            "apellido": "Jiménez",
            "email": "roberto@test.com",
            "carrera": "Derecho",
        }, follow_redirects=True)
        assert b"actualizado exitosamente" in r.data


class TestEliminarEstudiante:
    def _create(self, client):
        client.post("/estudiantes/nuevo", data={
            "cedula": "1-6666-6666",
            "nombre": "Elena",
            "apellido": "Solano",
            "email": "elena@test.com",
            "carrera": "Arquitectura",
        })

    def test_delete_student(self, client):
        self._create(client)
        r = client.post("/estudiantes/1/eliminar", follow_redirects=True)
        assert b"eliminado exitosamente" in r.data

    def test_deleted_student_not_in_list(self, client):
        self._create(client)
        client.post("/estudiantes/1/eliminar")
        r = client.get("/")
        assert b"Elena" not in r.data


class TestBusqueda:
    def test_search_finds_student(self, client):
        client.post("/estudiantes/nuevo", data={
            "cedula": "1-7777-7777",
            "nombre": "Andrés",
            "apellido": "Morales",
            "email": "andres@test.com",
            "carrera": "Ingeniería Industrial",
        })
        r = client.get("/?q=Andrés")
        assert "Andrés".encode() in r.data

    def test_search_no_results(self, client):
        r = client.get("/?q=XYZNoExiste")
        assert b"No se encontraron" in r.data
