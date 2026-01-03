# Méthode Volume of Fluid (VOF)

## Principe Fondamental

La méthode **VOF (Volume of Fluid)** est une approche eulérienne pour le suivi d'interfaces dans les écoulements diphasiques. Elle représente le standard industriel pour les simulations à surface libre, notamment dans OpenFOAM avec le solveur `interFoam`.

### Concept de Fraction Volumique

L'interface entre les deux fluides est capturée par une variable scalaire, la **fraction volumique** $\alpha$ :

- $\alpha = 1$ : Fluide 1 (encre) pur
- $\alpha = 0$ : Fluide 2 (air) pur
- $0 < \alpha < 1$ : Zone d'interface (transition)

Cette approche est dite "à interface diffuse" car l'interface n'est pas une ligne nette mais une zone de transition sur quelques cellules.

---

## Équations Fondamentales

### Équation de Transport de $\alpha$

L'évolution de la fraction volumique est gouvernée par l'équation d'advection :

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

où $\mathbf{v}$ est le champ de vitesse.

### Force de Tension Superficielle (CSF)

La tension superficielle est modélisée via le modèle **Continuum Surface Force (CSF)** de Brackbill :

$$\mathbf{f}_\sigma = \sigma \kappa \nabla \alpha$$

où :
- $\sigma$ : tension superficielle [N/m]
- $\kappa = -\nabla \cdot \left(\frac{\nabla \alpha}{|\nabla \alpha|}\right)$ : courbure de l'interface

### Propriétés du Mélange

Les propriétés physiques sont interpolées linéairement :

$$\rho = \alpha \rho_1 + (1-\alpha) \rho_2$$

$$\eta = \alpha \eta_1 + (1-\alpha) \eta_2$$

---

## Schémas de Reconstruction d'Interface

### Problématique de la Diffusion Numérique

Le transport de $\alpha$ par advection pure conduit à une **diffusion numérique** de l'interface, la rendant floue sur plusieurs cellules. Plusieurs schémas existent pour maintenir une interface nette :

### PLIC (Piecewise Linear Interface Calculation)

Le schéma **PLIC** reconstruit l'interface comme un plan dans chaque cellule :

$$\mathbf{n} \cdot \mathbf{x} = d$$

où $\mathbf{n} = \frac{\nabla \alpha}{|\nabla \alpha|}$ est la normale à l'interface et $d$ la distance à l'origine.

**Avantages :**
- Précision interfaciale de 0.1–1 µm
- Conservation de masse exacte
- Standard dans OpenFOAM

### Geometric VOF

Utilise des algorithmes géométriques pour calculer les flux de $\alpha$ entre cellules :
- Calcul exact des volumes de fluide traversant chaque face
- Plus coûteux mais plus précis que les schémas algébriques

### Compressive VOF (OpenFOAM)

OpenFOAM ajoute un terme de **compression artificielle** (MULES) :

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\mathbf{v} \alpha) + \nabla \cdot [\mathbf{v}_r \alpha (1-\alpha)] = 0$$

où $\mathbf{v}_r = c_\alpha |\mathbf{v}| \mathbf{n}$ est une vitesse de compression artificielle qui agit **uniquement à l'interface** ($\alpha(1-\alpha) \neq 0$) pour contrer la diffusion.

**Paramètre clé :** $c_\alpha = 1$ (valeur par défaut dans OpenFOAM)

---

## Adaptation aux Fluides Non-Newtoniens

### Tenseur des Contraintes

Pour les encres rhéofluidifiantes, le tenseur des contraintes $\boldsymbol{\tau}$ est modifié pour inclure la dépendance au taux de cisaillement $\dot{\gamma}$ :

$$\boldsymbol{\tau} = K|\dot{\gamma}|^{n-1}\dot{\gamma}$$

où $\dot{\gamma} = \sqrt{2\mathbf{D}:\mathbf{D}}$ et $\mathbf{D} = \frac{1}{2}\left(\nabla \mathbf{v} + (\nabla \mathbf{v})^T\right)$.

### Modèle de Carreau dans OpenFOAM

La viscosité effective $\eta_{eff}$ suit le modèle de Carreau :

$$\eta_{eff}(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) [1 + (\lambda \dot{\gamma})^2]^{(n-1)/2}$$

**Paramètres typiques pour encre Ag/AgCl :**

| Paramètre | Symbole | Valeur | Unité |
|-----------|---------|--------|-------|
| Masse volumique | $\rho$ | 3000 | kg/m³ |
| Viscosité au repos | $\eta_0$ | 0.5 – 5 | Pa·s |
| Viscosité à cisaillement infini | $\eta_\infty$ | 0.05 – 0.167 | Pa·s |
| Temps de relaxation | $\lambda$ | 0.15 | s |
| Indice de pseudoplasticité | $n$ | 0.7 | - |
| Tension de surface | $\sigma$ | 0.04 | N/m |

