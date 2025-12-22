import streamlit as st
import base64
import os
import pandas as pd

# --- Configuration de la page ---
st.set_page_config(page_title="Analyse de Simulation", page_icon="🔬", layout="wide")

# --- Masquage des éléments de l'interface (Confidentialité) ---
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stToolbar"] {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- Chemins Relatifs (Structure Propre) ---
BASE_PATH = "."
DOC_PATH = "docs"
DATA_PATH = "data"
ASSETS_PATH = "assets"

# Chemins vers les codes sources
LBM_SRC = os.path.join(DOC_PATH, "code/code_lbm.cpp")
SPH_SRC = os.path.join(DOC_PATH, "code/code_sph.py")

# Chemins vers les exemples visuels
VOF_GIF_EX = os.path.join(ASSETS_PATH, "vof/gif/animation_vof_93.gif")
LBM_GIF_EX = os.path.join(ASSETS_PATH, "lbm/gif/simulation_lbm_29.gif")
SPH_GIF_EX = os.path.join(ASSETS_PATH, "sph/gif/animation_sph_03.gif")

# --- Fonctions Utilitaires ---
@st.cache_data
def load_gif_mapping():
    try:
        df = pd.read_csv(os.path.join(DATA_PATH, 'fem_gif_mapping.csv'), sep=';', encoding='utf-8')
        mapping = {}
        for _, row in df.iterrows():
            key = (
                int(row['diamètre du puit (µm)']), int(row['diamètre de la buse (µm)']),
                int(row['shift buse en x (µm)']), float(str(row["Viscosité de l'encre (Pa.s)"]).replace(',', '.')), 
                int(row['CA wall right']), int(row['CA gold'])
            )
            mapping[key] = os.path.join(ASSETS_PATH, "fem/gif", row['nom fichier gif'])
        return mapping
    except Exception: return {}

@st.cache_data
def load_png_mapping():
    try:
        df = pd.read_csv(os.path.join(DATA_PATH, 'fem_png_mapping.csv'), sep=';', encoding='utf-8')
        mapping = {}
        for _, row in df.iterrows():
            key = (
                int(row['temps dispense (ms)']), float(str(row["Viscosité de l'encre (Pa.s)"]).replace(',', '.')), 
                int(row['shift buse en x (µm)']), int(row['shift buse en z (µm)']),
                int(row['CA gold']), float(str(row['remplissage']).replace(',', '.'))
            )
            filename = row['nom fichier gif'].replace('.png', '.jpg')
            mapping[key] = os.path.join(ASSETS_PATH, "fem/png", filename)
        return mapping
    except Exception: return {}

@st.cache_data
def load_file_content(path):
    try:
        with open(path, 'r', encoding='utf-8') as f: return f.read()
    except Exception: return f"⚠️ Fichier non trouvé : {path}"

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
st.sidebar.title("Navigation")

# Astuce pour espacement : des options vides ou séparateurs ne sont pas possibles dans un radio unique.
# Je scinde en sections avec des st.markdown("---") entre les blocs logiques si je n'utilise pas un radio unique.
# MAIS pour garder une navigation fluide (état unique), je vais utiliser des espaces insécables dans les noms ou accepter la liste contiguë.
# SOLUTION CLIENT : "saute une ligne après intro..." -> Je vais utiliser des options "vides" non sélectionnables ou juste aérer visuellement via des markdowns entre des widgets, mais cela casse la navigation unique.
# Je vais rester sur un radio unique mais avec des noms clairs, et ajouter la section "À propos" en bas qui elle sera bien séparée.

nav_options = [
    "Introduction",
    "Modèles de modélisation multifluidique",
    "1. FEM / Phase-Field (Python)",
    "2. VOF (OpenFOAM)",
    "3. LBM (Palabos C++)",
    "4. SPH (PySPH Python)",
    "Conclusion"
]

