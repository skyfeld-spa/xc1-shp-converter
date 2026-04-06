import geopandas as gpd

def convertir(input_path, output_path):

    gdf = gpd.read_file(input_path)

    print("Geometrías detectadas:", gdf.geometry.type.unique())

    if gdf.empty:
        raise Exception("Shapefile vacío")

    if gdf.crs is None:
        raise Exception("Sin sistema de coordenadas")

    # Convertir a WGS84
    gdf = gdf.to_crs(epsg=4326)

    # 🔥 CONVERTIR TODO A LÍNEA (CLAVE)
    nuevas_geometrias = []

    for geom in gdf.geometry:
        if geom is None:
            continue

        if geom.geom_type == "LineString":
            nuevas_geometrias.append(geom)

        elif geom.geom_type == "MultiLineString":
            for part in geom:
                nuevas_geometrias.append(part)

        elif geom.geom_type == "Polygon":
            nuevas_geometrias.append(geom.exterior)

        elif geom.geom_type == "MultiPolygon":
            for part in geom:
                nuevas_geometrias.append(part.exterior)

        elif geom.geom_type == "Point":
            # ignoramos puntos
            continue

    if len(nuevas_geometrias) == 0:
        raise Exception("No se pudieron generar líneas válidas")

    gdf = gpd.GeoDataFrame(geometry=nuevas_geometrias, crs="EPSG:4326")

    # Simplificar (opcional)
    gdf["geometry"] = gdf["geometry"].simplify(0.000001)

    # Crear ID limpio
    gdf["id"] = range(1, len(gdf) + 1)
    gdf = gdf[["id", "geometry"]]

    gdf.to_file(output_path)