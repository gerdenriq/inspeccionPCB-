import pandas as pd
import re
import os

# ✅ Función robusta para intentar varias codificaciones
def leer_csv_codificacion_robusta(ruta_archivo, codificaciones=('utf-8', 'utf-16', 'latin1')):
    for cod in codificaciones:
        try:
            df = pd.read_csv(ruta_archivo, encoding=cod, sep=None, index_col=False)
            print(f"✅ Leído correctamente con codificación: {cod}")
            return df
        except UnicodeDecodeError:
            print(f"⚠️ Falló con codificación: {cod}")
    raise ValueError("❌ No se pudo leer el archivo con las codificaciones dadas.")

# ✅ Función corregida para buscar columnas según patrones
def buscar_columna(df, patrones_regex):
    for regex in patrones_regex:
        for columna in df.columns:
            if re.search(regex, columna, re.IGNORECASE):
                return columna
    return None

# Función principal
def procesar_pick_and_place():
    print("🔴 Iniciando ejecución del script...")

    ruta_csv = r"C:\Users\DOBROVOLSKI\Desktop\TrabajoTerminal\PickAndPlace_PCB1_2025-05-06.csv"
    print(f"🔍 Leyendo archivo: {ruta_csv}")

    try:
        df = leer_csv_codificacion_robusta(ruta_csv)
    except Exception as e:
        print(e)
        return

    print("🔎 Primeras filas del archivo para revisión:")
    print(df.head())
    print()

    mapeo_columnas = {
        'Referencia': [r'designator', r'refdes',r'ref'],
        'Valor': [r'val', r'value', r'comment'],
        'Paquete': [r'footprint', r'package'],
        'X': [r'mid[\s_]?x', r'pos[\s_]?x', r'center[\s_]?x', r'^x$', r'center-x'],
        'Y': [r'mid[\s_]?y', r'pos[\s_]?y', r'center[\s_]?y', r'^y$', r'center-y'],
        'Rotacion': [r'rot', r'angle'],
        'Capa': [r'layer', r'side']
    }

    columnas_encontradas = {}
    for clave, patrones in mapeo_columnas.items():
        col = buscar_columna(df, patrones)
        columnas_encontradas[clave] = col

    print("🔎 Columnas encontradas:")
    for k, v in columnas_encontradas.items():
        print(f"  {k}: {v}")
    print()

    necesarias = ['Referencia', 'Paquete', 'X', 'Y', 'Rotacion', 'Capa']
    if any(columnas_encontradas[n] is None for n in necesarias):
        print("❌ Faltan columnas necesarias. Abortando.")
        return

    df_filtrado = df[[columnas_encontradas[n] for n in necesarias]].copy()
    df_filtrado.columns = necesarias

    print(f"📦 Componentes totales: {len(df_filtrado)}")

    # Normalizar 'Capa' y filtrar top
    df_filtrado['Capa'] = df_filtrado['Capa'].astype(str).str.strip().str.upper()
    df_filtrado = df_filtrado[df_filtrado['Capa'].isin(['T', 'TOP', 'TOP LAYER'])]
    print(f"⬆️  En top layer: {len(df_filtrado)}")

    # Normalizar 'Referencia' y filtrar útiles
    df_filtrado['Referencia'] = df_filtrado['Referencia'].astype(str).str.strip().str.upper()
    print("🔎 Referencias normalizadas:")
    print(df_filtrado['Referencia'].head())  # Verificamos cómo quedaron las referencias
    df_filtrado = df_filtrado[df_filtrado['Referencia'].str.match(r'^[A-Za-z]+\d+', na=False)]
    print(f"🧩 Componentes útiles: {len(df_filtrado)}")

    encapsulados_permitidos = ['0805', '1008', '1206', '1210', '1812', '1825', '2010', '2012', '2512', '2520', '2920']

    def extraer_encapsulado(paquete):
        match = re.search(r'(\d{4})', paquete)
        if match:
            encapsulado = match.group(1).zfill(4)
            if encapsulado in encapsulados_permitidos:
                return encapsulado
        return None

    # Limpiar las unidades de las coordenadas (mm y °) antes de la conversión
    # Verificar si la columna es de tipo string antes de aplicar .str.replace()
    def limpiar_unidades(columna):
        if columna.dtype == 'object':  # Si la columna es de tipo string
            return columna.str.replace(r'[^\d.-]', '', regex=True)
        return columna  # Si no es una columna de strings, devolverla tal cual

    # Aplicar la limpieza a las columnas correspondientes
    df_filtrado['X'] = pd.to_numeric(limpiar_unidades(df_filtrado['X']), errors='coerce')
    df_filtrado['Y'] = pd.to_numeric(limpiar_unidades(df_filtrado['Y']), errors='coerce')
    df_filtrado['Rotacion'] = pd.to_numeric(limpiar_unidades(df_filtrado['Rotacion']), errors='coerce')

    # Verificar valores después de la limpieza
    print("🔎 Valores de X, Y y Rotación después de la limpieza:")
    print(df_filtrado[['X', 'Y', 'Rotacion']].head())

    # Filtrar los componentes con encapsulado válido
    df_filtrado['Encapsulado'] = df_filtrado['Paquete'].apply(extraer_encapsulado)
    print("🔎 Encapsulados extraídos:")
    print(df_filtrado['Encapsulado'].head())  # Verificar encapsulados extraídos
    df_filtrado = df_filtrado[df_filtrado['Encapsulado'].notna()]

    # Filtrar los componentes válidos, eliminando los NaN en X, Y y Rotacion
    df_filtrado = df_filtrado.dropna(subset=['X', 'Y', 'Rotacion']).reset_index(drop=True)

    print(f"📏 Componentes válidos finales: {len(df_filtrado)}\n")

    # Aquí es donde se define df_final correctamente
    df_final = df_filtrado[['Referencia', 'Encapsulado', 'X', 'Y', 'Rotacion', 'Capa', 'Paquete']]
    df_final = df_final.sort_values(by='Referencia').reset_index(drop=True)

    carpeta_destino = r"C:\Users\DOBROVOLSKI\Desktop\TrabajoTerminal"
    os.makedirs(carpeta_destino, exist_ok=True)

    nombre_base = os.path.splitext(os.path.basename(ruta_csv))[0]
    ruta_salida = os.path.join(carpeta_destino, f"{nombre_base}_limpio.csv")

    try:
        df_final.to_csv(ruta_salida, index=False)
        print(f"✅ Archivo limpio guardado en:\n{ruta_salida}")
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")

    return df_final

# Ejecución
if __name__ == "__main__":
    procesar_pick_and_place()
