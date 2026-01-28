### Del excel que arroja generar promedios municipales ponderados, se hacen promedios ponderados a nivel estatal
import pandas as pd


###Tu excel debe de tener la columna POB mun 2020 censo, sino no va a funcionar. Cambiale el nombre a la columna de ponderado si es necesario.
#Tambien debes de agregar la columna "entidad" y "porcentaje 2020" a tu base de datos de excel, igual copiala y pegala
#Fijate que no tenga NA´s tu base al momento de correr este código.


# 1. Cargar tu archivo (ajusta la ruta a tu archivo real)
df = pd.read_excel("C:/Modelos_CIMAT/Logmediana 2020 EFNB7 si funciona/promedios_ponderados_por_municipio_logmed_2020_EFNB7.xlsx")

# --- PROMEDIO PONDERADO PARA "Ponderado" ---
# 2. Calcular Score1 para Ponderado
df["Score1_Ponderado"] = df["Ponderado"] * df["POB mun 2020 Censo"]

# 3. Agrupar por entidad y sumar Score1_Ponderado y población
agrupado_ponderado = (
    df.groupby("Entidad", as_index=False)
      .agg({"Score1_Ponderado": "sum", "POB mun 2020 Censo": "sum"})
)

# 4. Calcular promedio ponderado de la columna "Ponderado"
agrupado_ponderado["Promedio_Ponderado"] = (
    agrupado_ponderado["Score1_Ponderado"] / agrupado_ponderado["POB mun 2020 Censo"]
)

# --- PROMEDIO PONDERADO PARA "Porcentaje 2020" ---
# 5. Calcular Score1 para Porcentaje 2020
df["Score1_Porc2020"] = df["Porcentaje 2020"] * df["POB mun 2020 Censo"]

# 6. Agrupar por entidad y sumar Score1_Porc2020 y población
agrupado_porc = (
    df.groupby("Entidad", as_index=False)
      .agg({"Score1_Porc2020": "sum", "POB mun 2020 Censo": "sum"})
)

# 7. Calcular promedio ponderado de Porcentaje 2020
agrupado_porc["Promedio_Porc2020"] = (
    agrupado_porc["Score1_Porc2020"] / agrupado_porc["POB mun 2020 Censo"]
)

# --- UNIR RESULTADOS ---
# 8. Unir ambos resultados por Entidad
resultado = pd.merge(
    agrupado_ponderado[["Entidad", "Promedio_Ponderado"]],
    agrupado_porc[["Entidad", "Promedio_Porc2020"]],
    on="Entidad",
    how="inner"
)

# --- CALCULAR TOTAL NACIONAL ---
# 9. Sumar totales nacionales
total_pob = df["POB mun 2020 Censo"].sum()
total_ponderado = (df["Ponderado"] * df["POB mun 2020 Censo"]).sum() / total_pob
total_porc2020 = (df["Porcentaje 2020"] * df["POB mun 2020 Censo"]).sum() / total_pob

# 10. Crear fila "Total Nacional"
fila_total = pd.DataFrame({
    "Entidad": ["Total Nacional"],
    "Promedio_Ponderado": [total_ponderado],
    "Promedio_Porc2020": [total_porc2020]
})

# 11. Añadir al resultado final
resultado_final = pd.concat([resultado, fila_total], ignore_index=True)

# 12. Exportar resultado a Excel
resultado_final.to_excel("promedios_ponderados_por_entidad_y_nacional.xlsx", index=False) #Esta linea cambias el nombre del archivo. 

# Mostrar resultado

print(resultado_final)
