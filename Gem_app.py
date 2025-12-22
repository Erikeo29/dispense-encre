import streamlit as st
import base64
import os
import pandas as pd

# --- Configuration de la page ---
st.set_page_config(page_title="Analyse de Simulation", page_icon="🔬", layout="wide")

# --- Fonctions Utilitaires ---
BASE_PATH = "dispense-encre/dispense-encre"

@st.cache_data
def load_gif_mapping():
    try:
        csv_path = os.path.join(BASE_PATH, 'gif_mapping.csv')
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        mapping = {}
        for _, row in df.iterrows():
            key = (
                int(row['diamètre du puit (µm)']), int(row['diamètre de la buse (µm)']),
                int(row['shift buse en x (µm)']), float(str(row["Viscosité de l'encre (Pa.s)"]).replace(',', '.')),
                int(row['CA wall right']), int(row['CA gold'])
            )
            mapping[key] = os.path.join(BASE_PATH, "gif", row['nom fichier gif'])
        return mapping
    except Exception: return {}

@st.cache_data
def load_png_mapping():
    try:
        csv_path = os.path.join(BASE_PATH, 'png_mapping .csv')
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        mapping = {}
        for _, row in df.iterrows():
            key = (
                int(row['temps dispense (ms)']), float(str(row["Viscosité de l'encre (Pa.s)"]).replace(',', '.')),
                int(row['shift buse en x (µm)']), int(row['shift buse en z (µm)']),
                int(row['CA gold']), float(str(row['remplissage']).replace(',', '.'))
            )
            filename = row['nom fichier gif'].replace('.png', '.jpg')
            mapping[key] = os.path.join(BASE_PATH, "png", filename)
        return mapping
    except Exception: return {}

@st.cache_data
def load_markdown_file(filepath):
    full_path = os.path.join(BASE_PATH, filepath)
    try:
        with open(full_path, 'r', encoding='utf-8') as f: return f.read()
    except FileNotFoundError: return f"⚠️ Fichier non trouvé: {full_path}"

def load_media_as_base64(file_path):
    try:
        with open(file_path, "rb") as file:
            contents = file.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        if file_path.lower().endswith(('.jpg', '.jpeg')): mime_type = 'image/jpeg'
        elif file_path.lower().endswith('.gif'): mime_type = 'image/gif'
        else: mime_type = 'image/png'
        return f'<img src="data:{mime_type};base64,{data_url}" style="width:100%; max-width:600px;">'
    except FileNotFoundError: return None

def display_smart_markdown(content):
    """Affiche un markdown en séparant texte et blocs de code."""
    if "```python" in content:
        parts = content.split("```python")
        for i, part in enumerate(parts):
            if i > 0:
                if "```" in part:
                    code, text = part.split("```", 1)
                    st.code(code.strip(), language='python', line_numbers=False)
                    if text.strip(): st.markdown(text)
                else:
                    st.code(part.strip(), language='python', line_numbers=False)
            elif part.strip():
                st.markdown(part)
    else:
        st.markdown(content)

# --- Barre Latérale ---
st.sidebar.title("Sélection du Modèle")
selected_model = st.sidebar.radio("Choisissez un modèle :", ("FEM / Phase-Field (Python)", "VOF (OpenFOAM)", "LBM", "SPH"))

# --- Fenêtre Principale ---
st.title(f"Modèle Actuel : {selected_model}")

