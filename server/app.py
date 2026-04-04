from flask import Flask, request, send_file, render_template
from converter import convertir
from utils import zip_shapefile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convertir', methods=['POST'])
def convertir_archivo():
    file = request.files['file']

    input_path = "input.shp"
    output_path = "output.shp"
    zip_path = "resultado.zip"

    file.save(input_path)

    try:
        convertir(input_path, output_path)
        zip_shapefile(output_path, zip_path)
        return send_file(zip_path, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
