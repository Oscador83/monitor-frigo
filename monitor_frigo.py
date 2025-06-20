from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import csv
import sys # <-- Importamos la herramienta para forzar el fallo

# --- CONFIGURACIÓN ---
URL_PRODUCTO = "https://www.boulanger.com/ref/1203636"
NOMBRE_ARCHIVO_CSV = "historial_precios.csv"

def obtener_precio_selenium():
    """Intenta obtener el precio, con un modo de diagnóstico mejorado."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL_PRODUCTO)
        try:
            wait = WebDriverWait(driver, 10)
            cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            cookie_button.click()
            print("Botón de cookies aceptado.")
            time.sleep(2)
        except Exception:
            print("No se encontró el botón de cookies. Continuando...")
        
        elemento_precio = driver.find_element(By.CSS_SELECTOR, "div.price__amount")
        precio_texto = elemento_precio.text
        precio_limpio = precio_texto.replace('€', '').replace(' ', '').replace(',', '.').strip()
        precio_float = float(precio_limpio)
        return precio_float
    except Exception as e:
        if driver:
            driver.save_screenshot('error_screenshot.png')
            print("Captura guardada por error.")
        return f"ERROR_SELENIUM: {str(e)}" # Devolvemos el error como string
    finally:
        if driver:
            driver.quit()

def guardar_en_csv(precio_str):
    existe_archivo = os.path.isfile(NOMBRE_ARCHIVO_CSV)
    with open(NOMBRE_ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        if not existe_archivo:
            escritor.writerow(['Fecha', 'Precio'])
        fecha_hoy = datetime.date.today().strftime('%Y-%m-%d')
        escritor.writerow([fecha_hoy, precio_str])
    print(f"Datos '{precio_str}' guardados en {NOMBRE_ARCHIVO_CSV}")

# --- Flujo principal del script ---
if __name__ == "__main__":
    print("Iniciando monitor de precios (vFinal-Diagnostico)...")
    resultado = obtener_precio_selenium()
    
    # Lo guardamos en el CSV para tener un registro de lo que ha pasado
    guardar_en_csv(str(resultado))
    
    # --- ¡CAMBIO IMPORTANTE! ---
    # Si el resultado no es un número, forzamos que la ejecución de GitHub falle
    if not isinstance(resultado, float):
        print("El resultado no es un precio válido. Forzando fallo para obtener la captura...")
        sys.exit(1)
        
    print("Proceso finalizado con éxito.")
