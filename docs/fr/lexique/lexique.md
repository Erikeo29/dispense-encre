**Sommaire :**
1. Acronymes des Méthodes Numériques
2. Acronymes des Schémas Numériques
3. Nombres Adimensionnels
4. Symboles Physiques
5. Termes Techniques
6. Logiciels et Bibliothèques
7. Acronymes Hardware
8. Abréviations Courantes
9. Unités SI

---

## 1. Acronymes des Méthodes Numériques

| Acronyme | Signification | Description |
|----------|---------------|-------------|
| **FEM** | Finite Element Method | Méthode des éléments finis |
| **VOF** | Volume of Fluid | Méthode de suivi d'interface eulérienne |
| **LBM** | Lattice Boltzmann Method | Méthode de Boltzmann sur réseau |
| **SPH** | Smoothed Particle Hydrodynamics | Hydrodynamique des particules lissées |
| **CFD** | Computational Fluid Dynamics | Mécanique des fluides numérique |
| **DNS** | Direct Numerical Simulation | Simulation numérique directe |

---

## 2. Acronymes des Schémas Numériques

| Acronyme | Signification | Contexte |
|----------|---------------|----------|
| **PLIC** | Piecewise Linear Interface Calculation | Reconstruction d'interface VOF |
| **CSF** | Continuum Surface Force | Modèle de tension superficielle |
| **BGK** | Bhatnagar-Gross-Krook | Opérateur de collision LBM |
| **MRT** | Multiple Relaxation Time | Schéma LBM multi-relaxation |
| **SUPG** | Streamline Upwind Petrov-Galerkin | Stabilisation FEM convection |
| **PSPG** | Pressure Stabilizing Petrov-Galerkin | Stabilisation FEM pression |
| **GLS** | Galerkin Least-Squares | Stabilisation FEM combinée |
| **ALE** | Arbitrary Lagrangian-Eulerian | Maillage mobile |
| **AMR** | Adaptive Mesh Refinement | Maillage adaptatif |
| **MULES** | Multidimensional Universal Limiter | Limiteur OpenFOAM pour VOF |

---

## 3. Nombres Adimensionnels

| Symbole | Nom | Expression | Signification physique |
|---------|-----|------------|------------------------|
| $Re$ | Reynolds | $\frac{\rho v L}{\eta}$ | Inertie / Viscosité |
| $We$ | Weber | $\frac{\rho v^2 L}{\sigma}$ | Inertie / Tension superficielle |
| $Oh$ | Ohnesorge | $\frac{\eta}{\sqrt{\rho \sigma L}}$ | Viscosité / (Inertie × Capillarité)$^{1/2}$ |
| $Ca$ | Capillaire | $\frac{\eta v}{\sigma}$ | Viscosité / Capillarité |
| $Bo$ | Bond | $\frac{\rho g L^2}{\sigma}$ | Gravité / Capillarité |
| $De$ | Deborah | $\lambda \dot{\gamma}$ | Temps de relaxation × Taux de cisaillement |
| $Ma$ | Mach | $\frac{v}{c_s}$ | Vitesse / Vitesse du son |

---

## 4. Symboles Physiques

### Propriétés des Fluides

| Symbole | Nom | Unité SI |
|---------|-----|----------|
| $\rho$ | Masse volumique | kg/m³ |
| $\eta$, $\mu$ | Viscosité dynamique | Pa·s |
| $\nu$ | Viscosité cinématique | m²/s |
| $\sigma$ | Tension superficielle | N/m |
| $\theta$ | Angle de contact | ° ou rad |

### Paramètres Rhéologiques

| Symbole | Nom | Modèle | Unité |
|---------|-----|--------|-------|
| $\eta_0$ | Viscosité au repos | Carreau | Pa·s |
| $\eta_\infty$ | Viscosité à cisaillement infini | Carreau | Pa·s |
| $\lambda$ | Temps de relaxation | Carreau, Oldroyd-B | s |
| $n$ | Indice de comportement | Loi de puissance | - |
| $K$ | Consistance | Loi de puissance | Pa·s$^n$ |
| $\tau_0$ | Contrainte seuil | Herschel-Bulkley | Pa |
| $\dot{\gamma}$ | Taux de cisaillement | Tous | s$^{-1}$ |

### Variables d'Écoulement

| Symbole | Nom | Unité |
|---------|-----|-------|
| $\mathbf{v}$, $\mathbf{u}$ | Vecteur vitesse | m/s |
| $p$ | Pression | Pa |
| $\mathbf{D}$ | Tenseur des taux de déformation | s$^{-1}$ |
| $\boldsymbol{\tau}$ | Tenseur des contraintes | Pa |
| $\kappa$ | Courbure de l'interface | m$^{-1}$ |

