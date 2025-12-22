import streamlit as st
import base64
import os
import pandas as pd

# --- Configuration de la page ---
st.set_page_config(page_title="Analyse de Simulation", page_icon="🔬", layout="wide")

# --- Chemins Externes ---
LBM_SRC_PATH = "/home/erikeo29/17_RD_Ag_AgCl/41_AgAgCl_OF_LBM/01_AgCl_OF_LBM_v1/src/lbm_solver"
LBM_RES_PATH = "/home/erikeo29/17_RD_Ag_AgCl/41_AgAgCl_OF_LBM/01_AgCl_OF_LBM_v1/results"

SPH_SRC_PATH = "/home/erikeo29/17_RD_Ag_AgCl/42_AgACl_OF_SPH/01_AgCl_OF_SPH_v1/templates/pysph"
SPH_RES_PATH = "/home/erikeo29/17_RD_Ag_AgCl/42_AgACl_OF_SPH/01_AgCl_OF_SPH_v1/results"

VOF_RES_PATH = "/home/erikeo29/17_RD_Ag_AgCl/40_AgCl_OpenFOAM/04_AgCl_OF_v4/results"

BASE_PATH = "dispense-encre/dispense-encre"

# --- Fonctions Utilitaires ---
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
def load_file_content(full_path):
    try:
        with open(full_path, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e: return f"⚠️ Erreur: {str(e)}"

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
    ("Introduction", "Modèles de modélisation multifluidique", "1. FEM / Phase-Field (Python)", "2. VOF (OpenFOAM)", "3. LBM (Palabos C++)", "4. SPH (PySPH Python)")
)

# --- 1. PAGE INTRODUCTION ---
if selected_page == "Introduction":
    st.title("🔬 Simulation de Dispense d'Encre type Ag/AgCl")
    st.markdown("### Optimisation de la dispense d'encre conductrice en micro-puits")
    st.markdown("---")
    
    st.info("**Objectif du Projet**")
    st.markdown("""
    Ce projet de R&D vise à comprendre et optimiser le processus complexe de dispense d'encre micro-fluidique.
    L'encre Ag/AgCl doit remplir précisément des micro-puits sans emprisonner d'air ni déborder.
    """)
    st.success("**Comparatif des Approches Numériques**")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    with col1:
        st.markdown("**1. FEM / Phase-Field**")
        fem_gif = os.path.join(BASE_PATH, "gif", "gif_a01.gif")
        if os.path.exists(fem_gif): st.image(fem_gif, use_container_width=True)
    with col2:
        st.markdown("**2. VOF (OpenFOAM)**")
        vof_gif = os.path.join(VOF_RES_PATH, "93/animation_vtk.gif")
        if os.path.exists(vof_gif): st.image(vof_gif, use_container_width=True)
    with col3:
        st.markdown("**3. LBM (Palabos)**")
        lbm_gif = os.path.join(LBM_RES_PATH, "29_plat41_v0/simulation_sharp.gif")
        if os.path.exists(lbm_gif): st.image(lbm_gif, use_container_width=True)
    with col4:
        st.markdown("**4. SPH (PySPH)**")
        sph_gif = os.path.join(SPH_RES_PATH, "03_cavity_30ms_symmetric_v0/animation.gif")
        if os.path.exists(sph_gif): st.image(sph_gif, use_container_width=True)

# --- 2. MODÈLES MULTIFLUIDIQUES ---
elif selected_page == "Modèles de modélisation multifluidique":
    st.title("📊 Modèles de modélisation multifluidique")
    data = {
        "Méthode": ["FEM / Phase-Field", "VOF", "LBM", "SPH"],
        "Principe": ["Interface diffuse", "Fraction volumique", "Mésoscopique", "Particulaire"],
        "Atouts": ["Rigueur physique", "Standard industrie", "HPC / GPU", "Surfaces complexes"],
        "Langage": ["Python (FEniCS)", "C++ (OpenFOAM)", "C++ (Palabos)", "Python (PySPH)"],
        "Hardware": ["CPU", "CPU", "GPU / Cluster", "GPU"]
    }
    st.table(pd.DataFrame(data))
    st.markdown("""
    ### Analyse Critique
    *   **VOF** reste incontournable pour la validation industrielle.
    *   **LBM** offre des performances de calcul impressionnantes sur GPU.
    *   **SPH** est idéal pour les projections dynamiques.
    *   **Phase-Field** apporte une précision thermodynamique inégalée.
    """)

