import streamlit as st
import base64
from pathlib import Path
import os
import pandas as pd

st.set_page_config(
    page_title="Dispense d'encre",
    page_icon="💧",
    layout="wide"
)

def load_gif_mapping():
    """
    Charge le mapping des combinaisons de paramètres vers les fichiers GIF depuis le CSV.
    """
    try:
        df = pd.read_csv('gif_mapping.csv', sep=';', encoding='utf-8')
        # Créer un dictionnaire avec les paramètres comme clé et le nom du fichier GIF comme valeur
        mapping = {}
        for _, row in df.iterrows():
            # Clé : tuple (diamètre_puit, diamètre_buse, shift_x, viscosité, angle_contact_paroi, angle_contact_or)
            key = (
                int(row['diamètre du puit (µm)']),
                int(row['diamètre de la buse (µm)']),
                int(row['shift buse en x (µm)']),
                float(str(row['Viscosité de l\'encre (Pa.s)']).replace(',', '.')),
                int(row['CA wall right']),
                int(row['CA gold'])
            )
            # Valeur : chemin complet du fichier GIF
            mapping[key] = f"gif/{row['nom fichier gif']}"
        return mapping
    except Exception as e:
        st.error(f"Erreur lors du chargement du mapping: {str(e)}")
        return {}

def load_gif(gif_path):
    """Charge et encode un GIF en base64 pour l'affichage HTML."""
    try:
        with open(gif_path, "rb") as file:
            contents = file.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        return f'<img src="data:image/gif;base64,{data_url}" style="width:100%; max-width:600px;">'
    except FileNotFoundError:
        return None

def hide_streamlit_branding():
    """Injecte CSS pour masquer tous les éléments Streamlit indésirables"""
    hide_streamlit_style = """
    <style>
    /* Masquer le menu hamburger */
    #MainMenu {visibility: hidden;}

    /* Masquer le footer "Made with Streamlit" */
    footer {visibility: hidden;}

    /* Masquer le header avec les liens GitHub */
    header {visibility: hidden;}

    /* Masquer le bouton de déploiement */
    .stDeployButton {display: none;}

    /* Masquer la toolbar */
    .stToolbar {display: none;}

    /* Masquer le viewer badge */
    ._container_badge {display: none;}

    /* Masquer tous les liens vers GitHub */
    [href*="github"] {display: none;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def load_markdown_file(filepath):
    """Charge le contenu d'un fichier markdown."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"⚠️ Fichier non trouvé: {filepath}"
    except Exception as e:
        return f"⚠️ Erreur lors de la lecture du fichier: {str(e)}"

