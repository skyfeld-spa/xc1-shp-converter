import geopandas as gpd
from shapely.geometry import LineString, MultiLineString, Polygon, MultiPolygon

# 🔥 Función para eliminar Z y M (clave para Emlid)
def limpiar_geom(geom):
    try:
        if geom is None:
            return None

        # Si tiene coordenadas, eliminar Z/M
        if hasattr(geom, "coords"):
            coords_2d = [(x, y) for x, y, *rest in geom.coords]
            return type(geom)(coords_2d)

        return geom

    except:
        return None


def convertir(input_path, output_path):

    gdf = gpd.read_file(input_path)

    print("Geometrías detectadas:", gdf.geometry.type.unique())

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

        # 🔥 limpiar Z/M
        geom = limpiar_geom(geom)

        if geom is None:
            continue

        # 🔹 LINEA
        if geom.geom_type == "LineString":
            nuevas_geometrias.append(geom)

        # 🔹 MULTILINEA
        elif geom.geom_type == "MultiLineString":
            for part in geom.geoms:
                part = limpiar_geom(part)
                if part:
                    nuevas_geometrias.append(part)

        # 🔹 POLIGONO → borde
        elif geom.geom_type == "Polygon":
            nuevas_geometrias.append(limpiar_geom(geom.exterior))

        # 🔹 MULTIPOLIGONO
        elif geom.geom_type == "MultiPolygon":
            for part in geom.geoms:
                nuevas_geometrias.append(limpiar_geom(part.exterior))

        # 🔹 otros (Point, etc.) → ignorar
        else:
            continue

    if len(nuevas_geometrias) == 0:
        raise Exception("No se encontraron geometrías válidas")

    # Crear nuevo GeoDataFrame limpio
    gdf_out = gpd.GeoDataFrame(geometry=nuevas_geometrias, crs="EPSG:4326")

    # Simplificar ligeramente (mejor para XC-1)
    gdf_out["geometry"] = gdf_out["geometry"].simplify(0.000001)

    # ID limpio
    gdf_out["id"] = range(1, len(gdf_out) + 1)
    gdf_out = gdf_out[["id", "geometry"]]

    # Guardar shapefile final
    gdf_out.to_file(output_path)

    print("✔ Conversión completada:", output_path)