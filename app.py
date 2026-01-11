import streamlit as st
import base64
import os
import pandas as pd
from anthropic import Anthropic

# --- Configuration de la page ---
st.set_page_config(page_title="Simulation Dispense", layout="wide", initial_sidebar_state="expanded")

# --- Dictionnaire de Traduction UI ---
TRANSLATIONS = {
    "fr": {
        "title": "Simulation de Dispense d'Encre Rhéofluidifiante",
        "sidebar_title": "Modélisation de la dispense d'encre",
        "nav_header": "Navigation",
        "gen_header": "Général",
        "models_header": "Résultats de modélisation",
        "annex_header": "Annexes",
        "gen_pages": ["Accueil", "Introduction", "Comparaison des modèles"],
        "model_pages": ["1. FEM / Phase-Field", "2. VOF (OpenFOAM)", "3. LBM (Palabos)", "4. SPH (PySPH)"],
        "annex_pages": ["Conclusion", "Équations clés", "Lexique", "Un peu d'histoire", "Bibliographie"],
        "tabs_fem": ["Physique", "Code", "Résultats de modélisation (GIF)", "Résultats de modélisation (PNG)"],
        "tabs_other": ["Physique", "Code", "Résultats de modélisation"],
        "overview_title": "Aperçu des résultats des 4 modèles de Simulation",
        "sim_1": "Simulation 1",
        "sim_2": "Simulation 2",
        "btn_launch": "LANCER LES SIMULATIONS",
        "btn_reset": "RÉINITIALISER",
        "btn_show": "AFFICHER LES IMAGES",
        "combo_unavailable": "Combinaison non disponible",
        "image_unavailable": "Image non disponible",
        "gif_viewer": "Visualisation dynamique (GIF)",
        "png_viewer": "Visualisation état final (PNG)",
        "lbl_avail_sims": "📋 Simulations disponibles",
        # Titres Modèles
        "title_model_1": "Modèle 1 : FEM / Phase-Field (Python)",
        "title_model_2": "Modèle 2 : VOF (OpenFOAM)",
        "title_model_3": "Modèle 3 : LBM (Palabos C++)",
        "title_model_4": "Modèle 4 : SPH (PySPH Python)",
        # Labels GIF
        "lbl_well": "Ø Puit (µm)",
        "lbl_nozzle": "Ø Buse (µm)",
        "lbl_shift_x": "Décalage X (µm)",
        "lbl_viscosity": "η₀ (Pa·s)",
        "lbl_ca_wall": "θ paroi (°)",
        "lbl_ca_gold": "θ substrat (°)",
        # Labels PNG
        "lbl_time": "Temps (ms)",
        "lbl_shift_z": "Décalage Z (µm)",
        "lbl_ratio": "Ratio buse/puit",
        "version_info": """**Version 0.5.0** ***(not released)***

Jan 2025 - *EQU*

**Nouveautés :**
- Support bilingue FR/EN
- Bibliographie
- Style académique
- Navigation améliorée""",
        "caption_fem": "Méthode des éléments finis - Python/FEniCS",
        "caption_vof": "Volume of Fluid - C++/OpenFOAM",
        "caption_lbm": "Lattice Boltzmann - C++/Palabos",
        "caption_sph": "Smoothed Particle Hydrodynamics - Python/PySPH",
        # Chatbot
        "chat_title": "Assistant IA",
        "chat_welcome": "Bonjour ! Je suis votre assistant pour comprendre les simulations de dispense d'encre rhéofluidifiante. Posez-moi vos questions sur FEM, VOF, LBM, SPH, ou la physique des fluides !",
        "chat_placeholder": "Posez votre question...",
        "chat_error": "Erreur de connexion à l'API. Vérifiez votre clé API.",
        "chat_close": "Fermer",
        "chat_clear": "Effacer",
        "chat_api_missing": "⚠️ Clé API manquante. Configurez ANTHROPIC_API_KEY.",
        "chat_toggle": "Assistant IA",
    },
    "en": {
        "title": "Shear-Thinning Ink Dispensing Simulation",
        "sidebar_title": "Ink Dispensing Modeling",
        "nav_header": "Navigation",
        "gen_header": "General",
        "models_header": "Modeling Results",
        "annex_header": "Appendices",
        "gen_pages": ["Home", "Introduction", "Model Comparison"],
        "model_pages": ["1. FEM / Phase-Field", "2. VOF (OpenFOAM)", "3. LBM (Palabos)", "4. SPH (PySPH)"],
        "annex_pages": ["Conclusion", "Key Equations", "Glossary", "A Bit of History", "Bibliography"],
        "tabs_fem": ["Physics", "Code", "Modeling Results (GIF)", "Modeling Results (PNG)"],
        "tabs_other": ["Physics", "Code", "Modeling Results"],
        "overview_title": "Overview of 4 Simulation Models Results",
        "sim_1": "Simulation 1",
        "sim_2": "Simulation 2",
        "btn_launch": "LAUNCH SIMULATIONS",
        "btn_reset": "RESET",
        "btn_show": "SHOW IMAGES",
        "combo_unavailable": "Combination not available",
        "image_unavailable": "Image not available",
        "gif_viewer": "Dynamic Visualization (GIF)",
        "png_viewer": "Final State Visualization (PNG)",
        "lbl_avail_sims": "📋 Available Simulations",
        # Model Titles
        "title_model_1": "Model 1 : FEM / Phase-Field (Python)",
        "title_model_2": "Model 2 : VOF (OpenFOAM)",
        "title_model_3": "Model 3 : LBM (Palabos C++)",
        "title_model_4": "Model 4 : SPH (PySPH Python)",
        # Labels GIF
        "lbl_well": "Ø Well (µm)",
        "lbl_nozzle": "Ø Nozzle (µm)",
        "lbl_shift_x": "Offset X (µm)",
        "lbl_viscosity": "η₀ (Pa·s)",
        "lbl_ca_wall": "θ wall (°)",
        "lbl_ca_gold": "θ substrate (°)",
        # Labels PNG
        "lbl_time": "Time (ms)",
        "lbl_shift_z": "Offset Z (µm)",
        "lbl_ratio": "Nozzle/well ratio",
        "version_info": """**Version 0.5.0** ***(not released)***

Jan 2025 - *EQU*

**New Features:**
- Bilingual support FR/EN
- Bibliography
- Academic style
- Improved navigation""",
        "caption_fem": "Finite Element Method - Python/FEniCS",
        "caption_vof": "Volume of Fluid - C++/OpenFOAM",
        "caption_lbm": "Lattice Boltzmann - C++/Palabos",
        "caption_sph": "Smoothed Particle Hydrodynamics - Python/PySPH",
        # Chatbot
        "chat_title": "AI Assistant",
        "chat_welcome": "Hello! I'm your assistant to help you understand shear-thinning ink dispensing simulations. Ask me about FEM, VOF, LBM, SPH, or fluid physics!",
        "chat_placeholder": "Ask your question...",
        "chat_error": "API connection error. Check your API key.",
        "chat_close": "Close",
        "chat_clear": "Clear",
        "chat_api_missing": "⚠️ API key missing. Configure ANTHROPIC_API_KEY.",
        "chat_toggle": "AI Assistant",
    }
}

