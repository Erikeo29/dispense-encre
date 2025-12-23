# Simulation de Dispense d'Encre Rhéofluidifiante

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dispense-encre.streamlit.app/)

Application Streamlit pour la visualisation et comparaison de simulations numériques de dispense de fluides rhéofluidifiants (encre Ag/AgCl) dans des micro-puits.

## Modèles Comparés

| Modèle | Méthode | Implémentation | Focus Physique |
|--------|---------|----------------|----------------|
| **FEM** | Éléments Finis / Phase-Field | Python (FEniCS) | Thermodynamique interface, capillarité |
| **VOF** | Volume of Fluid | C++ (OpenFOAM) | Standard industriel, conservation masse |
| **LBM** | Lattice Boltzmann | C++ (Palabos) | Performance GPU, géométries complexes |
| **SPH** | Smoothed Particle Hydrodynamics | Python (PySPH) | Surfaces libres, grandes déformations |

## Fonctionnalités

- **Page d'accueil** : Aperçu des 4 modèles avec exemples animés
- **Documentation scientifique** : Équations LaTeX, nombres adimensionnels, références
- **Comparaison détaillée** : Tableaux hardware, précision, coût calcul
- **Visualiseur interactif** : Sélection de paramètres pour le modèle FEM
- **Navigation fluide** : Bouton retour en haut, onglets visibles

## Structure du Projet

```
app.py              # Application Streamlit (~350 lignes)
assets/             # Ressources visuelles (GIFs, PNGs)
  fem/, vof/, lbm/, sph/
data/               # Mappings CSV paramètres → fichiers
docs/               # Documentation Markdown (~2000 lignes)
  accueil/          # Page d'accueil
  intro/            # Contexte scientifique
  physics/          # Théorie par modèle
  comparaison/      # Tableaux comparatifs
  conclusion/       # Recommandations
```

## Installation

```bash
git clone https://github.com/Erikeo29/dispense-encre.git
cd dispense-encre
pip install -r requirements.txt
streamlit run app.py
```

## Documentation Technique

La documentation inclut :
- Nombres adimensionnels (Re, We, Oh, De, Ca, Bo)
- Équations de Navier-Stokes et modèles rhéologiques (Carreau, Herschel-Bulkley)
- Méthodes numériques détaillées (VOF-PLIC, LBM-BGK, SPH-CSF, FEM-SUPG)
- Résultats de validation expérimentale
- Recommandations hardware et coûts calcul

## Version

**Version 3.1.0 (Décembre 2025)**
- Nouvelle page d'accueil avec aperçu des 4 modèles
- Documentation scientifique enrichie (~2000 lignes)
- Interface améliorée (onglets visibles, bouton retour haut)
- Corrections LaTeX pour compatibilité KaTeX

## Licence

Projet de recherche - Usage interne
