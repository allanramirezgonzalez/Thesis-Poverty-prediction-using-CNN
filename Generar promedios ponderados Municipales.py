import pandas as pd #Sí funciona v:

###Codigos para 2020
#Asegurate de que la base de predicciones completas tenga la columna de población por AGEB, la puedes copiar y pegar de otra base, da lo mismo.

# 1. Cargar datos (ajusta la ruta a tu archivo)
df = pd.read_excel("C:/Modelos_CIMAT/CARPETA PROVISIONAL/Guarda los excels aca/preds2015SC.xlsx")

# 2. Crear la columna "yponderado" = y_pred * Pob
df["yponderado"] = df["y_pred"] * df["Pob"]

# 3. Agrupar por entidad y municipio para sumar yponderado y Pob
agrupado = (
        df.groupby(["CVE_ENT", "CVE_MUN"], as_index=False)
        .agg({"yponderado": "sum", "Pob": "sum"})
)

# 4. Calcular el promedio ponderado de cada municipio
agrupado["y_prom_ponderado"] = agrupado["yponderado"] / agrupado["Pob"]

# 5. Crear un identificador de municipio (entidad + municipio, opcional)
agrupado["id_mun"] = agrupado["CVE_ENT"].astype(str).str.zfill(2) + agrupado["CVE_MUN"].astype(str).str.zfill(3)

# 6. Seleccionar columnas finales (puedes cambiar el orden si lo prefieres)
resultado = agrupado[["id_mun", "y_prom_ponderado"]]

# 7. (Opcional) Guardar en Excel o CSV
resultado.to_excel("promedios_ponderados_por_municipio.xlsx", index=False) #Esta linea cambias el nombre del archivo. Se guardan en disco D DVCHANES documentos

print("Cálculo terminado")
