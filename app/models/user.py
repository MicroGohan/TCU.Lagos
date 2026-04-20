import sqlite3
from .database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, id, username, password_hash, rol, nombre_completo):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.rol = rol
        self.nombre_completo = nombre_completo

    @classmethod
    def create(cls, username, password, rol, nombre_completo):
        db = get_db()
        try:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO usuarios (username, password_hash, rol, nombre_completo) VALUES (?, ?, ?, ?)",
                (username, generate_password_hash(password), rol, nombre_completo)
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Si el username ya existe
            return None

    @classmethod
    def get_by_username(cls, username):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return cls(row['id'], row['username'], row['password_hash'], row['rol'], row['nombre_completo'])
        return None

    @classmethod
    def get_by_id(cls, user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return cls(row['id'], row['username'], row['password_hash'], row['rol'], row['nombre_completo'])
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_all(cls):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY id ASC")
        return [cls(row['id'], row['username'], row['password_hash'], row['rol'], row['nombre_completo']) for row in cursor.fetchall()]

    @classmethod
    def ensure_default_admin(cls):
        # Crear un admin por defecto si la base de datos está vacía
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM usuarios")
        count = cursor.fetchone()['count']
        if count == 0:
            cls.create('admin', 'admin123', 'admin', 'Administrador del Sistema')
            cls.create('director', 'director123', 'direccion', 'Director de Escuela')
            cls.create('profesor', 'profe123', 'docente', 'Profesor Regular')
