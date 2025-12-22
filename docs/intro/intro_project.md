# Simulation de Dispense d'Encre type Ag/AgCl

### Optimisation de la dispense d'encre conductrice en micro-puits

---

### Objectif du Projet

Ce projet de R&D vise à **comprendre, modéliser et optimiser** le processus complexe de dispense d'encre micro-fluidique.

L'encre Ag/AgCl, utilisée pour la fabrication de biocapteurs, possède un comportement rhéologique complexe (non-newtonien) et doit remplir précisément des micro-puits sans emprisonner d'air ni déborder.

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
