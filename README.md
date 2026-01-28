# Estimación de Pobreza en México usando CNN e Imágenes Satelitales 

Este repositorio contiene el código fuente para la tesis: **"Estimación de Pobreza Multidimensional a nivel AGEB mediante Redes Neuronales Convolucionales"**. Códigos adaptados de Marivel Zea Ortiz y Pablo Vera Alfaro, del laboratorio de ciencia de datos del INEGI.
Disponible en: https://git.inegi.org.mx/laboratorio-de-ciencia-de-datos/vulnerability/-/tree/main?ref_type=heads
El flujo de trabajo procesa imágenes satelitales (VRT) para entrenar modelos de Deep Learning y generar predicciones a nivel municipal y estatal.

## 📂 Estructura del Proyecto

El código está organizado en tres módulos secuenciales:

* 📁 **`utils_recortes/`**: Scripts para preprocesamiento, generación de *patches* (recortes) y unión de bandas.
* 📁 **`entrenamiento/`**: Modelos CNN (VGG16, ResNet, EfficientNet, etc.) para entrenamiento y generación de predicciones crudas.
* 📁 **`predicciones/`**: Procesamiento final para agregar resultados a nivel Municipal y Estatal.

---

Sigue estos pasos para reproducir los experimentos:

### 1. Preprocesamiento (`utils_recortes`)
**Requisito previo:** Debes contar con los archivos `.vrt` (Virtual Raster) de la Geomediana (imágenes diurnas) y de NTL (Luminosidad Nocturna).

1.  Utiliza los scripts generadores de recortes ubicados en esta carpeta para convertir los VRT en arreglos numéricos (arrays) que la red pueda leer.
2.  **Importante:** Para generar el input final de 7 canales (Bandas multiespectrales + Luminosidad), ejecuta el script:
    * `unir_recortes_7B.py`

### 2. Entrenamiento y Predicción (`entrenamiento`)
Una vez generados los arreglos (`.npy` o `.h5`):

1.  Navega a esta carpeta y selecciona el script correspondiente dependiendo del tipo de recorte o arquitectura que desees probar (ej. `EfficientNetB3`, `VGG16`).
2.  Ejecuta el script de entrenamiento.
3.  **Output:** Al finalizar, el modelo generará archivos **Excel (`.xlsx`)** con las predicciones crudas a nivel de AGEB/Patch.

### 3. Agregación de Resultados (`predicciones`)
Para obtener las métricas finales interpretables:

1.  Toma los archivos Excel generados en el paso anterior.
2.  Ejecuta los scripts de esta carpeta (ej. `predicciones_municipales.py` o `estatales.py`).
3.  Estos códigos aplicarán los promedios ponderados poblacionales para devolver la estimación final de pobreza por **Municipio** y **Estado**.

---
*Autor: Allan Ramírez González*
