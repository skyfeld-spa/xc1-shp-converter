import os
import zipfile
from flask import Flask, request, send_file, render_template
from converter import convertir
from utils import zip_shapefile

# 👇 PRIMERO se crea app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convertir', methods=['POST'])
def convertir_archivo():

    file = request.files['file']

    zip_path = "input.zip"
    extract_folder = "data"

    file.save(zip_path)

    # Crear carpeta si no existe
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    # Extraer ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # Buscar shapefile
    shp_file = None
    for f in os.listdir(extract_folder):
        if f.endswith(".shp"):
            shp_file = os.path.join(extract_folder, f)

    if not shp_file:
        return "No se encontró archivo .shp en el ZIP"

    output_path = "output.shp"
    zip_output = "resultado.zip"

    try:
        convertir(shp_file, output_path)
        zip_shapefile(output_path, zip_output)

        return send_file(zip_output, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)