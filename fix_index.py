
with open("app/templates/estudiantes/index.html", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("<th>Carrera</th>", "<th>Sección</th>")
text = text.replace("<th>Correo</th>", "<th>Sexo</th>")
text = text.replace("<td><span class=\"badge\">{{ e.carrera }}</span></td>", "<td><span class=\"badge\">{{ e.seccion }}</span></td>")
text = text.replace("<td>{{ e.email }}</td>", "<td>{{ e.sexo }}</td>")

with open("app/templates/estudiantes/index.html", "w", encoding="utf-8") as f:
    f.write(text)

