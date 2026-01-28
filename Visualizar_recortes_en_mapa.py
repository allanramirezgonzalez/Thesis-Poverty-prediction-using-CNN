import geopandas as gpd
import rasterio
from rasterio.windows import Window
import matplotlib.pyplot as plt
from shapely.geometry import box
import pandas as pd


# Leer el archivo shapefile del mapa de México (descargar el shapefile de la República Mexicana si no lo tienes)
mexico_shp = gpd.read_file("d:/Geomediana/AGEB shp 2020/Albers_AGEB.shp") #archivo shp en ALBERS

# Cargar las coordenadas de los recortes desde el CSV
df = pd.read_excel("c:/Users/dvcha/Documents/Centroides_EDOMEX.xlsx") 


# Dimensiones del recorte (en píxeles)
width = 40
height = 40

# Crear una lista para almacenar las geometrías de los recortes (rectángulos)
rectangles = []

# Procesar cada raster (asume que solo hay un archivo raster)
raster_path = ("d:/Geomediana/Geomediana2020/144_mosaicos.vrt") #vrt de la Geomediana
with rasterio.open(raster_path) as src:
    for idx, row in df.iterrows():
        py, px = src.index(row['LON_CENT_alb'], row['LAT_CENT_alb'])
        
        col_off = px - width // 2
        row_off = py - height // 2
        
        if col_off < 0 or row_off < 0 or (col_off + width) > src.width or (row_off + height) > src.height:
            continue  # Omitir si está fuera del raster
        
        # Crear el rectángulo con las coordenadas
        minx, miny = src.xy(row_off + height, col_off)
        maxx, maxy = src.xy(row_off, col_off + width)
        rec = box(minx, miny, maxx, maxy)  # Crear un rectángulo con las coordenadas
        rectangles.append(rec)

# Crear un GeoDataFrame con las geometrías de los recortes
gdf_recortes = gpd.GeoDataFrame(geometry=rectangles, crs=src.crs)

#### Visualización: Mapa base con los recortes
fig, ax = plt.subplots(figsize=(10, 10))
mexico_shp.plot(ax=ax, color='lightblue', edgecolor='black')  # Mapa de México
gdf_recortes.plot(ax=ax, facecolor='none', edgecolor='red')  # Dibujar los recortes en rojo
plt.title('Recortes de 40x40 píxeles sobre el mapa de México')
plt.show()


