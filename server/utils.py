import zipfile
import os

def zip_shapefile(base_name, output_zip):
    extensions = [".shp", ".shx", ".dbf", ".prj", ".cpg"]

    with zipfile.ZipFile(output_zip, 'w') as z:
        for ext in extensions:
            file = base_name.replace(".shp", ext)
            if os.path.exists(file):
                z.write(file, os.path.basename(file))
