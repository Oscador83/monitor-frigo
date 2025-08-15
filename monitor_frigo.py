from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import csv
import sys

# --- CONFIGURACIÓN ---
URL_PRODUCTO = "https://www.boulanger.com/ref/1203636"
NOMBRE_ARCHIVO_CSV = "historial_precios.csv"

def obtener_precio_selenium():
    """Intenta obtener el precio usando un navegador Chrome real."""
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # --- ¡CAMBIO CLAVE! USAMOS UN USER-AGENT MÁS MODERNO Y CREÍBLE ---
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL_PRODUCTO)
        
        # Aceptar cookies (si aparecen)
        try:
            wait = WebDriverWait(driver, 10)
            accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accepter et fermer')]")))
            accept_button.click()
            print("Pop-up de consentimiento aceptado.")
        except Exception as e:
            print(f"No se encontró o no se pudo hacer clic en el pop-up de consentimiento: {e}")

        print("Esperando a que el precio sea visible en la página...")
        wait = WebDriverWait(driver, 10)
        
        elemento_precio = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "p.price__amount")))
            
        precio_texto = driver.execute_script("return arguments[0].textContent;", elemento_precio)
        print(f"Texto extraído: '{precio_texto}'")

        precio_limpio = precio_texto.replace('€', '').replace('\u202f', '').replace(' ', '').replace(',', '.').strip()
        precio_float = float(precio_limpio)
        return precio_float

    except Exception as e:
        print(f"Se ha producido un error durante la ejecución de Selenium: {e}")
        if driver:
            driver.save_screenshot('error_screenshot.png')
            print("Captura de pantalla del error guardada en 'error_screenshot.png'")
        return f"ERROR_SELENIUM"
    finally:
        if driver:
            driver.quit()

def guardar_en_csv(precio_str):
    """Guarda la fecha y el precio en el archivo CSV."""
    existe_archivo = os.path.isfile(NOMBRE_ARCHIVO_CSV)
    with open(NOMBRE_ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        if not existe_archivo:
            escritor.writerow(['Fecha', 'Precio'])
        fecha_hoy = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        escritor.writerow([fecha_hoy, precio_str])
    print(f"Datos '{precio_str}' guardados en {NOMBRE_ARCHIVO_CSV}")

# --- Flujo principal ---
if __name__ == "__main__":
    print(f"Iniciando monitor de precios para: {URL_PRODUCTO}")
    resultado = obtener_precio_selenium()
    
    guardar_en_csv(str(resultado))
    
    if not isinstance(resultado, float):
        print("El resultado no es un precio válido. Forzando fallo del workflow para revisión.")
        sys.exit(1)
        
    print(f"¡Proceso finalizado con ÉXITO! Precio encontrado: {resultado}")
