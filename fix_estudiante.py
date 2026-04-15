
import re

with open("app/controllers/estudiante_controller.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace CARRERAS block
text = re.sub(r"CARRERAS = \[.*?\]\n\n", "", text, flags=re.DOTALL)

# Replace _validate_form
text = re.sub(
    r"(if not form.get\(\"apellido\", \"\"\).strip\(\):\n\s+errors.append\(.*?\)[\s\S]*?)return errors",
    "if not form.get(\"apellido\", \"\").strip():\n        errors.append(\"El apellido es obligatorio.\")\n    if not form.get(\"seccion\", \"\").strip():\n        errors.append(\"La sección es obligatoria.\")\n    return errors",
    text
)

# Replace references to create/update params in route functions
text = text.replace("carreras=CARRERAS,\n", "")
text = text.replace("email=request.form[\"email\"]", "sexo=request.form.get(\"sexo\", \"\")")
text = text.replace("carrera=request.form[\"carrera\"]", "seccion=request.form[\"seccion\"]")
text = text.replace("La cédula o el correo ya están", "La cédula ya está")
text = text.replace("La cÃdula o el correo ya estÃ¡n", "La cÃdula ya estÃ¡")

with open("app/controllers/estudiante_controller.py", "w", encoding="utf-8") as f:
    f.write(text)

