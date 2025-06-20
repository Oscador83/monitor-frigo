from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import csv

# --- CONFIGURACIÓN ---
URL_PRODUCTO = "https://www.boulanger.com/ref/1203636"
NOMBRE_ARCHIVO_CSV = "historial_precios.csv"

def obtener_precio_selenium():
    """Intenta obtener el precio usando un navegador Chrome real, aceptando primero las cookies."""
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080") # <-- LÍNEA CORREGIDA
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL_PRODUCTO)
        
        # --- NUEVO PASO: MANEJAR EL BANNER DE COOKIES ---
        try:
            # Esperamos un máximo de 10 segundos a que el botón de aceptar cookies sea clickeable
            wait = WebDriverWait(driver, 10)
            cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            cookie_button.click()
            print("Botón de cookies aceptado.")
            # Damos un pequeño respiro para que la página se reajuste tras cerrar el banner
            time.sleep(2)
        except Exception as e:
            # Si no encuentra el botón, no es un error fatal. Quizás no apareció.
            print(f"No se encontró o no se pudo hacer clic en el botón de cookies (quizás no apareció): {e}")

        # --- PASO ORIGINAL: BUSCAR EL PRECIO ---
        # Ahora que el banner está (probablemente) fuera del camino, buscamos el precio.
        elemento_precio = driver.find_element(By.CSS_SELECTOR, "div.price__amount")
        
        if elemento_precio:
            precio_texto = elemento_precio.text
            precio_limpio = precio_texto.replace('€', '').replace(' ', '').replace(',', '.').strip()
            precio_float = float(precio_limpio)
            print(f"Éxito (Método Cookies): Precio encontrado -> {precio_float}€")
            return precio_float
        else:
            print("Error: El elemento del precio no fue encontrado después de la espera.")
            return "ERROR_NO_ELEMENTO"

    except Exception as e:
        print(f"Ocurrió un error con Selenium: {e}")
        if driver:
            driver.save_screenshot('error_screenshot.png')
            print("Se ha guardado una captura de pantalla del error en 'error_screenshot.png'")
        return "ERROR_SELENIUM"
    finally:
        if driver:
            driver.quit()

def guardar_en_csv(precio):
    """Guarda la fecha y el precio en un archivo CSV."""
    existe_archivo = os.path.isfile(NOMBRE_ARCHIVO_CSV)
    
    with open(NOMBRE_ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        
        if not existe_archivo:
            escritor.writerow(['Fecha', 'Precio'])
        
        fecha_hoy = datetime.date.today().strftime('%Y-%m-%d')
        escritor.writerow([fecha_hoy, precio])
    
    print(f"Datos guardados en {NOMBRE_ARCHIVO_CSV}")

# --- Flujo principal del script ---
if __name__ == "__main__":
    print("Iniciando monitor de precios (vCookies-Corregido)...")
    precio = obtener_precio_selenium()
    
    if isinstance(precio, float):
        guardar_en_csv(precio)
    else:
        guardar_en_csv(str(precio))
        
    print("Proceso finalizado.")
