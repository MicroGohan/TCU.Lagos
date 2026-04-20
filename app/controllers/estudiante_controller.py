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
from .auth_controller import login_required, rol_requerido
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
    return errors


# ── Rutas ──────────────────────────────────────────────────────────────────────

@estudiantes_bp.route("/")
@login_required
def index():
    """Lista todos los estudiantes o muestra resultados de búsqueda."""
    query = request.args.get("q", "").strip()
    if query:
        datos = EstudianteModel.search_with_enrollment(query)
    else:
        datos = EstudianteModel.get_all_with_enrollment()
        
    agrupados = {}
    for est in datos:
        anio = est['anio_lectivo']
        seccion = est['seccion'] or "Sin sección"
        if not anio:
            decada = "Sin clasificar"
            anio_str = "Sin año asignado"
        else:
            decada = f"{(anio // 10) * 10}s"
            anio_str = str(anio)
            
        if decada not in agrupados:
            agrupados[decada] = {}
        if anio_str not in agrupados[decada]:
            agrupados[decada][anio_str] = {}
        if seccion not in agrupados[decada][anio_str]:
            agrupados[decada][anio_str][seccion] = []
            
        # Avoid duplicate rendering if a student is returned multiple times by SQL Joins
        # and has same section
        agrupados[decada][anio_str][seccion].append(est)
        
    # We also sort the keys to display them
    
    return render_template(
        "estudiantes/index.html",
        agrupados=agrupados,
        query=query,
    )


@estudiantes_bp.route("/estudiantes/nuevo", methods=["GET", "POST"])
@login_required
@rol_requerido('admin', 'direccion')
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
                volver_url=url_for("estudiantes.index"),
                form=request.form,
            )

        try:
            EstudianteModel.create(
                cedula=request.form["cedula"].strip(),
                nombre=request.form["nombre"].strip(),
                apellido=request.form["apellido"].strip(),
                sexo=request.form.get("sexo", "").strip(),
                telefono=request.form.get("telefono", "").strip(),
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
        volver_url=url_for("estudiantes.index"),
        form={},
    )


@estudiantes_bp.route("/estudiantes/<int:estudiante_id>")
@login_required
def detalle(estudiante_id):
    """Muestra el detalle de un estudiante."""
    estudiante = EstudianteModel.get_by_id(estudiante_id)
    if estudiante is None:
        flash("Estudiante no encontrado.", "warning")
        return redirect(url_for("estudiantes.index"))
    
    calificaciones = CalificacionModel.get_by_estudiante(estudiante_id)
    
    return render_template("estudiantes/detalle.html", estudiante=estudiante, calificaciones=calificaciones)


@estudiantes_bp.route("/estudiantes/<int:estudiante_id>/editar", methods=["GET", "POST"])
@login_required
@rol_requerido('admin', 'direccion')
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
                volver_url=url_for("estudiantes.detalle", estudiante_id=estudiante_id),
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
        volver_url=url_for("estudiantes.detalle", estudiante_id=estudiante_id),
        form=dict(estudiante),
    )


@estudiantes_bp.route("/estudiantes/<int:estudiante_id>/eliminar", methods=["POST"])
@login_required
@rol_requerido('admin', 'direccion')
def eliminar(estudiante_id):
    """Elimina un estudiante."""
    estudiante = EstudianteModel.get_by_id(estudiante_id)
    if estudiante is None:
        flash("Estudiante no encontrado.", "warning")
    else:
        EstudianteModel.delete(estudiante_id)
        flash("Estudiante eliminado exitosamente.", "success")
    return redirect(url_for("estudiantes.index"))

@estudiantes_bp.route("/estudiantes/imprimir_todos")
@login_required
def imprimir_todos():
    """Genera una vista para imprimir a todos los estudiantes y sus calificaciones."""
    estudiantes = EstudianteModel.get_all()
    data = []
    for e in estudiantes:
        calificaciones = CalificacionModel.get_by_estudiante(e.id)
        data.append({'estudiante': e, 'calificaciones': calificaciones})
    return render_template("estudiantes/imprimir_todos.html", data=data)

@estudiantes_bp.route("/estudiantes/<int:estudiante_id>/imprimir")
@login_required
def imprimir_individual(estudiante_id):
    """Genera una vista para imprimir las notas de un estudiante específico."""
    estudiante = EstudianteModel.get_by_id(estudiante_id)
    if estudiante is None:
        flash("Estudiante no encontrado.", "warning")
        return redirect(url_for("estudiantes.index"))
    
    calificaciones = CalificacionModel.get_by_estudiante(estudiante_id)
    return render_template("estudiantes/imprimir.html", estudiante=estudiante, calificaciones=calificaciones)
