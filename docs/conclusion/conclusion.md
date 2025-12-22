# Conclusion et Perspectives

Au terme de cette étude comparative sur la simulation de dispense d'encre Ag/AgCl, nous pouvons tirer les conclusions suivantes pour guider les choix technologiques futurs.

### Bilan par Modèle

#### 1. VOF (OpenFOAM)
*   **Verdict :** La valeur sûre.
*   **Forces :** Robustesse éprouvée, conservation de masse parfaite, communauté immense. Idéal pour valider les résultats.
*   **Faiblesses :** Coût de calcul élevé pour capturer les interfaces fines (nécessite un maillage très fin ou adaptatif AMR). Diffusion numérique inévitable sur le long terme.

#### 2. LBM (Palabos)
*   **Verdict :** Le challenger haute performance.
*   **Forces :** Parallélisation naturelle (HPC), gestion "gratuite" des géométries complexes (rugosité du puit) et des angles de contact dynamiques.
*   **Faiblesses :** Stabilité numérique parfois délicate (courants parasites) avec des grands ratios de densité (Air/Encre). Courbe d'apprentissage plus raide.

#### 3. SPH (PySPH)
*   **Verdict :** Le spécialiste de la dynamique violente.
*   **Forces :** Gestion parfaite de la topologie (rupture de jet, éclaboussures, satellites) car sans maillage. Très intuitif pour la physique des gouttes.
*   **Faiblesses :** Précision moindre sur les champs de pression (bruit). Conditions aux limites (parois solides) plus difficiles à implémenter correctement qu'en maillage.

#### 4. FEM / Phase-Field
*   **Verdict :** La référence théorique.
*   **Forces :** Rigueur thermodynamique inégalée pour la physique de la ligne de contact et la capillarité.
*   **Faiblesses :** Temps de calcul prohibitif pour des simulations 3D industrielles. Reste un outil de recherche ou de validation 2D.

### Recommandation

Pour la production industrielle et l'optimisation des paramètres de dispense (Vitesse, Pression), le couplage **VOF (pour la précision)** et **LBM (pour la rapidité d'exploration)** semble être la voie la plus prometteuse. SPH reste un outil précieux pour analyser spécifiquement la formation des gouttes satellites en sortie de buse.
