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
    """Intenta obtener el precio usando un navegador Chrome real y JavaScript para extraer el texto."""
    
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
            accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accepter et fermer')]")))
            accept_button.click()
            print("Pop-up de consentimiento aceptado.")
        except Exception as e:
            print(f"No se encontró el pop-up de consentimiento (quizás no apareció esta vez): {e}")

        print("Esperando a que el precio sea visible en la página...")
        wait = WebDriverWait(driver, 10)
        
        elemento_precio = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test-id='product-price']")))
            
        
        
        # --- ¡CAMBIO CLAVE! USAMOS JAVASCRIPT PARA EXTRAER EL TEXTO ---
        precio_texto = driver.execute_script("return arguments[0].textContent;", elemento_precio)
        
        print(f"Texto extraído con JS: '{precio_texto}'")

        precio_limpio = precio_texto.replace('€', '').replace('\u202f', '').replace(' ', '').replace(',', '.').strip()
        precio_float = float(precio_limpio)
        return precio_float

    except Exception as e:
        if driver:
            driver.save_screenshot('error_screenshot.png')
        return f"ERROR_SELENIUM: {str(e)}"
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

# --- Flujo principal ---
if __name__ == "__main__":
    print("Iniciando monitor de precios (vJavaScript-Extractor)...")
    resultado = obtener_precio_selenium()
    
    guardar_en_csv(str(resultado))
    
    if not isinstance(resultado, float):
        print("El resultado no es un precio válido. Forzando fallo para revisión.")
        sys.exit(1)
        
    print("¡Proceso finalizado con ÉXITO!")
