import geopandas as gpd

def convertir(input_path, output_path):

    gdf = gpd.read_file(input_path)

    print("Geometrías:", gdf.geometry.type.unique())

    if gdf.empty:
        raise Exception("Shapefile vacío")

    if gdf.crs is None:
        raise Exception("Sin sistema de coordenadas")

    # Convertir a WGS84
    gdf = gdf.to_crs(epsg=4326)

    nuevas_geometrias = []

    for geom in gdf.geometry:

        if geom is None:
            continue

        # 🔥 eliminar Z y M (CLAVE para Emlid)
        geom = geom.buffer(0)

        if geom.geom_type == "LineString":
            nuevas_geometrias.append(geom)

        elif geom.geom_type == "MultiLineString":
            for part in geom.geoms:
                nuevas_geometrias.append(part)

        elif geom.geom_type == "Polygon":
            nuevas_geometrias.append(geom.exterior)

        elif geom.geom_type == "MultiPolygon":
            for part in geom.geoms:
                nuevas_geometrias.append(part.exterior)

    if len(nuevas_geometrias) == 0:
        raise Exception("No se encontraron geometrías válidas")

    gdf = gpd.GeoDataFrame(geometry=nuevas_geometrias, crs="EPSG:4326")

    # Simplificar ligeramente
    gdf["geometry"] = gdf["geometry"].simplify(0.000001)

    # ID limpio
    gdf["id"] = range(1, len(gdf) + 1)
    gdf = gdf[["id", "geometry"]]

    gdf.to_file(output_path)