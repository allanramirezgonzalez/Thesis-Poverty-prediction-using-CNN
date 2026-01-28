import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize_scalar

def find_optimal_k_for_skewness(Y, method='brent', bounds=None):
    """
    Encuentra el valor óptimo de K para minimizar la asimetría de log(Y + K).
    
    Parámetros:
    -----------
    Y : array-like
        Variable dependiente que contiene ceros y valores positivos
    method : str, opcional
        Método de optimización ('brent' o 'bounded')
    bounds : tuple, opcional
        Límites para el método 'bounded' (ej. (1e-10, 1))
        
    Retorna:
    --------
    float
        Valor óptimo de K que minimiza la asimetría
    """
    Y = np.array(Y)
    Y_positive = Y[Y > 0]

    def objective(k):
        y_transformed = np.log(Y + k)
        skew = stats.skew(y_transformed)
        return np.abs(skew)
    
    if method == 'brent':
        result = minimize_scalar(objective, method='brent', options={'xtol': 1e-10})
    elif method == 'bounded':
        if bounds is None:
            min_k = 1e-10
            max_k = np.percentile(Y_positive, 95) if len(Y_positive) > 0 else 1
            bounds = (min_k, max_k)
        result = minimize_scalar(objective, method='bounded', bounds=bounds)
    else:
        raise ValueError("Método no soportado. Use 'brent' o 'bounded'.")
    
    return result.x

# Cargar Excel y ejecutar
def main():
    ruta_excel = "c:/Users/zonad/Documents/stats_ntl2023.xlsx"  # <-- CAMBIA esto por la ruta a tu archivo
    nombre_columna = "Mediana_2023_NO_NA"  # <-- CAMBIA esto por el nombre real de la columna

    # Leer el archivo
    df = pd.read_excel(ruta_excel)

    # Verificar que la columna existe
    if nombre_columna not in df.columns:
        raise ValueError(f"La columna '{nombre_columna}' no se encuentra en el archivo.")
    
    # Extraer datos y eliminar NaN
    Y = df[nombre_columna].dropna()

    # Asegurar que los valores sean numéricos
    Y = pd.to_numeric(Y, errors='coerce').dropna()

    # Calcular K óptimo
    k_optimo = find_optimal_k_for_skewness(Y, method='bounded')

    print(f"El valor óptimo de K para la columna '{nombre_columna}' es: {k_optimo:.6f}")

if __name__ == "__main__":
    main()