# Astuce visuelle : j'ajoute des sauts de ligne dans les libellés pour aérer ? Non, Streamlit ne le rend pas bien.
# Je vais garder la liste propre.

selected_page = st.sidebar.radio("Aller à :", nav_options)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### À propos
**Application de simulation de dispense d'encre.**

**Version:** 3.0.0 - EQU - Dec-25

**Features:**
- Comparaison de 4 modèles (FEM, VOF, LBM, SPH)
- Visualiseurs interactifs (GIF et PNG)
- Documentation physique détaillée
- Consultation des codes sources réels
""")

# --- 1. PAGE INTRODUCTION ---
if selected_page == "Introduction":
    st.title("🔬 Simulation de Dispense d'Encre type Ag/AgCl")
    st.markdown(load_file_content(os.path.join(DOC_PATH, "intro/intro_project.md")))
    
    # Galerie d'images
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.markdown("**1. FEM / Phase-Field**")
        fem_gif = os.path.join(ASSETS_PATH, "fem/gif/gif_a01.gif")
        if os.path.exists(fem_gif): st.image(fem_gif, use_container_width=True)
    with col2:
        st.markdown("**2. VOF (OpenFOAM)**")
        if os.path.exists(VOF_GIF_EX): st.image(VOF_GIF_EX, use_container_width=True)
    with col3:
        st.markdown("**3. LBM (Palabos)**")
        if os.path.exists(LBM_GIF_EX): st.image(LBM_GIF_EX, use_container_width=True)
    with col4:
        st.markdown("**4. SPH (PySPH)**")
        if os.path.exists(SPH_GIF_EX): st.image(SPH_GIF_EX, use_container_width=True)


# --- 2. MODÈLES MULTIFLUIDIQUES ---
elif selected_page == "Modèles de modélisation multifluidique":
    st.title("📊 Comparatif des Méthodes de Modélisation Multifluidique")
    st.markdown("---")
    st.markdown(load_file_content(os.path.join(DOC_PATH, "comparaison/comparaison_models.md")))

# --- 3. FEM ---
elif "FEM" in selected_page:
    st.title("Modèle 1 : FEM / Phase-Field (Python)")
    tab_phys, tab_code, tab_gif, tab_png = st.tabs(["Physique", "Code", "Exemples (GIF)", "Exemples (PNG)"])
    with tab_phys:
        display_smart_markdown(load_file_content(os.path.join(DOC_PATH, "physics/physics_fem.md")))
    with tab_code:
        display_smart_markdown(load_file_content(os.path.join(DOC_PATH, "code/code_fem.md")))
    with tab_gif:
        st.subheader("Visualiseur GIF")
        c1, c2 = st.columns(2)
        with c1:
            p1 = (st.selectbox("Puit",[800,1000,1500],key="g1_d"), st.selectbox("Buse",[200,250,300],key="g1_b"),
                  st.selectbox("Shift",[0,-75,-150],key="g1_s"), st.selectbox("Visc",[5.0,1.5],key="g1_v"),
                  st.selectbox("Angle P",[90,35],key="g1_a"), st.selectbox("Angle F",[35,75],key="g1_o"))
        with c2:
            p2 = (st.selectbox("Puit",[800,1000,1500],key="g2_d",index=1), st.selectbox("Buse",[200,250,300],key="g2_b",index=1),
                  st.selectbox("Shift",[0,-75,-150],key="g2_s",index=1), st.selectbox("Visc",[5.0,1.5],key="g2_v",index=1),
                  st.selectbox("Angle P",[90,35],key="g2_a",index=1), st.selectbox("Angle F",[35,75],key="g2_o",index=1))
        if st.button("LANCER GIF"):
            st.session_state.run_g = True
            st.session_state.p_g = (p1, p2)
        if st.session_state.get('run_g', False):
            r1, r2 = st.columns(2)
            m = load_gif_mapping()
            for i, c in enumerate([r1, r2]):
                with c:
                    params = st.session_state.p_g[i]
                    if params in m: st.markdown(load_media_as_base64(m[params]), unsafe_allow_html=True)
                    else: st.warning("Simulation non trouvée.")
    with tab_png:
        st.subheader("Visualiseur PNG")
        c1, c2 = st.columns(2)
        with c1:
            p1 = (st.selectbox("Temps",[20,40],key="p1_t"), st.selectbox("Visc",[0.05,0.5,1.5,5.0],index=2,key="p1_v"),
                  st.selectbox("Sx",[0,-75],key="p1_x"), st.selectbox("Sz",[0,-30],key="p1_z"),
                  st.selectbox("Angle",[15,35,75],key="p1_a"), st.selectbox("Rempl.",[0.6,0.8],key="p1_r"))
        with c2:
            p2 = (st.selectbox("Temps",[20,40],key="p2_t",index=1), st.selectbox("Visc",[0.05,0.5,1.5,5.0],index=3,key="p2_v"),
                  st.selectbox("Sx",[0,-75],key="p2_x",index=1), st.selectbox("Sz",[0,-30],key="p2_z",index=1),
                  st.selectbox("Angle",[15,35,75],index=1,key="p2_a"), st.selectbox("Rempl.",[0.6,0.8],index=1,key="p2_r"))
        if st.button("LANCER PNG"):
            st.session_state.run_p = True
            st.session_state.p_p = (p1, p2)
        if st.session_state.get('run_p', False):
            r1, r2 = st.columns(2)
            m = load_png_mapping()
            for i, c in enumerate([r1, r2]):
                with c:
                    params = st.session_state.p_p[i]
                    if params in m: st.markdown(load_media_as_base64(m[params]), unsafe_allow_html=True)
                    else: st.warning("Image non trouvée.")

# --- 4. VOF ---
elif "VOF" in selected_page:
    st.title("Modèle 2 : VOF (OpenFOAM)")
    t1, t2, t3 = st.tabs(["Physique", "Code", "Exemples"])
    with t1: st.markdown(load_file_content(os.path.join(DOC_PATH, "physics/physics_vof.md")))
    with t2:
        st.header("Configuration")
        st.code("transportModel Carreau; rho 3000; nu0 1.667e-4; sigma 0.04;", language='cpp', line_numbers=False)
    with t3:
        if os.path.exists(VOF_GIF_EX): st.image(VOF_GIF_EX, caption="Simulation VOF - Cas 93")

# --- 5. LBM ---
elif "LBM" in selected_page:
    st.title("Modèle 3 : LBM (Palabos C++)")
    t1, t2, t3 = st.tabs(["Physique", "Code", "Exemples"])
    with t1: st.markdown(load_file_content(os.path.join(DOC_PATH, "physics/physics_lbm.md")))
    with t2:
        st.header("Code Source Palabos")
        st.code(load_file_content(LBM_SRC), language='cpp', line_numbers=False)
    with t3:
        if os.path.exists(LBM_GIF_EX): st.image(LBM_GIF_EX, caption="Simulation LBM - Cas 29")

# --- 6. SPH ---
elif "SPH" in selected_page:
    st.title("Modèle 4 : SPH (PySPH Python)")
    t1, t2, t3 = st.tabs(["Physique", "Code", "Exemples"])
    with t1: st.markdown(load_file_content(os.path.join(DOC_PATH, "physics/physics_sph.md")))
    with t2:
        st.header("Code Source PySPH")
        st.code(load_file_content(SPH_SRC), language='python', line_numbers=False)
    with t3:
        if os.path.exists(SPH_GIF_EX): st.image(SPH_GIF_EX, caption="Simulation SPH - Cas 03")

# --- 7. CONCLUSION ---
elif selected_page == "Conclusion":
    st.title("🎯 Conclusion et Perspectives")
    st.markdown(load_file_content(os.path.join(DOC_PATH, "conclusion/conclusion.md")))