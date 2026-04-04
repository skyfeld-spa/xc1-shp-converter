import geopandas as gpd

def convertir(input_path, output_path):
    gdf = gpd.read_file(input_path)

    if gdf.empty:
        raise Exception("Shapefile vacío")

    if gdf.crs is None:
        raise Exception("Sin sistema de coordenadas")

    gdf = gdf.to_crs(epsg=4326)
    gdf = gdf.explode(index_parts=False)
    gdf = gdf[gdf.geometry.type == "LineString"]

    if gdf.empty:
        raise Exception("No hay líneas válidas")

    gdf["geometry"] = gdf["geometry"].simplify(0.000001)

    gdf["id"] = range(1, len(gdf) + 1)
    gdf = gdf[["id", "geometry"]]

    gdf.to_file(output_path)