def simulation_page():
    hide_streamlit_branding()

    st.title("💧 Simulation de dispense d'encre")
    st.markdown("### Comparez jusqu'à 2 simulations simultanément")
    st.markdown("---")

    # Créer deux colonnes pour les simulations
    sim1, sim2 = st.columns(2)

    with sim1:
        st.subheader("📊 Simulation 1")

        with st.expander("Paramètres", expanded=True):
            # Diviser en 3 colonnes pour les paramètres
            col1_1, col1_2, col1_3 = st.columns(3)

            with col1_1:
                diametre_puit_1 = st.selectbox(
                    "Diamètre puit (µm)",
                    options=[800, 1000, 1500],
                    key="diam_puit_1"
                )

                diametre_buse_1 = st.selectbox(
                    "Diamètre buse (µm)",
                    options=[200, 250, 300],
                    key="diam_buse_1"
                )

            with col1_2:
                shift_buse_x_1 = st.selectbox(
                    "Shift X (µm)",
                    options=[0, -75, -150],
                    key="shift_x_1"
                )

                viscosite_encre_1 = st.selectbox(
                    "Viscosité (Pa.s)",
                    options=[1.5, 5.0],
                    key="visc_1"
                )

            with col1_3:
                angle_contact_1 = st.selectbox(
                    "Angle contact paroi droite (°)",
                    options=[35, 90],
                    key="angle_1"
                )

                angle_or_1 = st.selectbox(
                    "Angle contact or (°)",
                    options=[35, 75],
                    key="angle_or_1"
                )

            if st.button("🚀 Lancer", key="btn_sim1", type="primary", use_container_width=True):
                st.session_state.sim1_running = True
                st.session_state.sim1_params = (
                    diametre_puit_1, diametre_buse_1, shift_buse_x_1, viscosite_encre_1, angle_contact_1, angle_or_1
                )

        # Affichage du résultat de la simulation 1
        if 'sim1_running' in st.session_state and st.session_state.sim1_running:
            params = st.session_state.sim1_params
            gif_mapping = load_gif_mapping()

            if params in gif_mapping:
                gif_file = gif_mapping[params]
                gif_html = load_gif(gif_file)

                if gif_html:
                    st.markdown(gif_html, unsafe_allow_html=True)
                    st.caption(f"Puit: {params[0]}µm | Buse: {params[1]}µm | Shift X: {params[2]}µm | Viscosité: {params[3]} Pa.s | Angle paroi: {params[4]}° | Angle or: {params[5]}°")
                else:
                    st.error(f"Fichier GIF non trouvé: {gif_file}")
            else:
                st.warning(f"Aucune simulation disponible pour ces paramètres: Puit={params[0]}µm, Buse={params[1]}µm, Shift={params[2]}µm, Viscosité={params[3]}Pa.s")
        else:
            st.info("Sélectionnez les paramètres et lancez la simulation")

    with sim2:
        st.subheader("📊 Simulation 2")

        with st.expander("Paramètres", expanded=True):
            # Diviser en 3 colonnes pour les paramètres
            col2_1, col2_2, col2_3 = st.columns(3)

            with col2_1:
                diametre_puit_2 = st.selectbox(
                    "Diamètre puit (µm)",
                    options=[800, 1000, 1500],
                    key="diam_puit_2"
                )

                diametre_buse_2 = st.selectbox(
                    "Diamètre buse (µm)",
                    options=[200, 250, 300],
                    key="diam_buse_2"
                )

            with col2_2:
                shift_buse_x_2 = st.selectbox(
                    "Shift X (µm)",
                    options=[0, -75, -150],
                    key="shift_x_2"
                )

                viscosite_encre_2 = st.selectbox(
                    "Viscosité (Pa.s)",
                    options=[1.5, 5.0],
                    key="visc_2"
                )

            with col2_3:
                angle_contact_2 = st.selectbox(
                    "Angle contact paroi droite (°)",
                    options=[35, 90],
                    key="angle_2"
                )

                angle_or_2 = st.selectbox(
                    "Angle contact or (°)",
                    options=[35, 75],
                    key="angle_or_2"
                )

            if st.button("🚀 Lancer", key="btn_sim2", type="primary", use_container_width=True):
                st.session_state.sim2_running = True
                st.session_state.sim2_params = (
                    diametre_puit_2, diametre_buse_2, shift_buse_x_2, viscosite_encre_2, angle_contact_2, angle_or_2
                )

        # Affichage du résultat de la simulation 2
        if 'sim2_running' in st.session_state and st.session_state.sim2_running:
            params = st.session_state.sim2_params
            gif_mapping = load_gif_mapping()

            if params in gif_mapping:
                gif_file = gif_mapping[params]
                gif_html = load_gif(gif_file)

                if gif_html:
                    st.markdown(gif_html, unsafe_allow_html=True)
                    st.caption(f"Puit: {params[0]}µm | Buse: {params[1]}µm | Shift X: {params[2]}µm | Viscosité: {params[3]} Pa.s | Angle paroi: {params[4]}° | Angle or: {params[5]}°")
                else:
                    st.error(f"Fichier GIF non trouvé: {gif_file}")
            else:
                st.warning(f"Aucune simulation disponible pour ces paramètres: Puit={params[0]}µm, Buse={params[1]}µm, Shift={params[2]}µm, Viscosité={params[3]}Pa.s")
        else:
            st.info("Sélectionnez les paramètres et lancez la simulation")

    # Section informations
    st.markdown("---")
    with st.expander("ℹ️ Combinaisons disponibles"):
        st.markdown("""
        ### Paramètres disponibles:
        - **Diamètre du puit**: 800, 1000, 1500 µm
        - **Diamètre de la buse**: 200, 250, 300 µm
        - **Shift buse en X**: 0, -75, -150 µm
        - **Viscosité**: 1.5 Pa.s (série A: gif_a1-a27) ou 5.0 Pa.s (série B: gif_b1-b18)

        ### Total de simulations disponibles: 45 GIFs
        - Série A (viscosité 1.5 Pa.s): 27 simulations (gif_a1 à gif_a27)
        - Série B (viscosité 5.0 Pa.s): 18 simulations (gif_b1 à gif_b18)
        """)

        # Afficher le mapping actuel
        try:
            mapping = load_gif_mapping()
            st.markdown(f"**{len(mapping)} simulations chargées depuis gif_mapping.csv**")
        except:
            st.warning("Impossible de charger le mapping des simulations")

