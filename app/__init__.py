"""
Paquete principal de la aplicación Flask - TCU Lagos
Patrón MVC: este módulo inicializa la aplicación y registra los blueprints.
"""
import os
from flask import Flask
from .models.database import init_db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "tcu-lagos-dev-secret-key")
    app.config["DATABASE"] = "estudiantes.db"

    # Inicializar la base de datos
    init_db(app)

    # Registrar controladores (blueprints)
    from .controllers.auth_controller import auth_bp
    from .controllers.estudiante_controller import estudiantes_bp
    from .controllers.calificacion_controller import calificaciones_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(estudiantes_bp)
    app.register_blueprint(calificaciones_bp)

    return app
