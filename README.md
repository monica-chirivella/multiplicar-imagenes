# 🖼️ Renombrador de imágenes por ASIN

Aplicación web en Streamlit que genera copias renombradas de imágenes de producto
para cada ASIN proporcionado, siguiendo el formato `ASIN.NOMBRE.jpg`.

## Uso
1. Sube un listado de ASINs (.txt / .csv) o pégalos en el cuadro de texto.
2. Sube una o varias imágenes base (MAIN.jpg, FRNT.jpg, etc.).
3. Pulsa "Generar ZIP" y descarga el resultado.

## Ejecución local
```bash
pip install -r requirements.txt
streamlit run app.py
