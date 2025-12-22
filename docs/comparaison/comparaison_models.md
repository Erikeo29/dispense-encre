# Comparatif des Méthodes de Modélisation Multifluidique

Vue globale des technologies open-source disponibles pour la simulation d'écoulements à surface libre.

---

### Analyse Critique

*   **VOF (Volume of Fluid)** reste incontournable pour la validation industrielle et l'ingénierie générale. Cependant, elle peut peiner sur les phénomènes de mouillage dynamique à très petite échelle sans un maillage extrêmement fin.
*   **LBM (Lattice Boltzmann)** offre des performances de calcul impressionnantes, surtout sur GPU. Elle gère naturellement les géométries complexes (poreux, rugosité) et la séparation de phase (Shan-Chen), mais peut souffrir de courants parasites.
*   **SPH (Smoothed Particle Hydrodynamics)** est la méthode de choix pour les projections dynamiques, les ruptures de jet et les éclaboussures violentes, car elle n'a pas de maillage. La gestion précise de la tension de surface reste son défi majeur.
*   **Phase-Field (FEM)** apporte une précision thermodynamique inégalée pour la capillarité et les angles de contact, mais au prix d'un temps de calcul souvent prohibitif pour des problèmes 3D industriels.

---

### Détails Techniques

| Méthode | Principe | Points Forts (Pros) | Points Faibles (Cons) | Hardware | Langages & Libs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FEM / Phase-Field** | Interface diffuse par équation d'énergie (Cahn-Hilliard) | Rigueur mathématique, Couplage multiphysique aisé | Très coûteux en temps de calcul, Difficile pour grandes déformations | CPU (Calcul matriciel lourd) | Python/C++ (FEniCS, Comsol) |
| **VOF (Volume of Fluid)** | Suivi d'interface sur maillage fixe (Eulerien), transport de fraction $\alpha$ | Standard industriel, Conservation de masse, Robuste | Diffusion numérique de l'interface, Coût du maillage dynamique (AMR) | CPU (Peu de threads rapides) | C++ (OpenFOAM) |
| **LBM (Lattice Boltzmann)** | Cinétique des gaz sur réseau (Mésoscopique), distribution de particules $f_i$ | Parallélisation massive (HPC/GPU), Géométries complexes, Mouillage naturel | Instabilités numériques à haute densité/vitesse, Gourmand en mémoire | GPU (Idéal) ou Cluster CPU (MPI) | C++ (Palabos, OpenLB, Walberla) |
| **SPH (Smoothed Particle Hydrodynamics)** | Particules mobiles sans maillage (Lagrangien) | Surfaces libres complexes (éclaboussures), Pas de maillage, Advection exacte | Précision moindre (bruit), Conditions aux limites (parois) difficiles | GPU (Essentiel pour grand nombre de particules) | Python/C++ (PySPH, DualSPHysics) |
