import streamlit as st
import base64
import os
import pandas as pd

# --- Configuration de la page ---
st.set_page_config(page_title="Simulation Dispense", layout="wide")

# --- Styles CSS personnalisés ---
custom_css = """
<style>
/* Masquer éléments Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stToolbar"] {display: none;}

/* Onglets plus visibles */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding: 10px 24px;
    background-color: #f0f2f6;
    border-radius: 8px 8px 0 0;
    font-weight: 600;
    font-size: 16px;
}
.stTabs [aria-selected="true"] {
    background-color: #ff4b4b;
    color: white;
}

/* Bouton retour en haut */
.back-to-top {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    background-color: #ff4b4b;
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
}
.back-to-top:hover {
    background-color: #d63030;
    transform: scale(1.1);
}
</style>

<!-- Bouton retour en haut -->
<a href="#top" class="back-to-top" title="Retour en haut">&#8679;</a>
<div id="top"></div>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Chemins Absolus Robustes (Compatible Cloud) ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DOC_PATH = os.path.join(ROOT_DIR, "docs")
DATA_PATH = os.path.join(ROOT_DIR, "data")
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")

# Chemins vers les codes sources
LBM_SRC = os.path.join(DOC_PATH, "code/code_lbm.cpp")
SPH_SRC = os.path.join(DOC_PATH, "code/code_sph.py")

# Chemins vers les exemples visuels
FEM_GIF_EX = os.path.join(ASSETS_PATH, "fem/gif/gif_a01.gif")
VOF_GIF_EX = os.path.join(ASSETS_PATH, "vof/gif/animation_vof_93.gif")
LBM_GIF_EX = os.path.join(ASSETS_PATH, "lbm/gif/simulation_lbm_29.gif")
SPH_GIF_EX = os.path.join(ASSETS_PATH, "sph/gif/animation_sph_03.gif")

# --- Fonctions Utilitaires ---

@st.cache_data(ttl=600)
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

@st.cache_data(ttl=600)
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

def load_file_content(path):
    try:
        with open(path, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e: return f"Fichier non trouvé : {path}"

def load_media_as_base64(file_path):
    try:
        with open(file_path, "rb") as file:
            contents = file.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        if file_path.lower().endswith(('.jpg', '.jpeg')): mime_type = 'image/jpeg'
        elif file_path.lower().endswith('.gif'): mime_type = 'image/gif'
        else: mime_type = 'image/png'
        return f'<img src="data:{mime_type};base64,{data_url}" style="width:100%; max-width:600px;">'
    except Exception: return None

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
selected_page = st.sidebar.radio(
    "Aller à :",
    ("Accueil", "Introduction", "Comparaison des modèles", "1. FEM / Phase-Field", "2. VOF (OpenFOAM)", "3. LBM (Palabos)", "4. SPH (PySPH)", "Conclusion", "Équations clés", "Lexique")
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Version 3.3.0** - Dec 2025
*EQU Research*

**Nouveautés :**
- Page d'accueil
- Documentation enrichie
- Équations clés & Lexique
- UI améliorée
""")

# --- Pages ---

# ===== PAGE ACCUEIL =====
if selected_page == "Accueil":
    st.title("Simulation de Dispense d'Encre Ag/AgCl")
    st.markdown(load_file_content(os.path.join(DOC_PATH, "accueil/accueil.md")))

    st.markdown("---")
    st.subheader("Aperçu des 4 Modèles de Simulation")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.markdown("#### 1. FEM / Phase-Field")
        if os.path.exists(FEM_GIF_EX):
            st.image(FEM_GIF_EX, use_container_width=True)
        st.caption("Méthode des éléments finis - Python/FEniCS")

    with col2:
        st.markdown("#### 2. VOF (OpenFOAM)")
        if os.path.exists(VOF_GIF_EX):
            st.image(VOF_GIF_EX, use_container_width=True)
        st.caption("Volume of Fluid - C++/OpenFOAM")

    with col3:
        st.markdown("#### 3. LBM (Palabos)")
        if os.path.exists(LBM_GIF_EX):
            st.image(LBM_GIF_EX, use_container_width=True)
        st.caption("Lattice Boltzmann - C++/Palabos")

    with col4:
        st.markdown("#### 4. SPH (PySPH)")
        if os.path.exists(SPH_GIF_EX):
            st.image(SPH_GIF_EX, use_container_width=True)
        st.caption("Smoothed Particle Hydrodynamics - Python/PySPH")

