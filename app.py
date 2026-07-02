import streamlit as st
import zipfile
import io
import os

st.set_page_config(page_title="Renombrador de imágenes por ASIN", page_icon="🖼️")
st.title("🖼️ Generador de imágenes por ASIN")

st.markdown("""
Sube tu **listado de ASINs** y las **imágenes base** (MAIN.jpg, FRNT.jpg, etc.).
La app generará una copia renombrada por cada combinación: `ASIN.NOMBRE.jpg`.
""")

# --- 1. Entrada de ASINs ---
st.subheader("1) ASINs")
col1, col2 = st.columns(2)
with col1:
    asin_file = st.file_uploader("Fichero de ASINs (.txt / .csv)", type=["txt", "csv"])
with col2:
    asin_text = st.text_area("...o pégalos aquí (uno por línea)", height=150)

asins = []
if asin_file is not None:
    content = asin_file.read().decode("utf-8", errors="ignore")
    for line in content.replace(",", "\n").replace(";", "\n").splitlines():
        if line.strip():
            asins.append(line.strip())
if asin_text.strip():
    for line in asin_text.splitlines():
        if line.strip():
            asins.append(line.strip())

# elimina duplicados conservando el orden
asins = list(dict.fromkeys(asins))

# --- 2. Imágenes base ---
st.subheader("2) Imágenes base")
images = st.file_uploader(
    "Sube las imágenes (MAIN.jpg, FRNT.jpg, TOP.png...)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# --- 3. Vista previa y generación ---
if asins and images:
    total = len(asins) * len(images)
    st.info(f"Se generarán **{total}** archivos "
            f"({len(asins)} ASINs × {len(images)} imágenes).")

    ejemplo = images[0].name
    nombre_base, ext = os.path.splitext(ejemplo)
    st.caption(f"Ejemplo de salida: `{asins[0]}.{nombre_base}{ext}`")

    if st.button("🚀 Generar ZIP"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for img in images:
                img_bytes = img.getvalue()
                base, ext = os.path.splitext(img.name)
                for asin in asins:
                    nuevo_nombre = f"{asin}.{base}{ext}"
                    zf.writestr(nuevo_nombre, img_bytes)

        zip_buffer.seek(0)
        st.success("✅ ¡Listo!")
        st.download_button(
            label="⬇️ Descargar ZIP",
            data=zip_buffer,
            file_name="imagenes_asin.zip",
            mime="application/zip"
        )
else:
    st.warning("Sube al menos un ASIN y una imagen para continuar.")
