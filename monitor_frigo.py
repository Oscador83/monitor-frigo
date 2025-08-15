# Nombre del workflow que aparecerá en la pestaña "Actions"
name: Monitor de Precios

# Disparadores: Cuándo se debe ejecutar este workflow
on:
  # Permite que lo ejecutes manualmente desde la pestaña "Actions"
  workflow_dispatch:

  # Opcional: Ejecutar a una hora programada (ej. todos los días a las 8 AM UTC)
  # Para activarlo, quita el '#' de las dos líneas siguientes.
  # schedule:
  #   - cron: '0 8 * * *'

# Definición de las tareas a realizar
jobs:
  build:
    # Usar la última versión de Ubuntu como máquina virtual
    runs-on: ubuntu-latest

    # Secuencia de pasos a ejecutar
    steps:
      # 1. Descargar tu código del repositorio a la máquina virtual
      - name: Checkout del código
        uses: actions/checkout@v4

      # 2. Configurar el entorno de Python 3.10
      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      # 3. Instalar las librerías de Python necesarias (Selenium)
      - name: Instalar dependencias de Python
        run: |
          python -m pip install --upgrade pip
          pip install selenium

      # 4. Instalar el navegador Google Chrome en la máquina virtual
      - name: Instalar Google Chrome
        run: |
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable
      
      # 5. Instalar el ChromeDriver correspondiente
      - name: Instalar ChromeDriver
        uses: nanasess/setup-chromedriver@v2

      # 6. Ejecutar tu script de Python
      - name: Ejecutar el script de monitoreo
        run: python monitor_frigo.py

      # 7. Si el script tiene éxito, guardar el archivo CSV como un "artefacto"
      - name: Guardar el historial de precios (si tuvo éxito)
        if: success()
        uses: actions/upload-artifact@v4
        with:
          name: historial-precios
          path: historial_precios.csv
          retention-days: 30 # Guardar el historial por 30 días

      # 8. Si el script falla, guardar la captura de pantalla como un "artefacto"
      - name: Guardar captura en caso de error
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: error-screenshot
          path: error_screenshot.png
          retention-days: 5 # Guardar la captura solo por 5 días
