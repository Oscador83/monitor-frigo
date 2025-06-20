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
    """Intenta obtener el precio usando un navegador Chrome real, aceptando el pop-up correcto."""
    
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
        
        # --- PASO CLAVE: MANEJAR EL POP-UP MODAL ---
        try:
            print("Esperando el pop-up de 'Vos données, votre choix'...")
            wait = WebDriverWait(driver, 10)
            
            # Buscamos el botón por su texto, que es mucho más fiable en este caso
            accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accepter et fermer')]")))
            
            accept_button.click()
            print("Pop-up de consentimiento aceptado.")
            time.sleep(2) # Damos un respiro para que la página se cargue bien
        except Exception as e:
            print(f"No se encontró el pop-up de consentimiento (quizás no apareció esta vez): {e}")

        # --- BUSCAR EL PRECIO ---
        print("Buscando el precio final en la página...")
        elemento_precio = driver.find_element(By.CSS_SELECTOR, "div.price__amount")
        
        precio_texto = elemento_precio.text
        precio_limpio = precio_texto.replace('€', '').replace(' ', '').replace(',', '.').strip()
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
    print("Iniciando monitor de precios (vFinal y Definitiva)...")
    resultado = obtener_precio_selenium()
    
    guardar_en_csv(str(resultado))
    
    if not isinstance(resultado, float):
        print("El resultado no es un precio válido. Forzando fallo para revisión.")
        sys.exit(1)
        
    print("¡Proceso finalizado con ÉXITO!")
