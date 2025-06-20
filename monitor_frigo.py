from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime
import os
import csv
import smtplib # Herramienta para enviar emails
from email.message import EmailMessage # Herramienta para construir el email

# --- CONFIGURACIÓN ---
URL_PRODUCTO = "https://www.boulanger.com/ref/1203636"
NOMBRE_ARCHIVO_CSV = "historial_precios.csv"
# Obtenemos los secretos de GitHub
EMAIL_ADDRESS = os.getenv('MAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

def enviar_email(asunto, cuerpo):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Variables de email no configuradas en los Secrets. No se puede enviar correo.")
        return

    msg = EmailMessage()
    msg['Subject'] = asunto
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS # Nos lo enviamos a nosotros mismos
    msg.set_content(cuerpo)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email de reporte enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar el email: {e}")

def obtener_precio_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL_PRODUCTO)
        time.sleep(5)
        elemento_precio = driver.find_element(By.CSS_SELECTOR, "div.price__amount")
        if elemento_precio:
            precio_texto = elemento_precio.text.replace('€', '').replace(' ', '').replace(',', '.').strip()
            return float(precio_texto)
        return "ERROR_NO_ELEMENTO"
    except Exception as e:
        if driver:
            driver.save_screenshot('error_screenshot.png')
        return f"ERROR_SELENIUM: {e}"
    finally:
        if driver:
            driver.quit()

def guardar_en_csv(precio):
    existe_archivo = os.path.isfile(NOMBRE_ARCHIVO_CSV)
    with open(NOMBRE_ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not existe_archivo:
            writer.writerow(['Fecha', 'Precio'])
        writer.writerow([datetime.date.today().strftime('%Y-%m-%d'), precio])

# --- FLUJO PRINCIPAL ---
if __name__ == "__main__":
    print("Iniciando monitor de precios...")
    precio_actual = obtener_precio_selenium()
    guardar_en_csv(precio_actual)

    # Preparar el email
    asunto = f"Reporte de Precio: Frigorífico Boulanger"
    cuerpo = f"El resultado de hoy es: {precio_actual}\n\nURL del producto: {URL_PRODUCTO}"
    
    # Leer el precio de ayer para comparar
    try:
        with open(NOMBRE_ARCHIVO_CSV, 'r') as f:
            # Leemos las últimas dos líneas para tener el precio de hoy y el de ayer
            lineas = f.readlines()
            if len(lineas) > 2: # Necesitamos al menos el encabezado y dos precios
                precio_ayer_str = lineas[-2].split(',')[1].strip()
                precio_hoy_str = lineas[-1].split(',')[1].strip()
                
                if precio_hoy_str.replace('.', '', 1).isdigit() and precio_ayer_str.replace('.', '', 1).isdigit():
                    precio_hoy = float(precio_hoy_str)
                    precio_ayer = float(precio_ayer_str)
                    if precio_hoy < precio_ayer:
                        asunto = f"🎉 PRECIO HA BAJADO: {precio_hoy}€"
                        cuerpo = f"¡El precio ha bajado de {precio_ayer}€ a {precio_hoy}€!\n\nEnlace: {URL_PRODUCTO}"
                    elif precio_hoy > precio_ayer:
                         asunto = f"📈 PRECIO HA SUBIDO: {precio_hoy}€"
                    else:
                        asunto = f"Frigorífico: El precio sigue igual a {precio_hoy}€"
    except Exception as e:
        print(f"No se pudo comparar precios (probablemente es el primer día): {e}")

    enviar_email(asunto, cuerpo)
    print("Proceso finalizado.")
