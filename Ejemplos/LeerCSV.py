import pandas as pd
import sys
from pathlib import Path


def instalar_dependencia(paquete):
    """Intenta instalar una dependencia faltante"""
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
        print(f"\n✅ {paquete} instalado correctamente")
        return True
    except Exception as e:
        print(f"\n❌ No se pudo instalar {paquete}: {e}")
        return False


def leer_csv(ruta_archivo):
    """Lee un archivo CSV con manejo de errores mejorado"""
    try:
        # Verificar extensión del archivo
        if not ruta_archivo.lower().endswith('.csv'):
            raise ValueError("El archivo debe ser de tipo CSV (.csv)")

        # Verificar si el archivo existe
        if not Path(ruta_archivo).exists():
            raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")

        # Leer el archivo con diferentes codificaciones comunes si es necesario
        codificaciones = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']

        for codificacion in codificaciones:
            try:
                df = pd.read_csv(ruta_archivo, encoding=codificacion)
                print(f"\n✅ Archivo leído exitosamente con codificación {codificacion}")
                return df
            except UnicodeDecodeError:
                continue

        # Si ninguna codificación funcionó
        raise UnicodeDecodeError("No se pudo determinar la codificación del archivo")

    except Exception as e:
        print(f"\n❌ Error al leer el archivo: {type(e).__name__} - {str(e)}")
        return None


def analizar_datos(df):
    """Realiza análisis básicos del DataFrame"""
    if df is not None:
        print("\n=== INFORMACIÓN DEL DATAFRAME ===")
        print(f"Total de filas: {len(df)}")
        print(f"Total de columnas: {len(df.columns)}")

        print("\n📊 Encabezados de columnas:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i:2d}. {col}")

        print("\n🔍 Primeras 5 filas:")
        print(df.head())

        print("\n🔎 Últimas 5 filas:")
        print(df.tail())

        print("\n🧮 Estadísticas descriptivas:")
        print(df.describe(include='all'))

        print("\n🔎 Valores faltantes por columna:")
        print(df.isnull().sum().to_string())

        return df.dropna(how='all')  # Devuelve DataFrame limpio
    return None


def menu_principal():
    """Interfaz de menú para el usuario"""
    print("\n" + "=" * 50)
    print("ANALIZADOR DE ARCHIVOS CSV".center(50))
    print("=" * 50)

    ruta = input("\nIngrese la ruta del archivo CSV (o Enter para default): ").strip()
    archivo_default = 'D:/DATOS/AD/datos/csv/MOCK_DATA.csv'

    ruta_archivo = ruta if ruta else archivo_default
    print(f"\nIntentando leer: {ruta_archivo}")

    datos = leer_csv(ruta_archivo)
    datos_limpios = analizar_datos(datos)

    if datos_limpios is not None:
        guardar = input("\n¿Desea guardar los datos limpios? (s/n): ").lower()
        if guardar == 's':
            nombre_salida = input("Nombre del archivo de salida (sin extensión): ")

            formato = input("\n¿Qué formato prefiere para guardar? (1-CSV, 2-Excel, 3-JSON): ")
            if formato == '1':
                datos_limpios.to_csv(f"{nombre_salida}.csv", index=False)
                print(f"\n💾 Archivo guardado como {nombre_salida}.csv")
            elif formato == '2':
                try:
                    datos_limpios.to_excel(f"{nombre_salida}.xlsx", index=False)
                    print(f"\n💾 Archivo guardado como {nombre_salida}.xlsx")
                except ImportError:
                    print("\n⚠️ Para exportar a Excel necesitas openpyxl")
                    if instalar_dependencia("openpyxl"):
                        datos_limpios.to_excel(f"{nombre_salida}.xlsx", index=False)
                        print(f"\n💾 Archivo guardado como {nombre_salida}.xlsx")
            elif formato == '3':
                datos_limpios.to_json(f"{nombre_salida}.json", orient='records')
                print(f"\n💾 Archivo guardado como {nombre_salida}.json")
            else:
                print("\n⚠️ Opción no válida, no se guardaron los datos")


if __name__ == "__main__":
    menu_principal()