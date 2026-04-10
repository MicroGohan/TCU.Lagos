"""
TCU Lagos - Sistema de Gestión de Estudiantes
Punto de entrada de la aplicación
"""
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
