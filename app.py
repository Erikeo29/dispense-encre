import streamlit as st
import base64
from pathlib import Path
import os

st.set_page_config(
    page_title="Dispense d'encre",
    page_icon="💧",
    layout="wide"
)

def get_gif_mapping():
    """
    Mapping des combinaisons de paramètres vers les fichiers GIF.
    À adapter selon vos conventions de nommage.
    """
    return {
        (800, 0, 100, 10): "gif/gif_1.gif",
        (1000, 50, 150, 20): "gif/gif_2.gif",
        (1200, 100, 200, 30): "gif/gif_3.gif",
    }

def load_gif(gif_path):
    """Charge et encode un GIF en base64 pour l'affichage HTML."""
    try:
        with open(gif_path, "rb") as file:
            contents = file.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        return f'<img src="data:image/gif;base64,{data_url}" style="width:100%; max-width:600px;">'
    except FileNotFoundError:
        return None

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
    st.title("💧 Simulation de dispense d'encre")
    st.markdown("### Comparez jusqu'à 2 simulations simultanément")
    st.markdown("---")

    # Créer deux colonnes pour les simulations
    sim1, sim2 = st.columns(2)

    with sim1:
        st.subheader("📊 Simulation 1")

        with st.expander("Paramètres", expanded=True):
            # Diviser en 2 colonnes pour les paramètres
            col1_1, col1_2 = st.columns(2)

            with col1_1:
                st.markdown("**Paramètres principaux**")
                diametre_puit_1 = st.selectbox(
                    "Diamètre puit (µm)",
                    options=[800, 1000, 1200],
                    key="diam_puit_1"
                )

                diametre_buse_1 = st.selectbox(
                    "Diamètre buse (µm)",
                    options=[100, 150, 200],
                    key="diam_buse_1"
                )

                shift_buse_x_1 = st.selectbox(
                    "Shift X (µm)",
                    options=[0, 50, 100],
                    key="shift_x_1"
                )

                shift_buse_z_1 = st.selectbox(
                    "Shift Z (µm)",
                    options=[0, 10, 20],
                    key="shift_z_1"
                )

                viscosite_encre_1 = st.selectbox(
                    "Viscosité (Pa.s)",
                    options=[10.0, 20.0, 30.0],
                    key="visc_1"
                )

            with col1_2:
                st.markdown("**Angles de contact**")
                angle_paroi_gauche_1 = st.selectbox(
                    "Paroi gauche (°)",
                    options=[30, 45, 60, 90],
                    key="angle_pg_1"
                )

                angle_paroi_droite_1 = st.selectbox(
                    "Paroi droite (°)",
                    options=[30, 45, 60, 90],
                    key="angle_pd_1"
                )

                angle_eg_gauche_1 = st.selectbox(
                    "EG gauche (°)",
                    options=[30, 45, 60, 90],
                    key="angle_eg_1"
                )

                angle_or_1 = st.selectbox(
                    "Or (°)",
                    options=[30, 45, 60, 90],
                    key="angle_or_1"
                )

            if st.button("🚀 Lancer", key="btn_sim1", type="primary", use_container_width=True):
                st.session_state.sim1_running = True
                st.session_state.sim1_params = (
                    diametre_puit_1, shift_buse_x_1, diametre_buse_1, viscosite_encre_1
                )
                st.session_state.sim1_params_full = {
                    'shift_z': shift_buse_z_1,
                    'angle_paroi_gauche': angle_paroi_gauche_1,
                    'angle_paroi_droite': angle_paroi_droite_1,
                    'angle_eg_gauche': angle_eg_gauche_1,
                    'angle_or': angle_or_1
                }

        # Affichage du résultat de la simulation 1
        if 'sim1_running' in st.session_state and st.session_state.sim1_running:
            params = st.session_state.sim1_params
            gif_mapping = get_gif_mapping()

            if params in gif_mapping:
                gif_file = gif_mapping[params]
                gif_html = load_gif(gif_file)

                if gif_html:
                    st.markdown(gif_html, unsafe_allow_html=True)
                    st.caption(f"Puit: {params[0]}µm | Shift: {params[1]}µm | Buse: {params[2]}µm | Viscosité: {params[3]}mPa.s")
                else:
                    st.error(f"Fichier GIF non trouvé: {gif_file}")
            else:
                st.warning("Aucune simulation disponible pour ces paramètres")
        else:
            st.info("Sélectionnez les paramètres et lancez la simulation")

    with sim2:
        st.subheader("📊 Simulation 2")

        with st.expander("Paramètres", expanded=True):
            # Diviser en 2 colonnes pour les paramètres
            col2_1, col2_2 = st.columns(2)

            with col2_1:
                st.markdown("**Paramètres principaux**")
                diametre_puit_2 = st.selectbox(
                    "Diamètre puit (µm)",
                    options=[800, 1000, 1200],
                    key="diam_puit_2"
                )

                diametre_buse_2 = st.selectbox(
                    "Diamètre buse (µm)",
                    options=[100, 150, 200],
                    key="diam_buse_2"
                )

                shift_buse_x_2 = st.selectbox(
                    "Shift X (µm)",
                    options=[0, 50, 100],
                    key="shift_x_2"
                )

                shift_buse_z_2 = st.selectbox(
                    "Shift Z (µm)",
                    options=[0, 10, 20],
                    key="shift_z_2"
                )

                viscosite_encre_2 = st.selectbox(
                    "Viscosité (Pa.s)",
                    options=[10.0, 20.0, 30.0],
                    key="visc_2"
                )

            with col2_2:
                st.markdown("**Angles de contact**")
                angle_paroi_gauche_2 = st.selectbox(
                    "Paroi gauche (°)",
                    options=[30, 45, 60, 90],
                    key="angle_pg_2"
                )

                angle_paroi_droite_2 = st.selectbox(
                    "Paroi droite (°)",
                    options=[30, 45, 60, 90],
                    key="angle_pd_2"
                )

                angle_eg_gauche_2 = st.selectbox(
                    "EG gauche (°)",
                    options=[30, 45, 60, 90],
                    key="angle_eg_2"
                )

                angle_or_2 = st.selectbox(
                    "Or (°)",
                    options=[30, 45, 60, 90],
                    key="angle_or_2"
                )

            if st.button("🚀 Lancer", key="btn_sim2", type="primary", use_container_width=True):
                st.session_state.sim2_running = True
                st.session_state.sim2_params = (
                    diametre_puit_2, shift_buse_x_2, diametre_buse_2, viscosite_encre_2
                )
                st.session_state.sim2_params_full = {
                    'shift_z': shift_buse_z_2,
                    'angle_paroi_gauche': angle_paroi_gauche_2,
                    'angle_paroi_droite': angle_paroi_droite_2,
                    'angle_eg_gauche': angle_eg_gauche_2,
                    'angle_or': angle_or_2
                }

        # Affichage du résultat de la simulation 2
        if 'sim2_running' in st.session_state and st.session_state.sim2_running:
            params = st.session_state.sim2_params
            gif_mapping = get_gif_mapping()

            if params in gif_mapping:
                gif_file = gif_mapping[params]
                gif_html = load_gif(gif_file)

                if gif_html:
                    st.markdown(gif_html, unsafe_allow_html=True)
                    st.caption(f"Puit: {params[0]}µm | Shift: {params[1]}µm | Buse: {params[2]}µm | Viscosité: {params[3]}mPa.s")
                else:
                    st.error(f"Fichier GIF non trouvé: {gif_file}")
            else:
                st.warning("Aucune simulation disponible pour ces paramètres")
        else:
            st.info("Sélectionnez les paramètres et lancez la simulation")

    # Section informations
    st.markdown("---")
    with st.expander("ℹ️ Combinaisons disponibles"):
        st.markdown("""
        Les simulations actuellement disponibles sont:
        - **Simulation 1**: Puit 800µm, Shift 0µm, Buse 100µm, Viscosité 10 mPa.s → `gif_1.gif`
        - **Simulation 2**: Puit 1000µm, Shift 50µm, Buse 150µm, Viscosité 20 mPa.s → `gif_2.gif`
        - **Simulation 3**: Puit 1200µm, Shift 100µm, Buse 200µm, Viscosité 30 mPa.s → `gif_3.gif`
        """)

def physics_page():
    st.title("📚 Physique de la dispense d'encre")
    st.markdown("---")

    # Charger le contenu depuis le fichier markdown
    physics_content = load_markdown_file("documentation/ink_dispensing_physique_v1.md")

    # Afficher le contenu
    st.markdown(physics_content)

def code_page():
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