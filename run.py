"""
TCU Lagos - Sistema de Gestión de Estudiantes
Punto de entrada de la aplicación
"""
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
