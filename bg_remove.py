import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance
from io import BytesIO

# Configuration de la page Streamlit
st.set_page_config(layout="wide", page_title="Retirer l'Arrière Plan")

# Titre principal
st.write("## Retirer l'arrière-plan de l'image")
st.write(":dog: Importez une image pour retirer son arrière-plan. :grin:")

# Section latérale
st.sidebar.write("## Importer et télécharger l'image :gear:")

# Taille maximale du fichier
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Fonction pour convertir l'image en bytes
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Création de colonnes pour afficher les images
col1, col2 = st.columns(2)

# Upload d'une image depuis la section latérale
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Vérification de la taille du fichier et traitement de l'image
if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("Image trop grande. Maximum autorisé : 5MB.")
    else:
        image = Image.open(my_upload)
        col1.write("Image originale :camera:")
        col1.image(image)
        
        # Ajoutez des curseurs pour le contraste et l'exposition
        contraste = st.sidebar.slider("Contraste", 10, 200, 100, 10) / 100.0  # Valeurs en pourcentage
        exposition = st.sidebar.slider("Exposition", 10, 200, 100, 10) / 100.0  # Valeurs en pourcentage

        if st.button("Retirer l'arrière-plan"):
            # Appliquer les ajustements de contraste et d'exposition
            image = ImageEnhance.Contrast(image).enhance(contraste)
            image = ImageEnhance.Brightness(image).enhance(exposition)
            
            # Retirer l'arrière-plan
            fixed = remove(image)
            col2.write("Image sans arrière-plan :wrench:")
            col2.image(fixed)
            st.sidebar.markdown("\n")
            st.sidebar.download_button("Télécharger l'image traitée", convert_image(fixed), "fixed.png", "image/png")
else:
    # Afficher une image par défaut (zebra.jpg)
    default_image = Image.open("zebra.jpg")
    col1.write("Image par défaut :camera:")
    col1.image(default_image)

# Bouton de réinitialisation
if st.button("Réinitialiser"):
    st.experimental_rerun()

# Pied de page
st.sidebar.markdown("Data Science For Business \n TOOLS FOR DATA SCIENCE \n Streamlit Application")
st.sidebar.text("© 2023 Constance Guelluy")
st.sidebar.image("HEC_logo.png", use_column_width=True)