---

## Configuration OpenFOAM

### Fichier `transportProperties`

```cpp
transportModel Carreau;

CarreauCoeffs
{
    nu0     nu0 [0 2 -1 0 0 0 0] 1.667e-4;  // η₀/ρ
    nuInf   nuInf [0 2 -1 0 0 0 0] 5.56e-5;  // η∞/ρ
    k       k [0 0 1 0 0 0 0] 0.15;          // λ
    n       n [0 0 0 0 0 0 0] 0.7;           // n
}

sigma   sigma [1 0 -2 0 0 0 0] 0.04;  // Tension de surface
```

### Solveur `interFoam`

Le solveur `interFoam` résout :
1. Équation de transport de $\alpha$ (MULES)
2. Équations de Navier-Stokes avec propriétés variables
3. Couplage pression-vitesse (PIMPLE)

---

## Avantages et Limitations

### Points Forts

- **Robustesse éprouvée** : Standard industriel avec >25 ans de développement
- **Conservation de masse parfaite** : Propriété intrinsèque de la formulation
- **Implémentations open-source** : OpenFOAM, Basilisk
- **Précision interfaciale** : 0.1–1 µm avec PLIC et maillage adaptatif (AMR)

### Limitations

- **Diffusivité numérique** : Nécessite des schémas de reconstruction coûteux
- **Coût mémoire** : Maillages fins requis pour les interfaces fines
- **Coalescences multiples** : Difficiles à gérer proprement
- **Rhéologie newtonienne** : Les lois simples (Carreau) fonctionnent, les lois complexes (thixotropie) sont difficiles

---

## Résultats de Validation

### Étude Duarte et al. (2019)

**Configuration :**
- Solveur : OpenFOAM (`interFoam`)
- Maillage adaptatif (AMR) avec taille minimale de cellule = 0.2 µm
- Encre newtonienne ($\sigma = 35$ mN/m, $\eta = 4$ mPa·s)

**Résultats :**
- Longueur du filament avant détachement : 150 µm (expérimental : 148 ± 2 µm)
- Vitesse de la goutte : 12 m/s (erreur < 2 %)
- Formation de satellite : 8 % du volume total à $t = 15$ µs

### Étude Li et al. (2021) - Fluides Non-Newtoniens

**Configuration :**
- Loi de puissance ($n = 0.7$, $K = 0.1$ Pa·sⁿ)
- $We = 3.5$, $Oh = 0.05$

**Résultats :**

| Paramètre | Newtonien ($n=1$) | Rhéofluidifiant ($n=0.7$) |
|-----------|-------------------|---------------------------|
| Temps de pincement (µs) | 18 ± 0.5 | 22 ± 0.8 |
| Volume satellite (%) | 12 | 8 |
| Vitesse goutte (m/s) | 12.1 | 11.8 |

**Mécanisme :** La rhéofluidification réduit la viscosité effective dans les zones de fort cisaillement (filament), accélérant le pincement tout en réduisant les satellites.

---

## Coût Computationnel

### Configuration Typique

Pour une simulation 2D axisymétrique (1 ms d'éjection) :

| Configuration | Maillage | Temps (h) | Hardware |
|---------------|----------|-----------|----------|
| Standard | 100k cellules | 2–4 | 8 cœurs CPU |
| Haute résolution | 500k cellules | 8–12 | 16 cœurs CPU |
| AMR | 100k–1M (adaptatif) | 4–8 | 16 cœurs + GPU |

**Impact GPU :** OpenFOAM supporte CUDA depuis la version 10, avec des accélérations de x5–x10 pour les opérations matricielles.

---

## Références

> **Note** : Pour la liste complète des références, consultez la section **Bibliographie** dans le menu Annexes.

1. Hirt, C. W., & Nichols, B. D. (1981). *Volume of fluid (VOF) method for the dynamics of free boundaries*. Journal of Computational Physics, 39(1), 201-225. [DOI:10.1016/0021-9991(81)90145-5](https://doi.org/10.1016/0021-9991(81)90145-5)

2. Brackbill, J. U., Kothe, D. B., & Zemach, C. (1992). *A continuum method for modeling surface tension*. Journal of Computational Physics, 100(2), 335-354. [DOI:10.1016/0021-9991(92)90240-Y](https://doi.org/10.1016/0021-9991(92)90240-Y)

3. Popinet, S. (2009). *An accurate adaptive solver for surface-tension-driven interfacial flows*. Journal of Computational Physics, 228(16), 5838-5866. [DOI:10.1016/j.jcp.2009.04.042](https://doi.org/10.1016/j.jcp.2009.04.042)

4. Jasak, H. (1996). *Error Analysis and Estimation for the Finite Volume Method with Applications to Fluid Flows*. PhD Thesis, Imperial College London.
