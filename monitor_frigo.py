# Nombre del workflow que```yaml
# Nombre del workflow que aparecerá en la pestaña "Actions"
name: Monitor de Precios

# Dis aparecerá en la pestaña "Actions"
name: Monitor de Precios

# Disparadores: Cuándo debeparadores: Cuándo se debe ejecutar este workflow
on:
  # Permite que lo ejecutes manualmente desde ejecutarse este workflow
on:
  # Permite que lo ejecutes manualmente desde la pestaña "Actions"
  workflow la pestaña "Actions"
  workflow_dispatch:
  
  # Opcional: Ejecutar cada vez_dispatch:
  
  # Opcional: Descomenta la línea de abajo si quieres que se ejecute cada que haces un commit a la rama principal
  # push:
  #   branches:
  #     - día a las 8 AM
  # schedule:
  #   - cron: '0 8 * * *' main
      
  # Opcional: Ejecutar a una hora programada (ej. todos los días a las 8 AM UTC)
  # schedule:
  #   - cron: '0 8 * * *'



# Definición de las tareas a realizar
jobs:
  build:
    # La máquina virtual que usjobs:
  # Nombre del trabajo a realizar
  build:
    # Usar la última versión de Ubuntuaremos (una Ubuntu limpia y actualizada)
    runs-on: ubuntu-latest

    # La secuencia de pasos que como máquina virtual
    runs-on: ubuntu-latest

    # Secuencia de pasos a ejecutar
    steps ejecutará la máquina
    steps:
      # 1. Descarga tu código en la máquina virtual
      - name:
      # 1. Descargar tu código del repositorio a la máquina virtual
      - name: Checkout del código: Checkout del código
        uses: actions/checkout@v4

      # 2. Instala el entorno de Python

        uses: actions/checkout@v3

      # 2. Configurar el entorno de Python
      - name:      - name: Configurar Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      # 3. Instala Configurar Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      # 3. Instalar las librerías de las librerías de Python (Selenium en este caso)
      - name: Instalar dependencias de Python
 Python necesarias
      - name: Instalar dependencias de Python
        run: |
          python -m pip install --        run: |
          python -m pip install --upgrade pip
          pip install selenium

      # 4. (upgrade pip
          pip install selenium

      # --- ¡AQUÍ ESTÁ LA MAGIA! INSTALACIÓN DELPASO NUEVO) Instala el navegador Google Chrome
      - name: Instalar Google Chrome
        run: |
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable

      #  NAVEGADOR Y DRIVER ---
      
      # 4. Instalar el navegador Google Chrome en la máquina virtual
5. (PASO NUEVO) Instala el ChromeDriver compatible con el Chrome instalado
      - name: Instalar ChromeDriver
        uses: nanasess/setup-chromedriver@v2

      # 6. Ejecuta tu script de Python
      - name: Instalar Google Chrome
        run: |
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable
      
      # 5. Instalar el ChromeDriver correspondiente a la versión de Chrome
      - name: Instalar ChromeDriver
        uses: nanasess/setup-chromedriver@v2

      # --- FIN      - name: Ejecutar el script de monitoreo
        # --- ¡¡¡ATENCIÓN!!! ---
        # Asegúrate de que el nombre del archivo aquí es el correcto.
        # Si tu script se llama "main.py", pon DE LA INSTALACIÓN ---

      # 6. Ejecutar tu script de Python
      - name: Ejecutar el "python main.py".
        run: python monitor_frigo.py 

      # 7. S script de monitoreo
        run: python monitor_frigo.py # <-- ¡¡¡IMPORTANTE!!! Reemplaza 'ube el archivo CSV como un "artefacto" para que puedas descargarlo
      - name: Guardar el historialmonitor_frigo.py' con el nombre real de tu archivo Python.

      # 7. Si el script tiene éxito, guardar el archivo CSV como un "artefacto"
      - name: Guardar el historial de precios
 de precios (si tuvo éxito)
        uses: actions/upload-artifact@v4
        with:
          name: historial-precios
          path: historial_precios.csv

      # 8. Si el paso 6 fall        if: success()
        uses: actions/upload-artifact@v3
        with:
          name: historial-precios
          path: historial_precios.csv

      # 8. Si el script falla,ó, sube la captura de pantalla del error
      - name: Guardar captura en caso de error
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: guardar la captura de pantalla como un "artefacto"
      - name: Guardar captura en caso de error
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name error-screenshot
          path: error_screenshot.png