# --- Fonctions de Langue ---
def get_language():
    if 'lang' not in st.session_state:
        st.session_state.lang = 'fr'
    return st.session_state.lang

def t(key):
    """Retourne la traduction pour la clé donnée."""
    lang = get_language()
    return TRANSLATIONS[lang].get(key, key)

# --- Styles CSS personnalisés (Style Académique) ---
custom_css = """
<style>
/* Masquer éléments Streamlit (sauf toolbar pour bouton sidebar) */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

/* Style académique */
.main {
    font-family: 'Georgia', 'Times New Roman', serif;
}
h1, h2, h3 {
    color: #004b87;
}

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
    background-color: #004b87;
    color: white;
}

/* Boutons de navigation - SVG flèche blanche sur fond bleu */
.nav-button {
    position: fixed;
    right: 30px;
    z-index: 9999;
    background-color: #004b87;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    transition: all 0.2s ease;
}
.nav-button:hover {
    background-color: #003366;
    transform: scale(1.1);
}
.back-to-top {
    bottom: calc(50% + 30px);
}
.scroll-to-bottom {
    bottom: calc(50% - 30px);
}

/* Bouton chatbot flottant */
.chat-toggle-btn {
    bottom: calc(50% - 90px);
    background-color: #28a745;
}
.chat-toggle-btn:hover {
    background-color: #218838;
}

/* Style du popover chatbot */
[data-testid="stPopover"] {
    max-width: 500px !important;
}
[data-testid="stPopover"] > div {
    padding: 0 !important;
}

/* Messages du chat */
.chat-container {
    max-height: 400px;
    overflow-y: auto;
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 8px;
    margin-bottom: 10px;
}

/* Espacement des radio buttons dans la sidebar */
[data-testid="stSidebar"] .stRadio > div {
    gap: 6px;
}

/* Améliorer la visibilité des radio buttons */
[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
    border: 2px solid #666;
}

/* Réduire l'espace des séparateurs dans la sidebar */
[data-testid="stSidebar"] hr {
    margin: 4px 0;
}

/* Réduire l'espace sous les subheaders de la sidebar */
[data-testid="stSidebar"] [data-testid="stSubheader"] {
    margin-bottom: -10px;
}

/* Réduire l'espace des paragraphes markdown dans la sidebar */
[data-testid="stSidebar"] [data-testid="stMarkdown"] p {
    margin-bottom: 0.3rem;
}

/* Réduire l'espace des listes dans la sidebar */
[data-testid="stSidebar"] [data-testid="stMarkdown"] ul {
    margin-top: 0;
    margin-bottom: 0.3rem;
}

/* Style spécifique pour le bouton du popover Chatbot dans la sidebar */
[data-testid="stSidebar"] [data-testid="stPopover"] > button {
    background-color: #004b87;
    color: white;
    border: none;
    font-weight: bold;
}
[data-testid="stSidebar"] [data-testid="stPopover"] > button:hover {
    background-color: #003366;
    color: white;
}
[data-testid="stSidebar"] [data-testid="stPopover"] > button:active {
    background-color: #002244;
    color: white;
}

/* Style "Rouge" pour le bouton Réinitialiser (hack CSS basé sur l'ordre ou le texte si possible) 
   Note: Cibler par texte est difficile en CSS pur sans structure stable. 
   On utilise une classe générique pour les boutons secondaires ici. 
   Pour un vrai bouton rouge, on compte sur le fait qu'il est "Secondary" et on le laisse gris/blanc 
   pour contraster avec le bleu "Primary". */

</style>

<!-- Bouton retour en haut - SVG avec flèche vers le haut -->
<a href="#top" class="nav-button back-to-top" title="Retour en haut / Back to top">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M12 4l-8 8h5v8h6v-8h5z"/>
    </svg>
</a>
<!-- Bouton descendre en bas - SVG avec flèche vers le bas -->
<a href="#bottom" class="nav-button scroll-to-bottom" title="Aller en bas / Go to bottom">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M12 20l8-8h-5V4h-6v8H4z"/>
    </svg>
</a>
<div id="top"></div>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Chemins Absolus Robustes (Compatible Cloud) ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DOC_PATH = os.path.join(ROOT_DIR, "docs")
DATA_PATH = os.path.join(ROOT_DIR, "data")
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")

# Chemins vers les codes sources (dans fr/ car identiques)
LBM_SRC = os.path.join(DOC_PATH, "fr/code/code_lbm.cpp")
SPH_SRC = os.path.join(DOC_PATH, "fr/code/code_sph.py")

# Chemins vers les exemples visuels
FEM_GIF_EX = os.path.join(ASSETS_PATH, "fem/gif/gif_a01.gif")
VOF_GIF_EX = os.path.join(ASSETS_PATH, "vof/gif/animation_vof_93.gif")
LBM_GIF_EX = os.path.join(ASSETS_PATH, "lbm/gif/lbm_029.gif")
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

def load_file_content(relative_path):
    """Charge un fichier depuis docs/<lang>/relative_path"""
    lang = get_language()
    full_path = os.path.join(DOC_PATH, lang, relative_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as f: return f.read()
    except Exception:
        return f"Document not found / Document non trouvé : {os.path.join(lang, relative_path)}"

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
    elif "```cpp" in content:
        parts = content.split("```cpp")
        for i, part in enumerate(parts):
            if i > 0:
                if "```" in part:
                    code, text = part.split("```", 1)
                    st.code(code.strip(), language='cpp', line_numbers=False)
                    if text.strip(): st.markdown(text)
                else:
                    st.code(part.strip(), language='cpp', line_numbers=False)
            elif part.strip():
                st.markdown(part)
    else:
        st.markdown(content)

# --- Callbacks pour Navigation ---
def on_change_gen():
    st.session_state.nav_model = None
    st.session_state.nav_annex = None

def on_change_model():
    st.session_state.nav_gen = None
    st.session_state.nav_annex = None

def on_change_annex():
    st.session_state.nav_gen = None
    st.session_state.nav_model = None

# --- Initialisation des États ---
if 'nav_gen' not in st.session_state: st.session_state.nav_gen = t("gen_pages")[0]
if 'nav_model' not in st.session_state: st.session_state.nav_model = None
if 'nav_annex' not in st.session_state: st.session_state.nav_annex = None

# --- Barre Latérale ---

# Sélecteur de langue avec conservation de la page
old_lang = st.session_state.get('lang', 'fr')
lang_selection = st.sidebar.radio(
    "Language",
    ["🇫🇷 FR", "🇬🇧 EN"],
    horizontal=True,
    label_visibility="collapsed",
    index=0 if old_lang == "fr" else 1
)
new_lang = "fr" if "FR" in lang_selection else "en"

# Si la langue change, convertir la sélection actuelle
if new_lang != old_lang:
    # Trouver l'index de la page actuelle dans l'ancienne langue
    old_gen_pages = TRANSLATIONS[old_lang]["gen_pages"]
    old_model_pages = TRANSLATIONS[old_lang]["model_pages"]
    old_annex_pages = TRANSLATIONS[old_lang]["annex_pages"]
    new_gen_pages = TRANSLATIONS[new_lang]["gen_pages"]
    new_model_pages = TRANSLATIONS[new_lang]["model_pages"]
    new_annex_pages = TRANSLATIONS[new_lang]["annex_pages"]

    if st.session_state.nav_gen and st.session_state.nav_gen in old_gen_pages:
        idx = old_gen_pages.index(st.session_state.nav_gen)
        st.session_state.nav_gen = new_gen_pages[idx]
    elif st.session_state.nav_model and st.session_state.nav_model in old_model_pages:
        idx = old_model_pages.index(st.session_state.nav_model)
        st.session_state.nav_model = new_model_pages[idx]
    elif st.session_state.nav_annex and st.session_state.nav_annex in old_annex_pages:
        idx = old_annex_pages.index(st.session_state.nav_annex)
        st.session_state.nav_annex = new_annex_pages[idx]
    else:
        # Par défaut, sélectionner Accueil/Home
        st.session_state.nav_gen = new_gen_pages[0]
        st.session_state.nav_model = None
        st.session_state.nav_annex = None

    st.session_state.lang = new_lang
    st.rerun()

st.session_state.lang = new_lang

st.sidebar.title(t("sidebar_title"))
st.sidebar.markdown("---")

# Navigation par groupes avec callbacks (style electrochemistry)
st.sidebar.subheader(t("gen_header"))
nav_gen = st.sidebar.radio(
    "Nav Gen",
    t("gen_pages"),
    key="nav_gen",
    on_change=on_change_gen,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.subheader(t("models_header"))
nav_model = st.sidebar.radio(
    "Nav Models",
    t("model_pages"),
    key="nav_model",
    index=None,
    on_change=on_change_model,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.subheader(t("annex_header"))
nav_annex = st.sidebar.radio(
    "Nav Annex",
    t("annex_pages"),
    key="nav_annex",
    index=None,
    on_change=on_change_annex,
    label_visibility="collapsed"
)

# --- Chatbot dans la Sidebar (avec toggle ON/OFF) ---

def is_chatbot_enabled():
    """Vérifie si le chatbot doit être affiché."""
    # 1. Vérifier si la clé API existe
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
        except Exception:
            pass
    if not api_key:
        return False  # Pas de clé = pas de chatbot

    # 2. Vérifier si explicitement désactivé dans secrets
    try:
        enabled = st.secrets.get("CHATBOT_ENABLED", True)
        if isinstance(enabled, str):
            enabled = enabled.lower() in ("true", "1", "yes", "oui")
        return enabled
    except Exception:
        return True  # Par défaut activé si clé présente

# System prompt contextuel pour l'assistant (défini hors du if)
SYSTEM_PROMPT = """Tu es un assistant expert en simulation numérique de la dispense d'encre rhéofluidifiante dans des micro-puits.

