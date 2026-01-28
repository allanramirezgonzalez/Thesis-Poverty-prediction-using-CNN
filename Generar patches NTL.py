###Este codigo es para generar los patches de el raster de luz nocturna. Para esto, el raster ya debio de haber sido reescalado al mismo tamaño que el de la Geoqmediana

#%%
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from rasterio.windows import Window


#%%
# # Rutas de los archivos raster
raster_paths = ["d:/Geomediana/Geomediana 2023/NTL2023_30p.vrt"] 

df = pd.read_excel("c:/Users/dvcha/OneDrive/Desktop/Bases AGEB/Todos_los_centroides_AGEB_MG2020.xlsx") #c:/Users/dvcha/OneDrive/Desktop/Bases AGEB/Base_Albers_Final_81k.xlsx ES LA DE 2020 LA BUENA FINAL

# # Ancho y altura de la ventana de recorte en píxeles
width = 40
height = 40

# # Lista para almacenar los recortes de todas las imágenes
all_cropped_images = []

# # Lista para almacenar la información de las imágenes que no tienen la forma deseada
invalid_images_set = set()

# # Diccionario para contar las ventanas válidas por cada raster
valid_windows_count = {raster_path: 0 for raster_path in raster_paths}

# # Lista para almacenar los índices de las imágenes válidas
valid_indices = set()

# # Procesar cada raster
for raster_path in raster_paths:
    with rasterio.open(raster_path) as src:
        for idx, row in df.iterrows():
            py, px = src.index(row['LON_CENT_alb'], row['LAT_CENT_alb'])
            
            col_off = px - width // 2
            row_off = py - height // 2
            
            if col_off < 0 or row_off < 0 or (col_off + width) > src.width or (row_off + height) > src.height:
                invalid_images_set.add((
                    row['CVEGEO'],
                    row['LAT_CENT_alb'],
                    row['LON_CENT_alb']
                ))
                continue
                
            window = Window(col_off, row_off, width, height)
            
            cropped_data = src.read(window=window)
            
            if cropped_data.shape == (1, 40, 40):
                valid_windows_count[raster_path] += 1
                valid_indices.add(idx)
                all_cropped_images.append(cropped_data)


#%%
# # Convertir la lista de imágenes recortadas a un array de NumPy
all_cropped_images_array = np.array(all_cropped_images)

# # Guardar el array en un archivo .npy
np.save('NTL_NN_2023_recortes_Albers_Base_Recortada_finaL_81k.npy', all_cropped_images_array)

print("Recortes de imágenes guardados en 'all_cropped_images.npy'.")


# %%


