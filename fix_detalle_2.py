
with open("app/templates/estudiantes/detalle.html", "r", encoding="utf-8") as f:
    text = f.read()

part_to_add = """
    <div class="mt-4">
        <h3>Calificaciones</h3>
        <a href="{{ url_for('calificaciones.nueva', estudiante_id=estudiante.id) }}" class="btn btn-sm btn-primary mb-2">+ Añadir Calificaciones</a>
        
        {% if calificaciones %}
            <div class="table-responsive">
                <table class="table table-striped table-bordered text-center">
                    <thead>
                        <tr>
                            <th>Año / Periodo</th>
                            <th>Soc</th>
                            <th>Cien</th>
                            <th>Esp</th>
                            <th>Mat</th>
                            <th>Agri</th>
                            <th>Ing</th>
                            <th>Mus</th>
                            <th>Rel</th>
                            <th>Fís</th>
                            <th>Hog</th>
                            <th>Ind</th>
                            <th>Plás</th>
                            <th>Fra</th>
                            <th>Cond</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for calc in calificaciones %}
                        <tr>
                            <td>{{ calc.anio_lectivo }} {% if calc.periodo %} - {{ calc.periodo }}{% endif %}</td>
                            <td>{{ calc.estudios_sociales or "-" }}</td>
                            <td>{{ calc.ciencias or "-" }}</td>
                            <td>{{ calc.espanol or "-" }}</td>
                            <td>{{ calc.matematica or "-" }}</td>
                            <td>{{ calc.educacion_agricola or "-" }}</td>
                            <td>{{ calc.ingles or "-" }}</td>
                            <td>{{ calc.educacion_musical or "-" }}</td>
                            <td>{{ calc.educacion_religiosa or "-" }}</td>
                            <td>{{ calc.educacion_fisica or "-" }}</td>
                            <td>{{ calc.educacion_hogar or "-" }}</td>
                            <td>{{ calc.artes_industriales or "-" }}</td>
                            <td>{{ calc.artes_plasticas or "-" }}</td>
                            <td>{{ calc.frances or "-" }}</td>
                            <td>{{ calc.conducta or "-" }}</td>
                            <td><strong>{{ calc.estado_final or "-" }}</strong></td>
                            <td>
                                <a href="{{ url_for('calificaciones.editar', estudiante_id=estudiante.id, calificacion_id=calc.id) }}" class="btn btn-sm btn-warning">Editar</a>
                                <form method="post" action="{{ url_for('calificaciones.eliminar', estudiante_id=estudiante.id, calificacion_id=calc.id) }}" style="display:inline;" onsubmit="return confirm('¿Eliminar estas calificaciones?')">
                                    <button type="submit" class="btn btn-sm btn-danger">Eliminar</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <p class="text-muted mt-2">No hay calificaciones registradas para este estudiante.</p>
        {% endif %}
    </div>

    <div class="form-actions mt-4">
"""

text = text.replace("    <div class=\"form-actions mt-4\">", part_to_add)

with open("app/templates/estudiantes/detalle.html", "w", encoding="utf-8") as f:
    f.write(text)

