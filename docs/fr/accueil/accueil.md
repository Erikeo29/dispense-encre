<div style="font-size: 0.9em; line-height: 1.3; background: #f8f9fa; padding: 8px 12px; border-radius: 4px; margin-bottom: 1em;">

**Sommaire :** 1. Objectif du Projet • 2. Application Cible • 3. Navigation
</div>

## 1. Objectif du Projet

Ce projet propose une **étude comparative de quatre méthodes numériques** pour la simulation de la dispense de fluides rhéofluidifiants dans des micro-puits. L'application permet de visualiser et comparer les résultats de simulations diphasiques réalisées avec différentes approches :

- **FEM / Phase-Field** : Méthode des éléments finis avec suivi d'interface par champ de phase
- **VOF (Volume of Fluid)** : Méthode eulérienne standard industriel (OpenFOAM)
- **LBM (Lattice Boltzmann)** : Approche mésoscopique optimisée GPU (Palabos)
- **SPH (Smoothed Particle Hydrodynamics)** : Méthode lagrangienne sans maillage (PySPH)

---

## 2. Application Cible

Les simulations modélisent la **dispense d'une encre rhéofluidifiante** dans des micro-puits pour la fabrication de capteurs électrochimiques. Ce procédé nécessite un contrôle précis du remplissage, du mouillage et de la forme finale du dépôt.

**Paramètres clés étudiés :**
- Géométrie : diamètre puit (800–1500 µm), diamètre buse (200–350 µm)
- Rhéologie : viscosité variable (modèle de Carreau)
- Mouillage : angles de contact sur le fond du puit, sur les parois verticales du puit, sur la surface horizontale du substrat.

---

## 3. Navigation

Utilisez le menu latéral pour explorer les différents chapitres du projet:
1. **Introduction** : Contexte scientifique et nombres adimensionnels
2. **Comparaison des modèles** : Tableaux comparatifs détaillés
3. **Pages par modèle** : Physique, code source et exemples de simulation: animation de l'écoulement pendant la dispense(fichiers GIF) et images de l'état final (fichiers PNG).