Tu connais parfaitement les 4 méthodes numériques comparées dans cette application :
1. **FEM / Phase-Field** (FEniCS/Python) : Méthode des éléments finis avec approche champ de phase pour le suivi d'interface diffuse
2. **VOF** (OpenFOAM/C++) : Volume of Fluid avec suivi d'interface nette (α ∈ [0,1])
3. **LBM** (Palabos/C++) : Lattice Boltzmann avec modèle Shan-Chen pour le multiphasique
4. **SPH** (PySPH/Python) : Smoothed Particle Hydrodynamics, méthode particulaire lagrangienne

Tu maîtrises :
- La rhéologie des fluides non-newtoniens (modèle Carreau pour les encres rhéofluidifiantes)
- Les phénomènes capillaires (tension de surface σ, angles de contact θ)
- Les nombres adimensionnels (Reynolds Re, Capillaire Ca, Weber We, Ohnesorge Oh)
- Les équations de Navier-Stokes incompressibles
- Les conditions aux limites (mouillabilité, non-glissement)

Réponds de manière concise, pédagogique et scientifiquement rigoureuse.
Utilise des équations LaTeX quand c'est pertinent (format $equation$ pour inline).
Si tu ne connais pas la réponse, dis-le honnêtement.
Réponds dans la langue de l'utilisateur (français ou anglais).
"""

def get_anthropic_client():
    """Retourne le client Anthropic si la clé API est disponible."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
        except Exception:
            pass
    if api_key:
        return Anthropic(api_key=api_key)
    return None