# --- MODÈLE PRINCIPAL : FEM / Phase-Field (Python) ---
if selected_model == "FEM / Phase-Field (Python)":
    tab_phys, tab_code, tab_gif, tab_png = st.tabs(["Physique", "Modèle de Code", "Exemples (GIF)", "Exemples (État Final - PNG)"])
    
    with tab_phys:
        display_smart_markdown(load_markdown_file("documentation/ink_dispensing_physique_v1.md"))
    with tab_code:
        display_smart_markdown(load_markdown_file("documentation/ink_dispensing_code_v8.md"))
    with tab_gif:
        st.subheader("Visualiseur de Simulations Dynamiques (GIFs)")
        with st.expander("PARAMÈTRES DE COMPARAISON (GIF)", expanded=True):
            param_col1, param_col2 = st.columns(2)
            with param_col1:
                st.markdown("##### Simulation 1")
                p1 = (st.selectbox("Diam. puit (µm)",[800,1000,1500],key="gif_d1"), st.selectbox("Diam. buse (µm)",[200,250,300],key="gif_b1"),
                      st.selectbox("Shift x (µm)",[0,-75,-150],key="gif_s1"), st.selectbox("Viscosité (Pa.s)",[5.0,1.5],key="gif_v1"),
                      st.selectbox("Angle paroi (°)",[90,35],key="gif_a1"), st.selectbox("Angle fond puit (°)",[35,75],key="gif_o1"))
            with param_col2:
                st.markdown("##### Simulation 2")
                p2 = (st.selectbox("Diam. puit (µm)",[800,1000,1500],key="gif_d2",index=1), st.selectbox("Diam. buse (µm)",[200,250,300],key="gif_b2",index=1),
                      st.selectbox("Shift x (µm)",[0,-75,-150],key="gif_s2",index=1), st.selectbox("Viscosité (Pa.s)",[5.0,1.5],key="gif_v2",index=1),
                      st.selectbox("Angle paroi (°)",[90,35],key="gif_a2",index=1), st.selectbox("Angle fond puit (°)",[35,75],key="gif_o2",index=1))
            st.session_state.fem_gif_params = (p1, p2)
        if st.button("LANCER COMPARAISON (GIF)", type="primary", use_container_width=True):
            st.session_state.run_gif_comparison = True
        if st.session_state.get('run_gif_comparison', False):
            st.markdown("---"); st.subheader("Résultats (GIF)")
            r_col1, r_col2 = st.columns(2)
            gif_mapping = load_gif_mapping()
            for i, col in enumerate([r_col1, r_col2]):
                with col:
                    params = st.session_state.fem_gif_params[i]
                    if params in gif_mapping: st.markdown(load_media_as_base64(gif_mapping[params]), unsafe_allow_html=True)
                    else: st.warning("Aucune simulation GIF disponible.")
    with tab_png:
        st.subheader("Visualiseur de Simulations État Final (PNG/JPG)")
        with st.expander("PARAMÈTRES DE COMPARAISON (PNG)", expanded=True):
            param_col1_png, param_col2_png = st.columns(2)
            with param_col1_png:
                st.markdown("##### Simulation 1")
                p1_png = (st.selectbox("Temps dispense (ms)",[20,40],key="png_t1"), st.selectbox("Viscosité (Pa.s)",[0.05,0.5,1.5,5.0],index=2,key="png_v1"),
                          st.selectbox("Shift x (µm)",[0,-75],key="png_sx1"), st.selectbox("Shift z (µm)",[0,-30],key="png_sz1"),
                          st.selectbox("Angle fond puit (°)",[15,35,75],index=1,key="png_a1"), st.selectbox("Remplissage",[0.6,0.8],key="png_r1"))
            with param_col2_png:
                st.markdown("##### Simulation 2")
                p2_png = (st.selectbox("Temps dispense (ms)",[20,40],key="png_t2",index=1), st.selectbox("Viscosité (Pa.s)",[0.05,0.5,1.5,5.0],index=3,key="png_v2"),
                          st.selectbox("Shift x (µm)",[0,-75],key="png_sx2",index=1), st.selectbox("Shift z (µm)",[0,-30],key="png_sz2",index=1),
                          st.selectbox("Angle fond puit (°)",[15,35,75],index=2,key="png_a2"), st.selectbox("Remplissage",[0.6,0.8],key="png_r2",index=1))
            st.session_state.fem_png_params = (p1_png, p2_png)
        if st.button("LANCER COMPARAISON (PNG)", type="primary", use_container_width=True):
            st.session_state.run_png_comparison = True
        if st.session_state.get('run_png_comparison', False):
            st.markdown("---"); st.subheader("Résultats (PNG)")
            r_col1_png, r_col2_png = st.columns(2)
            png_mapping = load_png_mapping()
            for i, col in enumerate([r_col1_png, r_col2_png]):
                with col:
                    params = st.session_state.fem_png_params[i]
                    if params in png_mapping: st.markdown(load_media_as_base64(png_mapping[params]), unsafe_allow_html=True)
                    else: st.warning("Aucune simulation PNG disponible.")

# --- Sections Placeholder pour les autres modèles ---
else:
    st.info("Section en cours de développement.")
    if selected_model in ["VOF (OpenFOAM)", "LBM", "SPH"]:
        st.warning(f"Veuillez fournir le contenu et/ou les fichiers de code pour le modèle {selected_model}.")
