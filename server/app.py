import os
import zipfile
import geopandas as gpd
from flask import Flask, request, send_file, render_template
from converter import convertir
from utils import zip_shapefile

# Crear app
app = Flask(__name__)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')


# Ruta de conversión
@app.route('/convertir', methods=['POST'])
def convertir_archivo():

    file = request.files['file']

    zip_path = "input.zip"
    extract_folder = "data"

    # Guardar archivo ZIP
    file.save(zip_path)

    # Crear carpeta si no existe
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    # Limpiar carpeta (importante)
    for f in os.listdir(extract_folder):
        os.remove(os.path.join(extract_folder, f))

    # Extraer ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # 🔥 Buscar shapefile válido automáticamente
    shp_file = None

    for f in os.listdir(extract_folder):
        if f.endswith(".shp"):
            path = os.path.join(extract_folder, f)
            try:
                gdf = gpd.read_file(path)

                print(f"Probando archivo: {f}")
                print("Tipos geometría:", gdf.geometry.type.unique())

                if not gdf.empty:
                    shp_file = path
                    break

            except Exception as e:
                print(f"Error leyendo {f}: {e}")
                continue

    if not shp_file:
        return "<h2>Error:</h2><p>No se encontró shapefile válido en el ZIP</p>"

    output_path = "output.shp"
    zip_output = "resultado_skyfeld.zip"

    try:
        convertir(shp_file, output_path)
        zip_shapefile(output_path, zip_output)

        return send_file(zip_output, as_attachment=True)

    except Exception as e:
        return f"<h2>Error:</h2><p>{str(e)}</p>"


# Ejecutar servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)