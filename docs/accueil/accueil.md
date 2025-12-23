# Bienvenue

## Objectif du Projet

Ce projet propose une **étude comparative de quatre méthodes numériques** pour la simulation de la dispense de fluides rhéofluidifiants dans des micro-puits. L'application permet de visualiser et comparer les résultats de simulations diphasiques réalisées avec différentes approches :

- **FEM / Phase-Field** : Méthode des éléments finis avec suivi d'interface par champ de phase
- **VOF (Volume of Fluid)** : Méthode eulérienne standard industriel (OpenFOAM)
- **LBM (Lattice Boltzmann)** : Approche mésoscopique optimisée GPU (Palabos)
- **SPH (Smoothed Particle Hydrodynamics)** : Méthode lagrangienne sans maillage (PySPH)

---

## Application Cible

Les simulations modélisent la **dispense d'encre conductrice Ag/AgCl** dans des micro-puits pour la fabrication de capteurs électrochimiques. Ce procédé nécessite un contrôle précis du remplissage, du mouillage et de la forme finale du dépôt.

**Paramètres clés étudiés :**
- Géométrie : diamètre puit (800–1500 µm), diamètre buse (200–350 µm)
- Rhéologie : viscosité variable (modèle de Carreau)
- Mouillage : angles de contact sur parois et électrode

---

## Navigation

Utilisez le menu latéral pour explorer :
1. **Introduction** : Contexte scientifique et nombres adimensionnels
2. **Comparaison des modèles** : Tableaux comparatifs détaillés
3. **Pages par modèle** : Physique, code source et exemples de simulation
