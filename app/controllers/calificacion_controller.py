"""
Controlador de Calificaciones - TCU Lagos
Define rutas para la gestión de las notas de los estudiantes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .auth_controller import login_required, rol_requerido
from ..models import estudiante as EstudianteModel
from ..models import calificacion as CalificacionModel

calificaciones_bp = Blueprint("calificaciones", __name__, url_prefix="/estudiantes/<int:estudiante_id>/calificaciones")

MATERIAS = [
    "estudios_sociales", "ciencias", "espanol", "matematica",
    "educacion_agricola", "ingles", "educacion_musical",
    "educacion_religiosa", "educacion_fisica", "educacion_hogar",
    "artes_industriales", "artes_plasticas", "frances", "conducta"
]

@calificaciones_bp.route("/nueva", methods=["GET", "POST"])
@login_required
@rol_requerido('admin', 'direccion')
def nueva(estudiante_id):
    estudiante = EstudianteModel.get_by_id(estudiante_id)
    if not estudiante:
        flash("Estudiante no encontrado.", "danger")
        return redirect(url_for("estudiantes.index"))

    if request.method == "POST":
        data = {
            "estudiante_id": estudiante_id,
            "anio_lectivo": request.form.get("anio_lectivo", "").strip() or None,
            "periodo": request.form.get("periodo", "").strip() or None,
            "seccion": request.form.get("seccion", "").strip() or None,
            "estado_final": request.form.get("estado_final", "").strip() or None,
        }
        for mat in MATERIAS:
            val = request.form.get(mat, "").strip()
            data[mat] = val if val else None

        CalificacionModel.create(data)
        flash("Calificaciones registradas.", "success")
        return redirect(url_for("estudiantes.detalle", estudiante_id=estudiante_id))

    return render_template(
        "calificaciones/form.html",
        titulo="Registrar Calificaciones",
        estudiante=estudiante,
        form={}
    )

@calificaciones_bp.route("/<int:calificacion_id>/editar", methods=["GET", "POST"])
@login_required
@rol_requerido('admin', 'direccion')
def editar(estudiante_id, calificacion_id):
    estudiante = EstudianteModel.get_by_id(estudiante_id)
    calificacion = CalificacionModel.get_by_id(calificacion_id)
    if not estudiante or not calificacion:
        flash("Registro no encontrado.", "danger")
        return redirect(url_for("estudiantes.index"))

    if request.method == "POST":
        data = {
            "anio_lectivo": request.form.get("anio_lectivo", "").strip() or None,
            "periodo": request.form.get("periodo", "").strip() or None,
            "seccion": request.form.get("seccion", "").strip() or None,
            "estado_final": request.form.get("estado_final", "").strip() or None,
        }
        for mat in MATERIAS:
            val = request.form.get(mat, "").strip()
            data[mat] = val if val else None

        CalificacionModel.update(calificacion_id, data)
        flash("Calificaciones actualizadas.", "success")
        return redirect(url_for("estudiantes.detalle", estudiante_id=estudiante_id))

    return render_template(
        "calificaciones/form.html",
        titulo="Editar Calificaciones",
        estudiante=estudiante,
        form=dict(calificacion)
    )

@calificaciones_bp.route("/<int:calificacion_id>/eliminar", methods=["POST"])
@login_required
@rol_requerido('admin', 'direccion')
def eliminar(estudiante_id, calificacion_id):
    CalificacionModel.delete(calificacion_id)
    flash("Calificaciones eliminadas.", "success")
    return redirect(url_for("estudiantes.detalle", estudiante_id=estudiante_id))