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
    """Intenta obtener el precio, con un modo de diagnóstico mejorado."""
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = None
    try:
        print("Iniciando navegador...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"Navegando a: {URL_PRODUCTO}")
        driver.get(URL_PRODUCTO)
        print(f"Título de la página cargada: {driver.title}")

        # --- MANEJAR EL BANNER DE COOKIES ---
        try:
            print("Esperando el botón de cookies...")
            wait = WebDriverWait(driver, 10)
            cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            cookie_button.click()
            print("Botón de cookies aceptado.")
            time.sleep(2)
        except Exception:
            print("No se encontró el botón de cookies (o no se pudo hacer clic). Continuando...")

        # --- BUSCAR EL PRECIO ---
        print("Buscando el elemento del precio...")
        elemento_precio = driver.find_element(By.CSS_SELECTOR, "div.price__amount")
        
        if elemento_precio:
            precio_texto = elemento_precio.text
            precio_limpio = precio_texto.replace('€', '').replace(' ', '').replace(',', '.').strip()
            precio_float = float(precio_limpio)
            print(f"Éxito: Precio encontrado -> {precio_float}€")
            return precio_float
        else:
            # Este caso es muy improbable, pero lo dejamos por si acaso
            raise Exception("El elemento del precio se encontró pero estaba vacío.")

    except Exception as e:
        print("--- OCURRIÓ UN ERROR ---")
        if driver:
            print("Guardando captura de pantalla del error...")
            driver.save_screenshot('error_screenshot.png')
            print("Captura guardada.")
        # Devolvemos el mensaje de error específico para el log
        return f"ERROR_SELENIUM: {str(e)}"
    finally:
        if driver:
            driver.quit()
            print("Navegador cerrado.")

def guardar_en_csv(precio):
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
    print("Iniciando monitor de precios (vDiagnostico)...")
    precio = obtener_precio_selenium()
    guardar_en_csv(precio)
    print("Proceso finalizado.")
