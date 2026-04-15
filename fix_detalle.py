
with open("app/templates/estudiantes/detalle.html", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("{{ estudiante.carrera }}", "{{ estudiante.seccion }}")
text = text.replace("Correo ElectrÃnico", "Sexo")
text = text.replace("{{ estudiante.email }}", "{{ estudiante.sexo }}")

with open("app/templates/estudiantes/detalle.html", "w", encoding="utf-8") as f:
    f.write(text)