# ===== PAGE INTRODUCTION =====
elif selected_page == "Introduction":
    st.title("Introduction : Contexte Scientifique")
    st.markdown("---")
    st.markdown(load_file_content(os.path.join(DOC_PATH, "intro/intro_project.md")))

# ===== PAGE COMPARAISON =====
elif selected_page == "Comparaison des modèles":
    st.title("Comparaison des Méthodes de Modélisation")
    st.markdown("---")
    st.markdown(load_file_content(os.path.join(DOC_PATH, "comparaison/comparaison_models.md")))

# ===== PAGE FEM =====
elif "FEM" in selected_page:
    st.title("Modèle 1 : FEM / Phase-Field (Python)")
    tab_phys, tab_code, tab_gif, tab_png = st.tabs(["Physique", "Code", "Exemples GIF", "Exemples PNG"])

    with tab_phys:
        display_smart_markdown(load_file_content(os.path.join(DOC_PATH, "physics/physics_fem.md")))

    with tab_code:
        display_smart_markdown(load_file_content(os.path.join(DOC_PATH, "code/code_fem.md")))

    with tab_gif:
        st.subheader("Visualiseur de Simulations GIF")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Simulation 1**")
            p1 = (st.selectbox("Puit (µm)",[800,1000,1500],key="g1_d"),
                  st.selectbox("Buse (µm)",[200,250,300],key="g1_b"),
                  st.selectbox("Shift X (µm)",[0,-75,-150],key="g1_s"),
                  st.selectbox("Viscosité (Pa·s)",[5.0,1.5],key="g1_v"),
                  st.selectbox("Angle Paroi (°)",[90,35],key="g1_a"),
                  st.selectbox("Angle Or (°)",[35,75],key="g1_o"))
        with c2:
            st.markdown("**Simulation 2**")
            p2 = (st.selectbox("Puit (µm)",[800,1000,1500],key="g2_d",index=1),
                  st.selectbox("Buse (µm)",[200,250,300],key="g2_b",index=1),
                  st.selectbox("Shift X (µm)",[0,-75,-150],key="g2_s",index=1),
                  st.selectbox("Viscosité (Pa·s)",[5.0,1.5],key="g2_v",index=1),
                  st.selectbox("Angle Paroi (°)",[90,35],key="g2_a",index=1),
                  st.selectbox("Angle Or (°)",[35,75],key="g2_o",index=1))

        if st.button("LANCER LES SIMULATIONS", type="primary", use_container_width=True):
            st.session_state.run_g = True
            st.session_state.p_g = (p1, p2)

        if st.session_state.get('run_g', False):
            r1, r2 = st.columns(2)
            m = load_gif_mapping()
            for i, c in enumerate([r1, r2]):
                with c:
                    params = st.session_state.p_g[i]
                    if params in m:
                        st.markdown(load_media_as_base64(m[params]), unsafe_allow_html=True)
                    else:
                        st.warning("Combinaison non disponible")

    with tab_png:
        st.subheader("Visualiseur d'Images PNG")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Image 1**")
            p1 = (st.selectbox("Temps (ms)",[20,40],key="p1_t"),
                  st.selectbox("Viscosité",[0.05,0.5,1.5,5.0],index=2,key="p1_v"),
                  st.selectbox("Shift X",[0,-75],key="p1_x"),
                  st.selectbox("Shift Z",[0,-30],key="p1_z"),
                  st.selectbox("Angle",[15,35,75],key="p1_a"),
                  st.selectbox("Remplissage",[0.6,0.8],key="p1_r"))
        with c2:
            st.markdown("**Image 2**")
            p2 = (st.selectbox("Temps (ms)",[20,40],key="p2_t",index=1),
                  st.selectbox("Viscosité",[0.05,0.5,1.5,5.0],index=3,key="p2_v"),
                  st.selectbox("Shift X",[0,-75],key="p2_x",index=1),
                  st.selectbox("Shift Z",[0,-30],key="p2_z",index=1),
                  st.selectbox("Angle",[15,35,75],index=1,key="p2_a"),
                  st.selectbox("Remplissage",[0.6,0.8],index=1,key="p2_r"))

        if st.button("AFFICHER LES IMAGES", type="primary", use_container_width=True):
            st.session_state.run_p = True
            st.session_state.p_p = (p1, p2)

        if st.session_state.get('run_p', False):
            r1, r2 = st.columns(2)
            m = load_png_mapping()
            for i, c in enumerate([r1, r2]):
                with c:
                    params = st.session_state.p_p[i]
                    if params in m:
                        st.markdown(load_media_as_base64(m[params]), unsafe_allow_html=True)
                    else:
                        st.warning("Image non disponible")

