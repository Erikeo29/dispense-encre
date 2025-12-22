import streamlit as st
import base64
import os
import pandas as pd

# --- Configuration ---
st.set_page_config(page_title="Analyse de Simulation", page_icon="🔬", layout="wide")

# --- Chemins ---
BASE_PATH = "dispense-encre/dispense-encre"
DOC_PATH = os.path.join(BASE_PATH, "documentation")

LBM_SRC = "/home/erikeo29/17_RD_Ag_AgCl/41_AgAgCl_OF_LBM/01_AgCl_OF_LBM_v1/src/lbm_solver/dropletCavity2D.cpp"
LBM_RES = "/home/erikeo29/17_RD_Ag_AgCl/41_AgAgCl_OF_LBM/01_AgCl_OF_LBM_v1/results"
SPH_SRC = "/home/erikeo29/17_RD_Ag_AgCl/42_AgACl_OF_SPH/01_AgCl_OF_SPH_v1/templates/pysph/droplet_spreading.py"
SPH_RES = "/home/erikeo29/17_RD_Ag_AgCl/42_AgACl_OF_SPH/01_AgCl_OF_SPH_v1/results"
VOF_RES = "/home/erikeo29/17_RD_Ag_AgCl/40_AgCl_OpenFOAM/04_AgCl_OF_v4/results"

