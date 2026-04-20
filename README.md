# TCU Lagos — Sistema de Gestión de Estudiantes

Trabajo Comunal Universitario de la Escuela Los Lagos.  
Aplicación web **MVC** con base de datos **SQLite** para el registro y gestión de estudiantes.

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Lenguaje | Python 3.12 |
| Framework web | Flask 3 |
| Base de datos | SQLite (vía módulo `sqlite3`) |
| Plantillas | Jinja2 (incluido en Flask) |

## Arquitectura MVC

```
app/
├── models/
│   ├── database.py        # Conexión e inicialización del esquema SQL
│   └── estudiante.py      # Operaciones CRUD sobre la tabla estudiantes
├── controllers/
│   └── estudiante_controller.py  # Rutas y lógica de negocio
├── templates/
│   ├── base.html
│   └── estudiantes/
│       ├── index.html     # Listado y búsqueda
│       ├── form.html      # Formulario (crear / editar)
│       └── detalle.html   # Vista de detalle
└── static/
    └── css/style.css
run.py                     # Punto de entrada
tests.py                   # Pruebas unitarias (pytest)
requirements.txt
```

## Funcionalidades

- **Registrar** estudiantes (cédula, nombre, apellido, correo, teléfono, carrera, fecha de nacimiento)
- **Listar** todos los estudiantes
- **Buscar** por nombre, apellido o cédula
- **Ver detalle** de un estudiante
- **Editar** datos de un estudiante
- **Eliminar** un estudiante

## Instalación y ejecución

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
python run.py
# La app estará disponible en http://127.0.0.1:5000
```

## Pruebas

```bash
pip install pytest
python -m pytest tests.py -v
```
