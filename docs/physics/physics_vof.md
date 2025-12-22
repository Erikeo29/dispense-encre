# Méthode Volume of Fluid (VOF)

La méthode **VOF** est la référence industrielle pour les écoulements à surface libre. Elle est implémentée ici via le solveur `interFoam` d'OpenFOAM.

### 1. Suivi d'Interface (Interface Tracking)

L'interface entre l'encre et l'air est capturée par une variable scalaire, la fraction volumique $\alpha$ :
*   $\alpha = 1$ : Encre pure
*   $\alpha = 0$ : Air pur
*   $0 < \alpha < 1$ : Interface

L'équation de transport résolue est :

$$ 
\frac{\partial \alpha}{\partial t} + \nabla \cdot (\mathbf{u} \alpha) + \nabla \cdot [\mathbf{u}_r \alpha (1-\alpha)] = 0 
$$ 

Le dernier terme est un terme de **compression artificielle** (MULES - *Multidimensional Universal Limiter with Explicit Solution*) spécifique à OpenFOAM. Il agit uniquement à l'interface pour contrer la diffusion numérique et garder une interface nette ("sharp").

### 2. Rhéologie Non-Newtonienne (Carreau)

L'encre Ag/AgCl est modélisée comme un fluide rhéofluidifiant (shear-thinning) pour simuler son comportement réel (moins visqueux quand il est cisaillé dans la buse, plus visqueux au repos).

La viscosité effective $\eta_{eff}$ dépend du taux de cisaillement local $\dot{\gamma}$ :

$$ 
\eta_{eff} = \eta_\infty + (\eta_0 - \eta_\infty) [1 + (\lambda \dot{\gamma})^2 ]^{(n-1)/2} 
$$ 

**Paramètres utilisés (extraits de `transportProperties`) :**
*   **Densité (rho) :** $3000 \, kg/m^3$
*   **Viscosité zéro cisaillement ($\eta_0$) :** $0.5 \, Pa \cdot s$
*   **Viscosité infinie ($\eta_\infty$) :** $0.167 \, Pa \cdot s$ (approx $\eta_0 / 3$)
*   **Temps de relaxation ($\lambda$) :** $0.15 \, s$
*   **Indice de loi de puissance (n) :** $0.7$
*   **Tension de surface ($\sigma$) :** $0.04 \, N/m