# ===== PAGE VOF =====
elif "VOF" in selected_page:
    st.title("Modèle 2 : VOF (OpenFOAM)")
    tab_phys, tab_code, tab_ex = st.tabs(["Physique", "Code", "Exemples"])

    with tab_phys:
        st.markdown(load_file_content(os.path.join(DOC_PATH, "physics/physics_vof.md")))

    with tab_code:
        st.subheader("Configuration OpenFOAM")
        st.code("""// transportProperties
transportModel Carreau;

CarreauCoeffs {
    nu0   1.667e-4;  // Viscosité au repos
    nuInf 5.56e-5;   // Viscosité infinie
    k     0.15;      // Temps de relaxation
    n     0.7;       // Indice rhéofluidifiant
}

sigma 0.04;  // Tension de surface [N/m]
rho   3000;  // Masse volumique [kg/m³]""", language='cpp')

    with tab_ex:
        st.subheader("Exemple de Simulation VOF")
        if os.path.exists(VOF_GIF_EX):
            st.image(VOF_GIF_EX, caption="Simulation VOF - Cas 93", use_container_width=True)

# ===== PAGE LBM =====
elif "LBM" in selected_page:
    st.title("Modèle 3 : LBM (Palabos C++)")
    tab_phys, tab_code, tab_ex = st.tabs(["Physique", "Code", "Exemples"])

    with tab_phys:
        st.markdown(load_file_content(os.path.join(DOC_PATH, "physics/physics_lbm.md")))

    with tab_code:
        st.subheader("Code Source Palabos")
        st.code(load_file_content(LBM_SRC), language='cpp')

    with tab_ex:
        st.subheader("Exemple de Simulation LBM")
        if os.path.exists(LBM_GIF_EX):
            st.image(LBM_GIF_EX, caption="Simulation LBM - Cas 29", use_container_width=True)

# ===== PAGE SPH =====
elif "SPH" in selected_page:
    st.title("Modèle 4 : SPH (PySPH Python)")
    tab_phys, tab_code, tab_ex = st.tabs(["Physique", "Code", "Exemples"])

    with tab_phys:
        st.markdown(load_file_content(os.path.join(DOC_PATH, "physics/physics_sph.md")))

    with tab_code:
        st.subheader("Code Source PySPH")
        st.code(load_file_content(SPH_SRC), language='python')

    with tab_ex:
        st.subheader("Exemple de Simulation SPH")
        if os.path.exists(SPH_GIF_EX):
            st.image(SPH_GIF_EX, caption="Simulation SPH - Cas 03", use_container_width=True)

# ===== PAGE CONCLUSION =====
elif selected_page == "Conclusion":
    st.title("Conclusion et Perspectives")
    st.markdown("---")
    st.markdown(load_file_content(os.path.join(DOC_PATH, "conclusion/conclusion.md")))

# ===== PAGE ÉQUATIONS CLÉS =====
elif selected_page == "Équations clés":
    st.title("Équations Clés des Modèles")
    st.markdown("---")
    st.markdown(load_file_content(os.path.join(DOC_PATH, "equations/equations_clef.md")))

# ===== PAGE LEXIQUE =====
elif selected_page == "Lexique":
    st.title("Lexique et Acronymes")
    st.markdown("---")
    st.markdown(load_file_content(os.path.join(DOC_PATH, "lexique/lexique.md")))
