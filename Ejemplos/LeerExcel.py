# importar las siguientes librerias
import sys
import pandas as pd


# el siguiende metodo es la instalacion de paquetes faltantes
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


# vamos a leer el excel
def leer_excel(ruta_archivo):
    """Lee un archivo Excel con manejo de errores mejorado"""
    try:
        # Verificar extensión del archivo
        if not ruta_archivo.lower().endswith(('.xls', '.xlsx')):
            raise ValueError("El archivo debe ser de tipo Excel (.xls o .xlsx)")

        # Leer el archivo
        df = pd.read_excel(ruta_archivo)
        print("\n✅ Archivo leído exitosamente")
        return df

    except ImportError as e:
        print("\n⚠️ Dependencia faltante detectada")
        if "openpyxl" in str(e):
            if instalar_dependencia("openpyxl"):
                return leer_excel(ruta_archivo)  # Reintentar después de instalar
        return None

    except Exception as e:
        print(f"\n❌ Error al leer el archivo: {type(e).__name__} - {str(e)}")
        return None


# vamos a analizar los datos
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

        print("\n🔎 Valores faltantes por columna:")
        print(df.isnull().sum().to_string())

        return df.dropna(how='all')  # Devuelve DataFrame limpio
    return None


def menu_principal():
    """Interfaz de menú para el usuario"""
    print("\n" + "=" * 50)
    print("ANALIZADOR DE ARCHIVOS EXCEL".center(50))
    print("=" * 50)

    # solicitamos la informacion de la ruta a la persona
    ruta = input("\nIngrese la ruta del archivo Excel (o Enter para default):\nFormato por defecto 'D:/ruta/de/tu/archivo.xlsx' ").strip()
    archivo_default = 'D:/gersan/AD/datos/excel/MOCK_DATA.xlsx'

    ruta_archivo = ruta if ruta else archivo_default
    print(f"\nIntentando leer: {ruta_archivo}")

    datos = leer_excel(ruta_archivo)
    datos_limpios = analizar_datos(datos)

    if datos_limpios is not None:
        guardar = input("\n¿Desea guardar los datos limpios? (s/n): ").lower()
        if guardar == 's':
            nombre_salida = input("Nombre del archivo de salida (sin extensión): ")
            datos_limpios.to_excel(f"{nombre_salida}.xlsx", index=False)
            print(f"\n💾 Archivo guardado como {nombre_salida}.xlsx")


if __name__ == "__main__":
    menu_principal()