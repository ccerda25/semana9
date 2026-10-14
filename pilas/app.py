from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory
)
import os

app = Flask(__name__)
app.secret_key = "clave-secreta"

stack = None

CARPETA_FOTOS = "fotos"


# Crear carpeta de fotos si no existe
os.makedirs(CARPETA_FOTOS, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    global stack

    if request.method == "POST":
        capacity = request.form.get("capacity")

        try:
            capacity = int(capacity)

            if capacity <= 0:
                flash("La capacidad debe ser mayor que 0.", "danger")
            else:
                stack = Stack(capacity)
                flash("Pila creada correctamente.", "success")

        except ValueError:
            flash("Ingrese un número válido.", "danger")

        return redirect(url_for("index"))

    fotos = os.listdir(CARPETA_FOTOS)

    return render_template(
        "index.html",
        stack=stack,
        fotos=fotos
    )


@app.route("/push", methods=["POST"])
def push():
    global stack

    if stack is None:
        flash("Primero debes crear una pila.", "warning")
        return redirect(url_for("index"))

    item = request.form.get("item", "").strip()

    if not item:
        flash("Debes ingresar un valor.", "warning")
        return redirect(url_for("index"))

    if stack.push(item):
        flash(f"Elemento '{item}' apilado correctamente.", "success")
    else:
        flash("La pila está llena.", "danger")

    return redirect(url_for("index"))


@app.route("/pop", methods=["POST"])
def pop():
    global stack

    if stack is None:
        flash("Primero debes crear una pila.", "warning")
        return redirect(url_for("index"))

    item = stack.pop()

    if item is None:
        flash("La pila está vacía.", "warning")
    else:
        flash(f"Elemento '{item}' desapilado.", "success")

    return redirect(url_for("index"))


@app.route("/peek")
def peek():
    if stack is None:
        flash("Primero debes crear una pila.", "warning")
    elif stack.peek() is None:
        flash("La pila está vacía.", "warning")
    else:
        flash(f"El elemento en el tope es: {stack.peek()}", "info")

    return redirect(url_for("index"))


@app.route("/guardar-foto", methods=["POST"])
def guardar_foto():
    imagen = request.json.get("imagen")

    if not imagen:
        return {
            "exito": False,
            "mensaje": "No se recibió ninguna imagen."
        }, 400

    try:
        # Eliminar la información inicial del formato Base64
        imagen = imagen.split(",")[1]

        datos = base64.b64decode(imagen)

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        ruta = os.path.join(CARPETA_FOTOS, f"foto_{nombre}.jpg")

        with open(ruta, "wb") as archivo:
            archivo.write(datos)

        return {
            "exito": True,
            "mensaje": "Foto guardada correctamente."
        }

    except Exception:
        return {
            "exito": False,
            "mensaje": "No se pudo guardar la foto."
        }, 500


if __name__ == "__main__":
    app.run(debug=True)