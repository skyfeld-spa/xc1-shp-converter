import zipfile

@app.route('/convertir', methods=['POST'])
def convertir_archivo():

    file = request.files['file']

    zip_path = "input.zip"
    extract_folder = "data"

    file.save(zip_path)

    # Extraer ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # Buscar el .shp dentro
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