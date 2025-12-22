# 🔬 Simulation de Dispense d'Encre Ag/AgCl

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dispense-encre.streamlit.app/)

Ce projet de R&D compare différentes approches numériques pour modéliser le processus de dispense d'encre conductrice (Ag/AgCl) dans des micro-puits pour la fabrication de biocapteurs.

L'application Streamlit permet de visualiser et comparer les résultats de 4 modèles physiques distincts.

## 📊 Modèles Comparés

| Modèle | Méthode | Implémentation | Focus Physique |
| :--- | :--- | :--- | :--- |
| **FEM** | Éléments Finis / Phase-Field | **Python (FEniCS)** | Thermodynamique de l'interface, capillarité fine |
| **VOF** | Volume of Fluid | **C++ (OpenFOAM)** | Standard industriel, robustesse, conservation de masse |
| **LBM** | Lattice Boltzmann (Shan-Chen) | **C++ (Palabos)** | Calcul HPC, géométries complexes, mouillage naturel |
| **SPH** | Smoothed Particle Hydrodynamics | **Python (PySPH)** | Surface libre complexe, éclaboussures, dynamique violente |

## 📂 Structure du Projet

L'architecture du projet a été rationalisée pour faciliter la maintenance :

*   `app.py` : Point d'entrée de l'application Streamlit.
*   `assets/` : Contient toutes les ressources visuelles (GIFs, PNGs), organisées par modèle (`fem`, `vof`, `lbm`, `sph`).
*   `data/` : Contient les fichiers de mapping CSV pour les correspondances paramètres/résultats.
*   `docs/` : Contient la documentation scientifique (Markdown) et les extraits de code source réels.
    *   `physics/` : Explications théoriques.
    *   `code/` : Fichiers sources (.cpp, .py) extraits des solveurs.

## 🚀 Installation et Lancement

Cloner le dépôt :
```bash
git clone https://github.com/Erikeo29/dispense-encre.git
cd dispense-encre
```

Installer les dépendances :
```bash
pip install -r requirements.txt
```

Lancer l'application :
```bash
streamlit run app.py
```

## 📝 Version

**Version 3.0.0 (Décembre 2025)**
*   Architecture multi-modèles unifiée.
*   Intégration des résultats VOF, LBM et SPH.
*   Documentation technique complète.