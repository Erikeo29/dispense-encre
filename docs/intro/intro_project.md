# Simulation de dispense d'encre rhéofluidifiante

### Objectif du Projet

Ce projet vise à **modéliser** le processus de dispense d'encre dans un domaine micro-fluidique en utilisant **différents modèles de modélisation: FEM, VOF, LBM, SPH**

Une encre type Ag/AgCl possède un comportement rhéologique complexe (non-newtonien) et doit remplir précisément des micro-puits sans emprisonner d'air ni déborder.

**Défis techniques :**
*   Dynamique rapide (quelques ms).
*   Rhéologie complexe (Shear-thinning).
*   Tension de surface dominante (Échelle capillaire).
*   Mouillage dynamique (Angles de contact).

---

### Approche Comparative

Nous comparons ici 4 approches numériques distinctes pour identifier la plus pertinente :

1.  **FEM / Phase-Field** (Approche continue diffuse).
2.  **VOF** (Volume of Fluid - Standard industriel).
3.  **LBM** (Lattice Boltzmann - Approche mésoscopique).
4.  **SPH** (Particules Lagrangiennes - Sans maillage).
