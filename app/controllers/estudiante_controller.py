"""
Controlador de Estudiantes - TCU Lagos
Define las rutas y la lógica de negocio para la gestión de estudiantes.
"""
import sqlite3
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from ..models import estudiante as EstudianteModel
from ..models import calificacion as CalificacionModel

estudiantes_bp = Blueprint("estudiantes", __name__, url_prefix="/")


def _validate_form(form):
    """Valida los campos del formulario y retorna una lista de errores."""
    errors = []
    if not form.get("cedula", "").strip():
        errors.append("La cédula es obligatoria.")
    if not form.get("nombre", "").strip():
        errors.append("El nombre es obligatorio.")
    if not form.get("apellido", "").strip():
        errors.append("El apellido es obligatorio.")
    if not form.get("seccion", "").strip():
        errors.append("La sección es obligatoria.")
    return errors


# ── Rutas ──────────────────────────────────────────────────────────────────────

@estudiantes_bp.route("/")
def index():
    """Lista todos los estudiantes o muestra resultados de búsqueda."""
    query = request.args.get("q", "").strip()
    if query:
        estudiantes = EstudianteModel.search(query)
    else:
        estudiantes = EstudianteModel.get_all()
    return render_template(
        "estudiantes/index.html",
        estudiantes=estudiantes,
        query=query,
    )


@estudiantes_bp.route("/estudiantes/nuevo", methods=["GET", "POST"])
def nuevo():
    """Muestra el formulario de registro y procesa la creación."""
    if request.method == "POST":
        errors = _validate_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "estudiantes/form.html",
                titulo="Registrar Estudiante",
                accion=url_for("estudiantes.nuevo"),
                                form=request.form,
            )

        try:
            EstudianteModel.create(
                cedula=request.form["cedula"].strip(),
                nombre=request.form["nombre"].strip(),
                apellido=request.form["apellido"].strip(),
                sexo=request.form.get("sexo", "").strip(),
                telefono=request.form.get("telefono", "").strip(),
                seccion=request.form["seccion"].strip(),
                fecha_nac=request.form.get("fecha_nac", "").strip() or None,
            )
            flash("Estudiante registrado exitosamente.", "success")
            return redirect(url_for("estudiantes.index"))
        except sqlite3.IntegrityError:
            flash("La cédula ya está registrada.", "danger")

    return render_template(
        "estudiantes/form.html",
        titulo="Registrar Estudiante",
        accion=url_for("estudiantes.nuevo"),
                form={},
    )


@estudiantes_bp.route("/estudiantes/<int:estudiante_id>")
def detalle(estudiante_id):
    """Muestra el detalle de un estudiante."""
    estudiante = EstudianteModel.get_by_id(estudiante_id)
    if estudiante is None:
        flash("Estudiante no encontrado.", "warning")
        return redirect(url_for("estudiantes.index"))
    
    calificaciones = CalificacionModel.get_by_estudiante(estudiante_id)
    
    return render_template("estudiantes/detalle.html", estudiante=estudiante, calificaciones=calificaciones)


@estudiantes_bp.route("/estudiantes/<int:estudiante_id>/editar", methods=["GET", "POST"])
def editar(estudiante_id):
    """Muestra el formulario de edición y procesa la actualización."""
    estudiante = EstudianteModel.get_by_id(estudiante_id)
    if estudiante is None:
        flash("Estudiante no encontrado.", "warning")
        return redirect(url_for("estudiantes.index"))

    if request.method == "POST":
        errors = _validate_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "estudiantes/form.html",
                titulo="Editar Estudiante",
                accion=url_for("estudiantes.editar", estudiante_id=estudiante_id),
                                form=request.form,
            )

        try:
            EstudianteModel.update(
                estudiante_id=estudiante_id,
                cedula=request.form["cedula"].strip(),
                nombre=request.form["nombre"].strip(),
                apellido=request.form["apellido"].strip(),
                sexo=request.form.get("sexo", "").strip(),
                telefono=request.form.get("telefono", "").strip(),
                seccion=request.form["seccion"].strip(),
                fecha_nac=request.form.get("fecha_nac", "").strip() or None,
            )
            flash("Estudiante actualizado exitosamente.", "success")
            return redirect(url_for("estudiantes.detalle", estudiante_id=estudiante_id))
        except sqlite3.IntegrityError:
            flash("La cédula ya está registrada por otro estudiante.", "danger")

    return render_template(
        "estudiantes/form.html",
        titulo="Editar Estudiante",
        accion=url_for("estudiantes.editar", estudiante_id=estudiante_id),
                form=dict(estudiante),
    )


@estudiantes_bp.route("/estudiantes/<int:estudiante_id>/eliminar", methods=["POST"])
def eliminar(estudiante_id):
    """Elimina un estudiante."""
    estudiante = EstudianteModel.get_by_id(estudiante_id)
    if estudiante is None:
        flash("Estudiante no encontrado.", "warning")
    else:
        EstudianteModel.delete(estudiante_id)
        flash("Estudiante eliminado exitosamente.", "success")
    return redirect(url_for("estudiantes.index"))