# --- 3. FEM ---
elif "FEM" in selected_page:
    st.title("Modèle 1 : FEM / Phase-Field (Python)")
    t1, t2, t3, t4 = st.tabs(["Physique", "Code", "Exemples (GIF)", "Exemples (PNG)"])
    with t1:
        display_smart_markdown(load_file_content(os.path.join(BASE_PATH, "documentation/ink_dispensing_physique_v1.md")))
    with t2:
        display_smart_markdown(load_file_content(os.path.join(BASE_PATH, "documentation/ink_dispensing_code_v8.md")))
    with t3:
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
    with t4:
        st.subheader("Visualiseur PNG")
        c1, c2 = st.columns(2)
        with c1:
            p1 = (st.selectbox("Temps",[20,40],key="p1_t"), st.selectbox("Visc",[0.05,0.5,1.5,5.0],index=2,key="p1_v"),
                  st.selectbox("Sx",[0,-75],key="p1_x"), st.selectbox("Sz",[0,-30],key="p1_z"),
                  st.selectbox("Angle",[15,35,75],key="p1_a"), st.selectbox("Rempl.",[0.6,0.8],key="p1_r"))
        with c2:
            p2 = (st.selectbox("Temps",[20,40],key="p2_t",index=1), st.selectbox("Visc",[0.05,0.5,1.5,5.0],index=3,key="p2_v"),
                  st.selectbox("Sx",[0,-75],key="p2_x",index=1), st.selectbox("Sz",[0,-30],key="p2_z",index=1),
                  st.selectbox("Angle",[15,35,75],index=1,key="p2_a"), st.selectbox("Rempl.",[0.6,0.8],index=1,key="p2_r")
                 )
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
    with t1:
        st.header("Méthode Volume of Fluid (VOF)")
        st.write("La méthode **VOF** est la référence industrielle. L'interface est capturée par la fraction volumique alpha.")
        st.subheader("1. Suivi d'Interface")
        st.latex(r"\\frac{\\partial \\alpha}{\\partial t} + \\nabla \\cdot (\\mathbf{u} \\alpha) + \\nabla \\cdot [\\mathbf{u}_r \\alpha (1-\\alpha)] = 0")
        st.markdown("""
        Le dernier terme est un terme de compression pour garder l'interface nette.
        Rhéologie de Carreau :
        """)
        st.latex(r"\\eta_{eff} = \\eta_\\infty + (\\eta_0 - \\eta_\\infty) [1 + (\\lambda \\dot{\\gamma})^2 ]^{(n-1)/2}")
    with t2:
        st.header("Configuration")
        st.code("transportModel Carreau; rho 3000; nu0 1.667e-4; sigma 0.04;", language='cpp', line_numbers=False)
    with t3:
        img = os.path.join(VOF_RES_PATH, "93/animation_vtk.gif")
        if os.path.exists(img): st.image(img, caption="Simulation VOF - Cas 93")

# --- 5. LBM ---
elif "LBM" in selected_page:
    st.title("Modèle 3 : LBM (Palabos C++)")
    t1, t2, t3 = st.tabs(["Physique", "Code", "Exemples"])
    with t1:
        st.header("Lattice Boltzmann Method")
        st.markdown("""
        Palabos utilise le modèle **Shan-Chen** (Pseudopotentiel) :
        *   **Principe :** Interactions via un pseudopotentiel.
        *   **Avantages :** Séparation de phase spontanée, mouillage naturel.
        """)
    with t2:
        st.header("Code Source Palabos")
        st.code(load_file_content(os.path.join(LBM_SRC_PATH, "dropletCavity2D.cpp")), language='cpp', line_numbers=False)
    with t3:
        img = os.path.join(LBM_RES_PATH, "29_plat41_v0/simulation_sharp.gif")
        if os.path.exists(img): st.image(img, caption="Simulation LBM - Cas 29")

# --- 6. SPH ---
elif "SPH" in selected_page:
    st.title("Modèle 4 : SPH (PySPH Python)")
    t1, t2, t3 = st.tabs(["Physique", "Code", "Exemples"])
    with t1:
        st.header("Smoothed Particle Hydrodynamics")
        st.latex(r"A(\\mathbf{r}) = \\sum_b m_b \\frac{A_b}{\\rho_b} W(\|\|\\mathbf{r} - \\mathbf{r}_b\|, h)")
        st.subheader("Tension de Surface (Morris)")
        st.latex(r"\\mathbf{F}_{st} = -\\sigma \\kappa \\mathbf{n}")
        st.markdown("Gestion des parois par particules fantômes (Adami).")
    with t2:
        st.header("Code Source PySPH")
        st.code(load_file_content(os.path.join(SPH_SRC_PATH, "droplet_spreading.py")), language='python', line_numbers=False)
    with t3:
        img = os.path.join(SPH_RES_PATH, "03_cavity_30ms_symmetric_v0/animation.gif")
        if os.path.exists(img): st.image(img, caption="Simulation SPH - Cas 03")