def physics_page():
    hide_streamlit_branding()
    st.title("📚 Physique de la dispense d'encre")
    st.markdown("---")

    # Charger le contenu depuis le fichier markdown
    physics_content = load_markdown_file("documentation/ink_dispensing_physique_v1.md")

    # Afficher le contenu
    st.markdown(physics_content)

def code_page():
    hide_streamlit_branding()
    st.title("💻 Code Python de simulation")
    st.markdown("---")

    # Charger le contenu depuis le fichier markdown
    code_content = load_markdown_file("documentation/ink_dispensing_code_v8.md")

    # Traiter le contenu pour extraire le code Python
    if "```python" in code_content:
        # Extraire les blocs de code Python
        parts = code_content.split("```python")

        for i, part in enumerate(parts):
            if i == 0:
                # Texte avant le premier bloc de code
                if part.strip():
                    st.markdown(part)
            else:
                # Séparer le code du texte qui suit
                if "```" in part:
                    code, text = part.split("```", 1)
                    # Afficher le code
                    st.code(code.strip(), language='python')
                    # Afficher le texte qui suit
                    if text.strip():
                        st.markdown(text)
                else:
                    # Cas où le bloc de code n'est pas fermé correctement
                    st.code(part.strip(), language='python')
    else:
        # Si pas de blocs de code Python, afficher tel quel
        st.markdown(code_content)

def main():
    # Masquer les éléments Streamlit dès le début
    hide_streamlit_branding()

    st.sidebar.title("🧭 Navigation")

    page = st.sidebar.radio(
        "Choisir une page",
        ["💧 Simulation", "📚 Physique", "💻 Code Python"],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")

    # Bouton pour réinitialiser toutes les simulations
    if st.sidebar.button("🔄 Réinitialiser les simulations", use_container_width=True):
        if 'sim1_running' in st.session_state:
            del st.session_state.sim1_running
        if 'sim2_running' in st.session_state:
            del st.session_state.sim2_running
        if 'sim1_params' in st.session_state:
            del st.session_state.sim1_params
        if 'sim2_params' in st.session_state:
            del st.session_state.sim2_params
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### À propos
    **Application de simulation de dispense d'encre.**
    """)
    st.sidebar.markdown("")  # Ligne vide pour espacer
    st.sidebar.markdown("**Version:** 2.0.0   - EQU - Sept-25")
    st.sidebar.markdown("")  # Ligne vide pour espacer
    st.sidebar.markdown("")  # Ligne vide pour espacer

    st.sidebar.markdown("""
    **Features:**
    - Comparaison de 2 simulations
    - Documentation intégrée
    - Code source disponible
    """)

    # Vérifier l'existence des dossiers requis
    if not os.path.exists("gif"):
        st.sidebar.error("⚠️ Dossier 'gif' non trouvé!")
    if not os.path.exists("documentation"):
        st.sidebar.error("⚠️ Dossier 'documentation' non trouvé!")

    if page == "💧 Simulation":
        simulation_page()
    elif page == "📚 Physique":
        physics_page()
    elif page == "💻 Code Python":
        code_page()

if __name__ == "__main__":
    main()