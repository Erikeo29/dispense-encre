# Smoothed Particle Hydrodynamics (SPH)

La méthode SPH est une méthode **Lagrangienne** et **sans maillage (meshless)**. Le fluide est représenté par un ensemble de particules mobiles qui transportent les propriétés physiques (masse, vitesse, pression).

### Physique Fondamentale

Contrairement aux méthodes sur grille (VOF, FEM), il n'y a pas de connexions fixes entre les points. La valeur d'une propriété $A$ en une position $\mathbf{r}$ est calculée par interpolation sur les particules voisines $b$ :

$$
A(\mathbf{r}) = \sum_b m_b \frac{A_b}{\rho_b} W(|\mathbf{r} - \mathbf{r}_b|, h)
$$

Où $W$ est le **noyau de lissage (Smoothing Kernel)** et $h$ la longueur de lissage.

### Gestion de la Physique Multiphasique

#### 1. Tension de Surface (Modèle de Morris)

La tension de surface est critique pour la formation de gouttelettes. Le modèle utilisé ici (Morris, 2000 - *Continuum Surface Force*) ajoute une force volumique basée sur la courbure de l'interface.

La force appliquée à chaque particule d'interface est :

$$
\mathbf{F}_{st} = -\sigma \kappa \mathbf{n}
$$

*   $\\mathbf{n} = \nabla c$ : La normale est calculée par le gradient du champ de couleur $c$ (qui vaut 1 dans l'encre, 0 ailleurs).
*   $\\kappa = -\nabla \cdot \mathbf{n}$ : La courbure est la divergence de cette normale.

#### 2. Conditions aux Limites (Adami et al.)

Gérer des parois solides étanches est difficile en SPH. Nous utilisons la méthode d'**Adami (2012)** :
*   Les parois sont constituées de plusieurs couches de **particules fantômes (dummy particles)** fixes.
*   Ces particules exercent une pression répulsive calculée dynamiquement pour empêcher le fluide de traverser, tout en imposant la condition de non-glissement (no-slip).

### Avantages Uniques pour la Dispense

*   **Surface Libre :** La SPH est imbattable pour gérer les surfaces libres complexes, les ruptures de jet, les satellites et les éclaboussures violentes, car il n'y a pas de maillage à déformer ou à raffiner.
*   **Advection Exacte :** Le terme convectif non-linéaire $(\mathbf{u} \cdot \nabla)\mathbf{u}$ est traité exactement par le mouvement des particules, éliminant totalement la diffusion numérique classique des méthodes Euleriennes.