# --- Fonctions Utilitaires ---
@st.cache_data
def load_markdown(filename):
    """Charge un fichier MD depuis le dossier documentation."""
    path = os.path.join(DOC_PATH, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f: return f.read()
    except FileNotFoundError: return f"⚠️ Fichier manquant : {filename}"

@st.cache_data
def load_code(path):
    """Charge un fichier de code source externe."""
    try:
        with open(path, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e: return f"⚠️ Erreur lecture code : {str(e)}"

def load_media(path):
    """Charge une image/gif en base64 pour affichage HTML."""
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        ext = path.lower().split('.')[-1]
        mime = 'image/gif' if ext == 'gif' else 'image/jpeg' if ext in ['jpg','jpeg'] else 'image/png'
        return f'<img src="data:{mime};base64,{data}" style="width:100%; max-width:600px;">'
    except: return None

@st.cache_data
def load_mapping(type_):
    """Charge les CSV de mapping GIF ou PNG."""
    file = 'gif_mapping.csv' if type_ == 'gif' else 'png_mapping .csv'
    try:
        return pd.read_csv(os.path.join(BASE_PATH, file), sep=';', encoding='utf-8')
    except: return {}

def display_smart_doc(filename):
    """Affiche un MD en gérant intelligemment les blocs de code Python."""
    content = load_markdown(filename)
    if "```python" in content:
        parts = content.split("```python")
        for i, p in enumerate(parts):
            if i > 0:
                if "```" in p:
                    c, t = p.split("```", 1)
                    st.code(c.strip(), language='python', line_numbers=False)
                    st.markdown(t)
                else: st.code(p.strip(), language='python', line_numbers=False)
            else: st.markdown(p)
    else: st.markdown(content)

# --- Interface ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", 
    ("Introduction", "Modèles de modélisation multifluidique", 
     "1. FEM / Phase-Field (Python)", "2. VOF (OpenFOAM)", 
     "3. LBM (Palabos C++)", "4. SPH (PySPH Python)"))

# --- Pages ---
if page == "Introduction":
    st.markdown(load_markdown("intro.md"))
    # Galerie
    c1, c2 = st.columns(2); c3, c4 = st.columns(2)
    with c1: 
        st.markdown("**FEM**"); i = os.path.join(BASE_PATH, "gif/gif_a01.gif")
        if os.path.exists(i): st.image(i, use_container_width=True)
    with c2:
        st.markdown("**VOF**"); i = os.path.join(VOF_RES, "93/animation_vtk.gif")
        if os.path.exists(i): st.image(i, use_container_width=True)
    with c3:
        st.markdown("**LBM**"); i = os.path.join(LBM_RES, "29_plat41_v0/simulation_sharp.gif")
        if os.path.exists(i): st.image(i, use_container_width=True)
    with c4:
        st.markdown("**SPH**"); i = os.path.join(SPH_RES, "03_cavity_30ms_symmetric_v0/animation.gif")
        if os.path.exists(i): st.image(i, use_container_width=True)

elif page == "Modèles de modélisation multifluidique":
    st.markdown(load_markdown("comparison.md"))

elif "FEM" in page:
    st.title("Modèle 1 : FEM / Phase-Field")
    t1, t2, t3, t4 = st.tabs(["Physique", "Code", "Exemples (GIF)", "Exemples (PNG)"])
    with t1: display_smart_doc("ink_dispensing_physique_v1.md")
    with t2: display_smart_doc("ink_dispensing_code_v8.md")
    with t3:
        st.subheader("Visualiseur GIF")
        c1, c2 = st.columns(2)
        with c1:
            p1 = (st.selectbox("Puit",[800,1000,1500],key="gd1"), st.selectbox("Buse",[200,250,300],key="gb1"),
                  st.selectbox("Shift",[0,-75,-150],key="gs1"), st.selectbox("Visc",[5.0,1.5],key="gv1"),
                  st.selectbox("Angle P",[90,35],key="ga1"), st.selectbox("Angle F",[35,75],key="go1"))
        with c2:
            p2 = (st.selectbox("Puit",[800,1000,1500],key="gd2",index=1), st.selectbox("Buse",[200,250,300],key="gb2",index=1),
                  st.selectbox("Shift",[0,-75,-150],key="gs2",index=1), st.selectbox("Visc",[5.0,1.5],key="gv2",index=1),
                  st.selectbox("Angle P",[90,35],key="ga2",index=1), st.selectbox("Angle F",[35,75],key="go2",index=1))
        if st.button("LANCER GIF"):
            st.session_state.run_g = True; st.session_state.pg = (p1, p2)
        if st.session_state.get('run_g'):
            r1, r2 = st.columns(2); m = load_mapping('gif')
            for i, c in enumerate([r1, r2]):
                with c:
                    k = (int(st.session_state.pg[i][0]), int(st.session_state.pg[i][1]), int(st.session_state.pg[i][2]), 
                         float(str(st.session_state.pg[i][3]).replace(',', '.')), int(st.session_state.pg[i][4]), int(st.session_state.pg[i][5]))
                    if k in m.keys(): 
                        path = os.path.join(BASE_PATH, "gif", m.loc[m[(m['diamètre du puit (µm)']==k[0]) & (m['diamètre de la buse (µm)']==k[1]) & (m['shift buse en x (µm)']==k[2])].index[0], 'nom fichier gif']) # Simplification mapping logic needed here but keeping generic for now
                        # Re-implementing specific mapping logic for safety
                        found = False
                        for _, row in m.iterrows():
                             if (int(row[0])==k[0] and int(row[1])==k[1] and int(row[2])==k[2] and 
                                 float(str(row[3]).replace(',','.'))==k[3] and int(row[4])==k[4] and int(row[5])==k[5]):
                                 img = os.path.join(BASE_PATH, "gif", row['nom fichier gif'])
                                 st.markdown(load_media(img), unsafe_allow_html=True); found=True; break
                        if not found: st.warning("Non trouvé")

    with t4:
        st.subheader("Visualiseur PNG")
        c1, c2 = st.columns(2)
        with c1:
            p1 = (st.selectbox("Temps",[20,40],key="pt1"), st.selectbox("Visc",[0.05,0.5,1.5,5.0],index=2,key="pv1"),
                  st.selectbox("Sx",[0,-75],key="psx1"), st.selectbox("Sz",[0,-30],key="psz1"),
                  st.selectbox("Angle",[15,35,75],key="pa1"), st.selectbox("Rempl.",[0.6,0.8],key="pr1"))
        with c2:
            p2 = (st.selectbox("Temps",[20,40],key="pt2",index=1), st.selectbox("Visc",[0.05,0.5,1.5,5.0],index=3,key="pv2"),
                  st.selectbox("Sx",[0,-75],key="psx2",index=1), st.selectbox("Sz",[0,-30],key="psz2",index=1),
                  st.selectbox("Angle",[15,35,75],index=1,key="pa2"), st.selectbox("Rempl.",[0.6,0.8],index=1,key="pr2"))
        if st.button("LANCER PNG"):
            st.session_state.run_p = True; st.session_state.pp = (p1, p2)
        if st.session_state.get('run_p'):
            r1, r2 = st.columns(2); m = load_mapping('png')
            for i, c in enumerate([r1, r2]):
                with c:
                    k = (int(st.session_state.pp[i][0]), float(str(st.session_state.pp[i][1]).replace(',', '.')), 
                         int(st.session_state.pp[i][2]), int(st.session_state.pp[i][3]), int(st.session_state.pp[i][4]), float(str(st.session_state.pp[i][5]).replace(',', '.')))
                    found = False
                    for _, row in m.iterrows():
                         if (int(row[0])==k[0] and float(str(row[1]).replace(',','.'))==k[1] and int(row[2])==k[2] and 
                             int(row[3])==k[3] and int(row[4])==k[4] and float(str(row[5]).replace(',','.'))==k[5]):
                             img = os.path.join(BASE_PATH, "png", row['nom fichier gif'].replace('.png','.jpg'))
                             st.markdown(load_media(img), unsafe_allow_html=True); found=True; break
                    if not found: st.warning("Non trouvé")

elif "VOF" in page:
    st.title("Modèle 2 : VOF (OpenFOAM)")
    t1, t2, t3 = st.tabs(["Physique", "Code", "Exemples"])
    with t1: st.markdown(load_markdown("vof_physics.md"))
    with t2:
        st.header("Configuration interFoam")
        st.code("transportModel Carreau; rho 3000; nu0 1.667e-4; sigma 0.04;", language='cpp', line_numbers=False)
        st.code("div(phi,alpha) Gauss interfaceCompression vanLeer 1;", language='cpp', line_numbers=False)
    with t3:
        i = os.path.join(VOF_RES, "93/animation_vtk.gif")
        if os.path.exists(i): st.image(i, caption="Cas 93 - Animation VOF")

elif "LBM" in page:
    st.title("Modèle 3 : LBM (Palabos)")
    t1, t2, t3 = st.tabs(["Physique", "Code", "Exemples"])
    with t1: st.markdown(load_markdown("lbm_physics.md"))
    with t2: st.code(load_code(LBM_SRC), language='cpp', line_numbers=False)
    with t3:
        i = os.path.join(LBM_RES, "29_plat41_v0/simulation_sharp.gif")
        if os.path.exists(i): st.image(i, caption="Cas 29 - Animation LBM")

elif "SPH" in page:
    st.title("Modèle 4 : SPH (PySPH)")
    t1, t2, t3 = st.tabs(["Physique", "Code", "Exemples"])
    with t1: st.markdown(load_markdown("sph_physics.md"))
    with t2: st.code(load_code(SPH_SRC), language='python', line_numbers=False)
    with t3:
        c1, c2 = st.columns(2)
        with c1:
            i = os.path.join(SPH_RES, "03_cavity_30ms_symmetric_v0/animation.gif")
            if os.path.exists(i): st.image(i, caption="Animation SPH")
        with c2:
            i = os.path.join(SPH_RES, "03_cavity_30ms_symmetric_v0/final_state.png")
            if os.path.exists(i): st.image(i, caption="État Final SPH")
