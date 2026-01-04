import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from qr_logic import compress_image

# Page Configuration
st.set_page_config(
    page_title="QR Compression Démo",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
        color: #1a1a1a;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .metric-container {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        transition-duration: 0.4s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# Application Header
st.title("📉 Compression d'Image via Décomposition QR")
st.markdown("Cette application interactive démontre comment la **Décomposition QR** peut être utilisée pour réduire la dimensionnalité d'une image tout en préservant ses caractéristiques principales.")
st.markdown("---")

# Sidebar - Image Upload
with st.sidebar:
    st.header("Upload & Paramètres")
    uploaded_file = st.file_uploader("Choisissez une image (JPG, PNG)", type=["jpg", "jpeg", "png"])
    
    st.markdown("### À propos")
    st.info("""
    **QR Decomposition** factorise une matrice $A$ en :
    
    $A = Q \cdot R$
    
    - $Q$ : Matrice orthogonale
    - $R$ : Matrice triangulaire supérieure
    
    En ne gardant que les $k$ premières colonnes de $Q$ et les $k$ premières lignes de $R$, on obtient une approximation compressée de l'image.
    """)

if uploaded_file is not None:
    # Load and process image
    try:
        image = Image.open(uploaded_file)
        
        # Convert to grayscale
        gray_image = image.convert('L')
        image_matrix = np.array(gray_image)
        
        h, w = image_matrix.shape
        st.sidebar.markdown(f"**Dimensions de l'image**: {w}x{h}")
        
        # Slider for k
        max_k = min(h, w)
        k = st.sidebar.slider("Nombre de composantes (k)", min_value=1, max_value=max_k, value=min(50, max_k))
        
        # Perform Compression
        compressed_img, orig_size, comp_size = compress_image(image_matrix, k)
        
        # Calculate Compression Stats
        compression_ratio = (1 - (comp_size / orig_size)) * 100
        
        # Display Results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Image Originale")
            st.image(image_matrix, caption=f"Taille: {w}x{h}", use_column_width=True, clamp=True, channels='GRAY')
            
        with col2:
            st.subheader(f"Image Compressée (k={k})")
            # Normalize and cast to uint8 for display
            compressed_display = np.clip(compressed_img, 0, 255).astype(np.uint8)
            st.image(compressed_display, caption=f"Taille Approximation", use_column_width=True, clamp=True, channels='GRAY')
            
        # Analysis Section
        st.markdown("### 📊 Analyse de Performance")
        
        cols = st.columns(3)
        cols[0].metric(label="Taille Originale (pixels)", value=f"{orig_size:,}")
        cols[1].metric(label="Taille Compressée (valeurs)", value=f"{comp_size:,}")
        cols[2].metric(label="Taux de Compression", value=f"{compression_ratio:.2f}%", delta_color="normal")
        
        st.progress(comp_size / orig_size)
        st.caption(f"Données conservées : {(comp_size / orig_size)*100:.1f}%")
        
    except Exception as e:
        st.error(f"Erreur lors du traitement de l'image : {e}")

else:
    st.info("👋 Veuillez charger une image dans la barre latérale pour commencer.")
    
    # Example/Placeholder visualization or text
    st.markdown("""
    ### Comment ça marche ?
    
    1. **Upload** : Chargez n'importe quelle image.
    2. **Prétraitement** : L'image est convertie en niveaux de gris (matrice 2D).
    3. **Décomposition** : `numpy.linalg.qr` sépare l'information.
    4. **Reconstruction** : On ne garde que les composants les plus significatifs.
    """)