---

## 5. Termes Techniques

### Rhéologie

| Terme | Définition |
|-------|------------|
| **Rhéofluidifiant** | Fluide dont la viscosité diminue avec le cisaillement (shear-thinning) |
| **Rhéoépaississant** | Fluide dont la viscosité augmente avec le cisaillement (shear-thickening) |
| **Thixotropie** | Dépendance temporelle de la viscosité (restructuration) |
| **Viscoélasticité** | Comportement combinant viscosité et élasticité |
| **Fluide newtonien** | Viscosité constante indépendante du cisaillement |
| **Fluide non-newtonien** | Viscosité dépendante du cisaillement |
| **Yield stress** | Contrainte seuil d'écoulement |

### Mécanique des Fluides

| Terme | Définition |
|-------|------------|
| **Écoulement diphasique** | Écoulement impliquant deux phases (ex: liquide/gaz) |
| **Interface** | Surface de séparation entre deux phases |
| **Capillarité** | Phénomène lié à la tension superficielle |
| **Mouillage** | Interaction fluide-solide caractérisée par l'angle de contact |
| **Ménisque** | Courbure de l'interface au contact d'une paroi |
| **Pincement** | Rétrécissement du filament avant rupture |
| **Satellite** | Goutte secondaire formée lors de la rupture |
| **Coalescence** | Fusion de deux gouttes |

### Méthodes Numériques

| Terme | Définition |
|-------|------------|
| **Eulérien** | Référentiel fixe (grille fixe) |
| **Lagrangien** | Référentiel mobile (suit les particules) |
| **Maillage** | Discrétisation spatiale du domaine |
| **Sans maillage (meshless)** | Méthode sans connectivité fixe (ex: SPH) |
| **Formulation faible** | Forme intégrale des équations (éléments finis) |
| **Fonction test** | Fonction de pondération en formulation faible |
| **DOF** | Degrees of Freedom (degrés de liberté) |
| **Condition inf-sup** | Critère de stabilité LBB pour éléments mixtes |

---

## 6. Logiciels et Bibliothèques

| Nom | Type | Langage | Méthode |
|-----|------|---------|---------|
| **FEniCS** | Open-source | Python/C++ | FEM |
| **OpenFOAM** | Open-source | C++ | VOF, FVM |
| **Palabos** | Open-source | C++ | LBM |
| **PySPH** | Open-source | Python | SPH |
| **COMSOL** | Commercial | GUI/MATLAB | FEM multiphysique |
| **Ansys Fluent** | Commercial | GUI | VOF, FVM |
| **DualSPHysics** | Open-source | C++/CUDA | SPH GPU |
| **waLBerla** | Open-source | C++ | LBM HPC |

---

## 7. Acronymes Hardware

| Acronyme | Signification | Description |
|----------|---------------|-------------|
| **CPU** | Central Processing Unit | Processeur central |
| **GPU** | Graphics Processing Unit | Processeur graphique |
| **HPC** | High Performance Computing | Calcul haute performance |
| **CUDA** | Compute Unified Device Architecture | API GPU NVIDIA |
| **MPI** | Message Passing Interface | Parallélisation distribuée |
| **OpenMP** | Open Multi-Processing | Parallélisation mémoire partagée |
| **TFLOPS** | Tera Floating-Point Operations Per Second | Unité de puissance de calcul |
| **RAM** | Random Access Memory | Mémoire vive |

---

## 8. Abréviations Courantes

| Abréviation | Signification |
|-------------|---------------|
| **DOD** | Drop-on-Demand (éjection à la demande) |
| **CIJ** | Continuous Inkjet (jet continu) |
| **PIV** | Particle Image Velocimetry |
| **OCT** | Optical Coherence Tomography |
| **PINN** | Physics-Informed Neural Networks |
| **IA** | Intelligence Artificielle |
| **FSI** | Fluid-Structure Interaction |

---

## 9. Unités SI

| Grandeur | Unité | Symbole |
|----------|-------|---------|
| Longueur | mètre | m |
| Masse | kilogramme | kg |
| Temps | seconde | s |
| Force | newton | N |
| Pression | pascal | Pa |
| Viscosité dynamique | pascal-seconde | Pa·s |
| Tension superficielle | newton par mètre | N/m |
| Énergie | joule | J |
| Puissance | watt | W |

### Préfixes

| Préfixe | Symbole | Facteur |
|---------|---------|---------|
| micro | µ | 10$^{-6}$ |
| milli | m | 10$^{-3}$ |
| kilo | k | 10$^{3}$ |
| méga | M | 10$^{6}$ |
| giga | G | 10$^{9}$ |
| téra | T | 10$^{12}$ |
