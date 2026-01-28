###Este código fue usado en la Supercomputadora del CIMAT

#PREDICCIONES 2015

import os
import numpy as np
import pandas as pd
import cv2
import time
import tensorflow as tf
from tensorflow.keras import models

# ----------------------------
# CONFIGURACIÓN (¡IMPORTANTE: AJUSTA ESTAS RUTAS!)
# ----------------------------
# --- Rutas de Archivos de Entrada ---
# Asegúrate de que esta ruta apunte al modelo que quieres usar para predecir
MODEL_PATH = "/home/proy_sc25_dvchanes/model_EfficientNetB7_7B.h5" #Aqui tienes que cambiar los pesos del modelo entrenado, dependiendo si probamos con logmediana o sensor completo (primer modelo)
X_NPY_PATH = "/home/proy_sc25_dvchanes/data/7bandas_2015_NN.npy" #Estas son las imagenes satelitales de 2015
EXCEL_PATH = "/home/proy_sc25_dvchanes/data/Base_AGEB_Albers_pobreza_2015.xlsx" #Esta es la base CONEVAL 2015

# --- Ruta de Salida ---
OUTPUT_DIR = "/home/proy_sc25_dvchanes/output_predictions"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Parámetros del Modelo ---
BATCH_SIZE = 32 # Puedes usar un batch size más grande para predicción
HEIGHT, WIDTH = 224, 224 # Asegúrate que coincida con el tamaño de entrada de tu modelo
CHANNELS = 7

# ----------------------------
# ESTRATEGIA MULTI-GPU
# ----------------------------
strategy = tf.distribute.MirroredStrategy()
print(f'Número de dispositivos GPU para predicción: {strategy.num_replicas_in_sync}')
GLOBAL_BATCH_SIZE = BATCH_SIZE * strategy.num_replicas_in_sync

# ----------------------------
# CARGA DE MODELO Y DATOS
# ----------------------------
print("Cargando el modelo entrenado...")
with strategy.scope():
    model = models.load_model(MODEL_PATH)
print("Modelo cargado exitosamente.")
model.summary()

print("Cargando datos de imágenes y metadatos...")
x_imgs = np.load(X_NPY_PATH, mmap_mode='r')
df_base = pd.read_excel(EXCEL_PATH, usecols=["CVEGEO", "CVE_ENT", "CVE_MUN", "CVE_LOC", "CVE_AGEB", "Coneval_2015"])
y_true_all = df_base["Coneval_2015"].values
n_total = len(x_imgs)
print(f"Se procesarán {n_total} imágenes en total.")

# ----------------------------
# PIPELINE DE DATOS PARA PREDICCIÓN
# ----------------------------
# Función para preprocesar las imágenes al vuelo
def preprocess_for_prediction(index):
    img = x_imgs[index]
    # Transponer de (C, H, W) a (H, W, C)
    img = np.transpose(img, (1, 2, 0)).astype(np.float32)
    # Escalar
    img[img < 0.0] = 0.0
    img *= (1.0 / 10000.0)
    # Redimensionar
    img_resized = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)
    return img_resized

def tf_preprocess_wrapper(index):
    # Usamos tf.numpy_function para poder usar NumPy/OpenCV dentro del pipeline de TF
    [img] = tf.numpy_function(preprocess_for_prediction, [index], [tf.float32])
    img.set_shape([HEIGHT, WIDTH, CHANNELS])
    return img

# Crear el dataset de TensorFlow a partir de los índices de las imágenes
indices_ds = tf.data.Dataset.from_tensor_slices(np.arange(n_total))
prediction_ds = indices_ds.map(tf_preprocess_wrapper, num_parallel_calls=tf.data.AUTOTUNE)
prediction_ds = prediction_ds.batch(GLOBAL_BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

# ----------------------------
# PREDICCIÓN Y EVALUACIÓN
# ----------------------------
print("Iniciando predicción en todo el dataset...")
start_time = time.time()
y_pred_all = model.predict(prediction_ds, verbose=1)
y_pred_all = y_pred_all.ravel() # Aplanar el resultado
print(f"Predicción completada en {time.time() - start_time:.2f} segundos.")

# Agregar predicciones al DataFrame
df_base["y_pred"] = y_pred_all

# Evaluación sobre la base completa
print("Calculando métricas de evaluación en la base completa...")
mse = np.mean((y_pred_all - y_true_all)**2)
sigma2 = np.var(y_true_all)
r2 = 1.0 - mse / sigma2

print("\n--- Resultados en Base Completa ---")
print(f"  R^2  = {r2:.4f}")
print(f"  MSE  = {mse:.4f}")
print("-----------------------------------\n")

# ----------------------------
# GUARDADO DE RESULTADOS
# ----------------------------
output_csv_path = os.path.join(OUTPUT_DIR, "predicciones_completas_con_ids.csv")
df_base.to_csv(output_csv_path, index=False)
print(f"Resultados guardados exitosamente en: {output_csv_path}")

print("FIN.")