def stream_claude_response(user_message: str):
    """Génère la réponse de Claude en streaming (mot par mot)."""
    client = get_anthropic_client()
    if not client:
        yield t("chat_api_missing")
        return

    st.session_state.chat_messages.append({"role": "user", "content": user_message})

    try:
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=st.session_state.chat_messages
        ) as stream:
            full_response = ""
            for text in stream.text_stream:
                full_response += text
                yield text

            # Sauvegarder la réponse complète dans l'historique
            st.session_state.chat_messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        error_msg = f"{t('chat_error')} ({str(e)[:50]}...)"
        yield error_msg

# Initialiser l'historique du chat
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Interface chatbot dans la sidebar (seulement si activé)
if is_chatbot_enabled():
    st.sidebar.markdown("---")
    with st.sidebar.popover(f"{t('chat_title')}", use_container_width=True):
        # Bouton effacer
        if st.button(t("chat_clear"), use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

        st.markdown("---")

        # Message de bienvenue
        if not st.session_state.chat_messages:
            st.info(t("chat_welcome"))

        # Historique des messages
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Zone de saisie
        if prompt := st.chat_input(t("chat_placeholder")):
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                # Streaming : affichage progressif mot par mot !
                st.write_stream(stream_claude_response(prompt))

st.sidebar.markdown("---")
st.sidebar.markdown(t("version_info"))

# --- Déterminer la page active ---
selected_page = None
if nav_model:
    selected_page = nav_model
elif nav_annex:
    selected_page = nav_annex
elif nav_gen:
    selected_page = nav_gen
else:
    selected_page = t("gen_pages")[0]  # Default: Accueil/Home

# --- Pages ---

# Mapping pour les pages (indépendant de la langue)
gen_pages = t("gen_pages")
model_pages = t("model_pages")
annex_pages = t("annex_pages")

# ===== PAGE ACCUEIL =====
if selected_page == gen_pages[0]:  # Accueil / Home
    st.title(t("title"))
    st.markdown(load_file_content("accueil/accueil.md"))

    st.markdown("---")
    st.subheader(t("overview_title"))

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.markdown("#### 1. FEM / Phase-Field")
        if os.path.exists(FEM_GIF_EX):
            st.image(FEM_GIF_EX, use_container_width=True)
        st.caption(t("caption_fem"))

    with col2:
        st.markdown("#### 2. VOF (OpenFOAM)")
        if os.path.exists(VOF_GIF_EX):
            st.image(VOF_GIF_EX, use_container_width=True)
        st.caption(t("caption_vof"))

    with col3:
        st.markdown("#### 3. LBM (Palabos)")
        if os.path.exists(LBM_GIF_EX):
            st.image(LBM_GIF_EX, use_container_width=True)
        st.caption(t("caption_lbm"))

    with col4:
        st.markdown("#### 4. SPH (PySPH)")
        if os.path.exists(SPH_GIF_EX):
            st.image(SPH_GIF_EX, use_container_width=True)
        st.caption(t("caption_sph"))

# ===== PAGE INTRODUCTION =====
elif selected_page == gen_pages[1]:  # Introduction
    st.title(f"Introduction")
    st.markdown("---")
    st.markdown(load_file_content("intro/intro_project.md"))

# ===== PAGE COMPARAISON =====
elif selected_page == gen_pages[2]:  # Comparaison des modèles
    st.title(selected_page)
    st.markdown("---")
    st.markdown(load_file_content("comparaison/comparaison_models.md"))

# ===== PAGE FEM =====
elif selected_page == model_pages[0]:  # FEM
    st.title(t("title_model_1"))
    tabs = st.tabs(t("tabs_fem"))

    with tabs[0]:  # Physique
        display_smart_markdown(load_file_content("physics/physics_fem.md"))

    with tabs[1]:  # Code
        display_smart_markdown(load_file_content("code/code_fem.md"))

    with tabs[2]:  # GIF
        # Layout Titre + Popover
        c_title, c_pop = st.columns([0.7, 0.3])
        with c_title:
            st.subheader(t("gif_viewer"))
        with c_pop:
            # Popover pour voir les simulations disponibles sans scroller
            with st.popover(t("lbl_avail_sims"), use_container_width=True):
                try:
                    df_mapping = pd.read_csv(os.path.join(DATA_PATH, 'fem_gif_mapping.csv'), sep=';', encoding='utf-8')
                    st.dataframe(df_mapping, use_container_width=True, hide_index=True)
                except Exception:
                    st.error("Données non trouvées")

        # Zone de sélection des paramètres (colonnes réduites avec espaceurs)
        with st.container(border=True):
            st.markdown(f"**{t('sim_1')}**")
            _, c1, c2, c3, c4, c5, c6, _ = st.columns([0.5, 1, 1, 1, 1, 1, 1, 0.5])
            with c1: g1_d = st.selectbox(t("lbl_well"), [800,1000,1500], key="g1_d")
            with c2: g1_b = st.selectbox(t("lbl_nozzle"), [200,250,300], key="g1_b")
            with c3: g1_s = st.selectbox(t("lbl_shift_x"), [0,-75,-150], key="g1_s")
            with c4: g1_v = st.selectbox(t("lbl_viscosity"), [5.0,1.5], key="g1_v")
            with c5: g1_a = st.selectbox(t("lbl_ca_wall"), [90,35], key="g1_a")
            with c6: g1_o = st.selectbox(t("lbl_ca_gold"), [35,75], key="g1_o")
            p1 = (g1_d, g1_b, g1_s, g1_v, g1_a, g1_o)

            st.markdown(f"**{t('sim_2')}**")
            _, c1, c2, c3, c4, c5, c6, _ = st.columns([0.5, 1, 1, 1, 1, 1, 1, 0.5])
            with c1: g2_d = st.selectbox(t("lbl_well"), [800,1000,1500], key="g2_d", index=1)
            with c2: g2_b = st.selectbox(t("lbl_nozzle"), [200,250,300], key="g2_b", index=1)
            with c3: g2_s = st.selectbox(t("lbl_shift_x"), [0,-75,-150], key="g2_s", index=1)
            with c4: g2_v = st.selectbox(t("lbl_viscosity"), [5.0,1.5], key="g2_v", index=1)
            with c5: g2_a = st.selectbox(t("lbl_ca_wall"), [90,35], key="g2_a", index=1)
            with c6: g2_o = st.selectbox(t("lbl_ca_gold"), [35,75], key="g2_o", index=1)
            p2 = (g2_d, g2_b, g2_s, g2_v, g2_a, g2_o)

            # Boutons Lancer (Bleu) et Réinitialiser (Rouge/Gris)
            _, btn_col1, btn_col2, _ = st.columns([1, 1, 1, 1])
            with btn_col1:
                if st.button(t("btn_launch"), type="primary", use_container_width=True, key="btn_gif_launch"):
                    st.session_state.run_g = True
                    st.session_state.p_g = (p1, p2)
            with btn_col2:
                if st.button(t("btn_reset"), type="secondary", use_container_width=True, key="btn_gif_reset"):
                    st.session_state.run_g = False
                    st.rerun()

        # Zone d'affichage des résultats
        if st.session_state.get('run_g', False):
            with st.container(border=True):
                gif_cols = st.columns(2)
                m = load_gif_mapping()
                for i, (col, params) in enumerate(zip(gif_cols, st.session_state.p_g)):
                    with col:
                        st.subheader(f"{t('sim_1') if i==0 else t('sim_2')}")
                        if params in m:
                            st.markdown(load_media_as_base64(m[params]), unsafe_allow_html=True)
                        else:
                            st.warning(t("combo_unavailable"))

    with tabs[3]:  # PNG
        # Layout Titre + Popover
        c_title, c_pop = st.columns([0.7, 0.3])
        with c_title:
            st.subheader(t("png_viewer"))
        with c_pop:
            # Popover pour voir les simulations disponibles sans scroller
            with st.popover(t("lbl_avail_sims"), use_container_width=True):
                try:
                    df_mapping = pd.read_csv(os.path.join(DATA_PATH, 'fem_png_mapping.csv'), sep=';', encoding='utf-8')
                    st.dataframe(df_mapping, use_container_width=True, hide_index=True)
                except Exception:
                    st.error("Données non trouvées")

        # Zone de sélection des paramètres (colonnes réduites avec espaceurs)
        with st.container(border=True):
            st.markdown(f"**{t('sim_1')}**")
            _, c1, c2, c3, c4, c5, c6, _ = st.columns([0.5, 1, 1, 1, 1, 1, 1, 0.5])
            with c1: p1_t = st.selectbox(t("lbl_time"), [20,40], key="p1_t")
            with c2: p1_v = st.selectbox(t("lbl_viscosity"), [0.05,0.5,1.5,5.0], index=2, key="p1_v")
            with c3: p1_x = st.selectbox(t("lbl_shift_x"), [0,-75], key="p1_x")
            with c4: p1_z = st.selectbox(t("lbl_shift_z"), [0,-30], key="p1_z")
            with c5: p1_a = st.selectbox(t("lbl_ca_gold"), [15,35,75], key="p1_a")
            with c6: p1_r = st.selectbox(t("lbl_ratio"), [0.6,0.8], key="p1_r")
            png1 = (p1_t, p1_v, p1_x, p1_z, p1_a, p1_r)

            st.markdown(f"**{t('sim_2')}**")
            _, c1, c2, c3, c4, c5, c6, _ = st.columns([0.5, 1, 1, 1, 1, 1, 1, 0.5])
            with c1: p2_t = st.selectbox(t("lbl_time"), [20,40], key="p2_t", index=1)
            with c2: p2_v = st.selectbox(t("lbl_viscosity"), [0.05,0.5,1.5,5.0], index=3, key="p2_v")
            with c3: p2_x = st.selectbox(t("lbl_shift_x"), [0,-75], key="p2_x", index=1)
            with c4: p2_z = st.selectbox(t("lbl_shift_z"), [0,-30], key="p2_z", index=1)
            with c5: p2_a = st.selectbox(t("lbl_ca_gold"), [15,35,75], index=1, key="p2_a")
            with c6: p2_r = st.selectbox(t("lbl_ratio"), [0.6,0.8], index=1, key="p2_r")
            png2 = (p2_t, p2_v, p2_x, p2_z, p2_a, p2_r)

            # Boutons Afficher (Bleu) et Réinitialiser (Rouge/Gris)
            _, btn_col1, btn_col2, _ = st.columns([1, 1, 1, 1])
            with btn_col1:
                if st.button(t("btn_show"), type="primary", use_container_width=True, key="btn_png_launch"):
                    st.session_state.run_p = True
                    st.session_state.p_p = (png1, png2)
            with btn_col2:
                if st.button(t("btn_reset"), type="secondary", use_container_width=True, key="btn_png_reset"):
                    st.session_state.run_p = False
                    st.rerun()

        # Zone d'affichage des résultats
        if st.session_state.get('run_p', False):
            with st.container(border=True):
                png_cols = st.columns(2)
                m = load_png_mapping()
                for i, (col, params) in enumerate(zip(png_cols, st.session_state.p_p)):
                    with col:
                        st.subheader(f"{t('sim_1') if i==0 else t('sim_2')}")
                        if params in m:
                            st.markdown(load_media_as_base64(m[params]), unsafe_allow_html=True)
                        else:
                            st.warning(t("image_unavailable"))

# ===== PAGE VOF =====
elif selected_page == model_pages[1]:  # VOF
    st.title(t("title_model_2"))
    tabs = st.tabs(t("tabs_other"))

    with tabs[0]:
        st.markdown(load_file_content("physics/physics_vof.md"))

    with tabs[1]:
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

    with tabs[2]:
        st.subheader("Exemple de Simulation VOF")
        if os.path.exists(VOF_GIF_EX):
            st.image(VOF_GIF_EX, caption="Simulation VOF - Cas 93", use_container_width=True)

# ===== PAGE LBM =====
elif selected_page == model_pages[2]:  # LBM
    st.title(t("title_model_3"))
    tabs = st.tabs(t("tabs_other"))

    with tabs[0]:
        st.markdown(load_file_content("physics/physics_lbm.md"))

    with tabs[1]:
        st.subheader("Code Source Palabos")
        st.code(load_file_content(os.path.join(DOC_PATH, "fr/code/code_lbm.cpp")), language='cpp')

    with tabs[2]:
        st.subheader("Exemple de Simulation LBM")
        if os.path.exists(LBM_GIF_EX):
            st.image(LBM_GIF_EX, caption="Simulation LBM - Cas 29", use_container_width=True)

# ===== PAGE SPH =====
elif selected_page == model_pages[3]:  # SPH
    st.title(t("title_model_4"))
    tabs = st.tabs(t("tabs_other"))

    with tabs[0]:
        st.markdown(load_file_content("physics/physics_sph.md"))

    with tabs[1]:
        st.subheader("Code Source PySPH")
        st.code(load_file_content(os.path.join(DOC_PATH, "fr/code/code_sph.py")), language='python')

    with tabs[2]:
        st.subheader("Exemple de Simulation SPH")
        if os.path.exists(SPH_GIF_EX):
            st.image(SPH_GIF_EX, caption="Simulation SPH - Cas 03", use_container_width=True)

# ===== PAGE CONCLUSION =====
elif selected_page == annex_pages[0]:  # Conclusion
    st.title("Conclusion")
    st.markdown("---")
    st.markdown(load_file_content("conclusion/conclusion.md"))

# ===== PAGE ÉQUATIONS CLÉS =====
elif selected_page == annex_pages[1]:  # Équations clés / Key Equations
    st.title(selected_page)
    st.markdown("---")
    st.markdown(load_file_content("equations/equations_clef.md"))

# ===== PAGE LEXIQUE =====
elif selected_page == annex_pages[2]:  # Lexique / Glossary
    st.title(selected_page)
    st.markdown("---")
    st.markdown(load_file_content("lexique/lexique.md"))

# ===== PAGE HISTOIRE =====
elif selected_page == annex_pages[3]:  # Un peu d'histoire / A Bit of History
    st.title(selected_page)
    st.markdown("---")
    st.markdown(load_file_content("histoire/histoire.md"))

# ===== PAGE BIBLIOGRAPHIE =====
elif selected_page == annex_pages[4]:  # Bibliographie / Bibliography
    st.title(selected_page)
    st.markdown("---")
    st.markdown(load_file_content("biblio/biblio.md"))

# --- Ancre de fin de page pour bouton scroll-to-bottom ---
st.markdown('<div id="bottom"></div>', unsafe_allow_html=True)