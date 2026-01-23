**Sommaire :**
1. Principe de la Méthode
2. Équations Fondamentales
3. Formulation Mathématique
4. Avantages et Limitations
5. Coût Computationnel
6. Bibliothèques Open-Source
7. Références

---

## 1. Principe de la Méthode

La méthode **VOF (Volume of Fluid)** est une approche eulérienne pour le suivi d'interfaces dans les écoulements diphasiques. Elle représente le **standard industriel** pour les simulations à surface libre, notamment avec le solveur `interFoam` d'OpenFOAM.

### Variable principale : Fraction volumique α

| Valeur | Signification |
|--------|---------------|
| α = 1 | Encre (fluide 1) |
| α = 0 | Air (fluide 2) |
| 0 < α < 1 | Zone d'interface |

**Avantage clé :** Conservation de masse parfaite, propriété intrinsèque de la formulation.

---

## 2. Équations Fondamentales

### 2.1 Équations de Navier-Stokes

**Conservation de la masse :**
$$\nabla \cdot \mathbf{v} = 0$$

**Conservation de la quantité de mouvement :**
$$\rho\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho\mathbf{g} + \mathbf{f}_\sigma$$

### 2.2 Équation de transport de α

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

**Avec compression artificielle (MULES - OpenFOAM) :**
$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\mathbf{v} \alpha) + \nabla \cdot [\mathbf{v}_r \alpha (1-\alpha)] = 0$$

où **v**_r = c_α |**v**| **n** est une vitesse de compression qui agit uniquement à l'interface pour contrer la diffusion numérique.

### 2.3 Force de tension de surface (CSF)

Le modèle **Continuum Surface Force** de Brackbill :

$$\mathbf{f}_\sigma = \sigma \kappa \nabla \alpha$$

où κ = -∇·(∇α/|∇α|) est la courbure de l'interface.

---

## 3. Formulation Mathématique

### 3.1 Propriétés du mélange

Les propriétés physiques sont interpolées linéairement :

$$\rho = \alpha \rho_1 + (1-\alpha) \rho_2$$
$$\eta = \alpha \eta_1 + (1-\alpha) \eta_2$$

### 3.2 Modèle de Carreau (fluides non-Newtoniens)

$$\eta_{eff}(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) [1 + (\lambda \dot{\gamma})^2]^{(n-1)/2}$$

| Paramètre | Symbole | Valeur | Unité |
|-----------|---------|--------|-------|
| Masse volumique | ρ | 3000 | kg/m³ |
| Viscosité au repos | η₀ | 0.5 – 5 | Pa·s |
| Viscosité à cisaillement infini | η∞ | 0.05 – 0.167 | Pa·s |
| Temps de relaxation | λ | 0.15 | s |
| Indice de pseudoplasticité | n | 0.7 | - |
| Tension de surface | σ | 0.04 | N/m |

### 3.3 Configuration OpenFOAM (`transportProperties`)

```cpp
transportModel Carreau;

CarreauCoeffs {
    nu0   nu0 [0 2 -1 0 0 0 0] 1.667e-4;  // η₀/ρ
    nuInf nuInf [0 2 -1 0 0 0 0] 5.56e-5; // η∞/ρ
    k     k [0 0 1 0 0 0 0] 0.15;          // λ
    n     n [0 0 0 0 0 0 0] 0.7;           // n
}

sigma sigma [1 0 -2 0 0 0 0] 0.04;
```

---

## 4. Avantages et Limitations

| Avantages | Limitations |
|-----------|-------------|
| Robustesse éprouvée (>25 ans) | Diffusion numérique de l'interface |
| Conservation de masse parfaite | Maillages fins requis près de l'interface |
| Standard industriel (OpenFOAM) | Coalescences multiples difficiles |
| Précision interfaciale 0.1–1 µm (avec PLIC) | Rhéologie complexe (thixotropie) difficile |
| Support GPU depuis OpenFOAM 10 | Coût mémoire pour AMR |

---

## 5. Coût Computationnel

| Configuration | Maillage | Temps | Hardware |
|---------------|----------|-------|----------|
| 2D standard | 100k cellules | 2–4 h | 8 cœurs CPU |
| 2D haute résolution | 500k cellules | 8–12 h | 16 cœurs CPU |
| 2D avec AMR | 100k–1M (adaptatif) | 4–8 h | 16 cœurs + GPU |

**Accélération GPU :** x5–x10 pour les opérations matricielles (OpenFOAM ≥ v10 avec CUDA).

---

## 6. Bibliothèques Open-Source

| Bibliothèque | Langage | Focus | Parallélisation |
|--------------|---------|-------|-----------------|
| **OpenFOAM** | C++ | Standard industriel, VOF/interFoam | MPI, CUDA |
| **Basilisk** | C | Recherche, AMR natif | MPI |
| **Gerris** | C | Précurseur de Basilisk | MPI |

---

## 7. Références

> **Note** : Pour la liste complète des références, consultez la section **Bibliographie** dans le menu Annexes.
