# Méthode Lattice Boltzmann (LBM)

## Principe Mésoscopique

La méthode **LBM (Lattice Boltzmann Method)** est une approche mésoscopique qui ne résout pas directement les équations de Navier-Stokes, mais l'**équation de Boltzmann discrétisée** sur un réseau régulier (lattice).

### Concept Fondamental

On suit l'évolution de **fonctions de distribution** $f_i(\mathbf{x}, t)$ représentant la probabilité de trouver des particules à la position $\mathbf{x}$ au temps $t$, se déplaçant selon des directions discrètes $\mathbf{c}_i$.

Les grandeurs macroscopiques (densité $\rho$, vitesse $\mathbf{u}$) sont obtenues par **moments statistiques** :

$$\rho = \sum_i f_i \quad \text{et} \quad \rho \mathbf{u} = \sum_i f_i \mathbf{c}_i$$

---

## Équation de Boltzmann Discrète

### Formulation BGK

L'équation fondamentale est :

$$f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = \Omega_i(f) + F_i$$

où :
- $\Omega_i(f)$ : opérateur de collision (relaxation vers l'équilibre)
- $F_i$ : terme de force externe

### Opérateur de Collision BGK

L'approximation BGK (Bhatnagar-Gross-Krook) simplifie la collision en une relaxation linéaire vers l'équilibre :

$$\Omega_i = -\frac{1}{\tau}(f_i - f_i^{eq})$$

où $\tau$ est le **temps de relaxation** et $f_i^{eq}$ la distribution d'équilibre de Maxwell-Boltzmann discrétisée :

$$f_i^{eq} = w_i \rho \left[1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2c_s^4} - \frac{\mathbf{u}^2}{2c_s^2}\right]$$

avec $c_s = 1/\sqrt{3}$ la vitesse du son sur le réseau et $w_i$ les poids de quadrature.

---

## Grilles de Discrétisation

### Nomenclature DdQq

La notation **DdQq** indique :
- **d** : nombre de dimensions spatiales
- **q** : nombre de vitesses discrètes

### Grilles Courantes

| Grille | Application | Vitesses |
|--------|-------------|----------|
| **D2Q9** | 2D standard | 9 directions (repos + 4 axes + 4 diagonales) |
| **D3Q15** | 3D économique | 15 directions |
| **D3Q19** | 3D standard | 19 directions (bon compromis précision/coût) |
| **D3Q27** | 3D haute précision | 27 directions (cube complet) |

**Choix typique pour l'inkjet :** D3Q19 avec $\Delta x = 0.3$ µm

---

## Lien avec la Viscosité

### Relation Fondamentale

La viscosité cinématique $\nu$ est reliée au temps de relaxation $\tau$ par :

$$\nu = c_s^2 \left(\tau - \frac{1}{2}\right) \Delta t$$

Cette relation est **fondamentale** : elle permet de modéliser des fluides de viscosités différentes en ajustant simplement $\tau$.

### Adaptation aux Fluides Non-Newtoniens

Pour les fluides rhéofluidifiants, $\tau$ dépend localement du taux de cisaillement $\dot{\gamma}$ :

$$\tau(\dot{\gamma}) = \frac{1}{2} + \frac{\nu(\dot{\gamma})}{c_s^2 \Delta t}$$

où $\nu(\dot{\gamma})$ est donné par une loi rhéologique (ex. loi de puissance, Carreau).

---

## Modèles Multiphasiques

### Shan-Chen (Pseudopotentiel)

Le modèle **Shan-Chen** modélise les interactions entre fluides via une **force interparticulaire** :

$$\mathbf{F}_{int}(\mathbf{x}) = -G\psi(\mathbf{x}) \sum_i w_i \psi(\mathbf{x} + \mathbf{c}_i \Delta t) \mathbf{c}_i$$

où :
- $G$ : paramètre d'interaction (contrôle la tension superficielle)
- $\psi(\mathbf{x})$ : fonction de pseudopotentiel dépendant de la densité locale

**Séparation de phase :** Cette force provoque une séparation spontanée des phases (comme eau/huile) sans suivi explicite de l'interface.

**Tension superficielle :** $\sigma \propto G(\psi_{max} - \psi_{min})^2$

### Free Energy Model

Le modèle **Free Energy** est basé sur une fonctionnelle d'énergie libre :

$$\mathcal{F} = \int_V \left[\psi(\rho) + \frac{\kappa}{2}|\nabla\rho|^2\right] dV$$

La force d'interface est dérivée du gradient d'énergie :

$$\mathbf{F} = -\nabla \cdot \boldsymbol{\sigma}^{chem}$$

**Avantages vs Shan-Chen :**
- Meilleure stabilité pour les grands ratios de densité
- Contrôle plus précis de la tension superficielle
- Moins de courants parasites

### Color Gradient Model

Utilise deux populations de fluides (rouge/bleu) avec une force de ségrégation :

$$\mathbf{F}_{seg} = A|\nabla \rho^N| \mathbf{n}$$

où $\rho^N = (\rho^R - \rho^B)/(\rho^R + \rho^B)$ est la fraction de couleur normalisée.

---

## Gestion du Mouillage

### Angles de Contact

Les angles de contact sur les parois solides sont gérés en assignant une **densité fictive** (ou un potentiel) aux nœuds solides :

$$\rho_{solid} = \rho_0 + \Delta \rho \cdot \cos(\theta_{eq})$$

où $\theta_{eq}$ est l'angle de contact d'équilibre souhaité.

**Avantage majeur :** Le mouillage est géré **naturellement** sans conditions aux limites explicites complexes, ce qui est idéal pour les géométries complexes (micro-puits, rugosité).

---

## Scalabilité GPU

### Performance Exceptionnelle

La LBM est **intrinsèquement parallèle** : chaque nœud peut être mis à jour indépendamment lors des étapes de collision et de streaming.

**Accélération typique :** x20 sur GPU vs CPU (mesuré sur NVIDIA A100)

### Benchmark Li et al. (2022)

| Configuration | Temps de calcul |
|---------------|-----------------|
| CPU (20 h) | Référence |
| GPU A100 (1 GPU) | 2 h |
| GPU A100 (4 GPUs) | 35 min |
| GPU A100 (16 GPUs) | 10 min |

**Scalabilité quasi-linéaire** jusqu'à 16 GPUs.

---

## Bibliothèques Open-Source

### Palabos

**Palabos** (Parallel Lattice Boltzmann Solver) est la référence open-source :

- **Langage :** C++ orienté objet
- **Parallélisation :** MPI natif, excellent scaling sur clusters
- **Modèles :** Shan-Chen, Free Energy, Color Gradient
- **Documentation :** Excellente avec tutoriels

### Alternatives

| Bibliothèque | Focus | GPU |
|--------------|-------|-----|
| **OpenLB** | Ingénierie, applications industrielles | OpenMP/CUDA |
| **waLBerla** | HPC extrême, millions de cœurs | CUDA native |
| **Sailfish** | GPU natif, Python interface | CUDA prioritaire |
| **Musubi** | Couplage multiphysique | MPI |

---

## Résultats de Validation

### Étude Li et al. (2022) - Encre Rhéofluidifiante

**Configuration :**
- Solveur : Palabos (C++/CUDA)
- Grille : D3Q19, $\Delta x = 0.3$ µm
- Interface : Free Energy (Shan-Chen)
- Rhéologie : MRT avec $\tau(\dot{\gamma})$, $n = 0.72$

**Conditions :**
- $Re = 40$, $We = 3.5$
- $T = 298$ K
- Hardware : NVIDIA A100 GPU

**Résultats :**
- Vitesse maximale de la goutte : 15.2 m/s (expérimental : 15.0 m/s)
- Diamètre de la goutte : 28 µm (erreur < 2 %)
- Temps de calcul : 2 h (vs 20 h sur CPU)

**Mécanisme :** La rhéofluidification réduit la viscosité dans le filament, accélérant le pincement. Le modèle Free Energy capture correctement la tension superficielle ($\sigma = 35$ mN/m).

### Hybridation VOF-LBM (Thiery et al., 2023)

**Objectif :** Combiner la précision interfaciale de VOF avec la scalabilité de LBM.

**Méthodologie :**
- VOF (PLIC) pour le suivi d'interface
- LBM (D2Q9) pour la résolution de Navier-Stokes
- Couplage : transfert de $\alpha$ et $\mathbf{v}$ entre les deux méthodes

**Résultats :**

| Modèle | Précision (µm) | Temps (h) | Scalabilité GPU |
|--------|----------------|-----------|-----------------|
| VOF seul | 0.5 | 10 | Moyenne |
| LBM seul | 1.2 | 2 | Excellente |
| Hybride VOF-LBM | 0.3 | 3 | Bonne |

---

## Limitations et Solutions

### Compressibilité Artificielle

**Problème :** La LBM simule un fluide faiblement compressible. Pour maintenir l'approximation incompressible :

$$Ma = \frac{u}{c_s} < 0.1$$

**Solution :** Utiliser des schémas à faible Mach (LBM à deux vitesses de relaxation, entropic LBM).

### Courants Parasites

**Problème :** Des courants de convection artificiels apparaissent aux interfaces (Shan-Chen).

**Solutions :**
- Modèle Free Energy (réduit les courants parasites de 90 %)
- Isotropie améliorée des opérateurs de gradient
- Schémas de discrétisation d'ordre supérieur

### Calibration Rhéologique

**Problème :** La relation $\nu(\tau)$ est linéaire, ce qui limite la gamme de viscosités simulables.

**Solution :** Matrices de relaxation multiple (MRT) avec des temps de relaxation séparés pour les moments impairs et pairs.

---

## Coût Computationnel

### Configuration Typique

Pour une simulation 3D (1 ms d'éjection, D3Q19) :

| Configuration | Grille | Temps (h) | Hardware |
|---------------|--------|-----------|----------|
| Standard | 100³ nœuds | 4–8 | 4 cœurs CPU |
| Haute résolution | 300³ nœuds | 1–2 | A100 GPU |
| Multi-GPU | 500³ nœuds | 0.5–1 | 4× A100 |

**Mémoire GPU :** ~16 GB pour 300³ nœuds en D3Q19 (19 distributions × 8 bytes × 27M nœuds)

---

## Références

> **Note** : Pour la liste complète des références, consultez la section **Bibliographie** dans le menu Annexes.

1. Chen, S., & Doolen, G. D. (1998). *Lattice Boltzmann method for fluid flows*. Annual Review of Fluid Mechanics, 30(1), 329-364. [DOI:10.1146/annurev.fluid.30.1.329](https://doi.org/10.1146/annurev.fluid.30.1.329)

2. Shan, X., & Chen, H. (1993). *Lattice Boltzmann model for simulating flows with multiple phases and components*. Physical Review E, 47(3), 1815. [DOI:10.1103/PhysRevE.47.1815](https://doi.org/10.1103/PhysRevE.47.1815)

3. Krüger, T., Kusumaatmaja, H., Kuzmin, A., Shardt, O., Silva, G., & Viggen, E. M. (2017). *The Lattice Boltzmann Method: Principles and Practice*. Springer. ISBN: 978-3-319-44649-3. [DOI:10.1007/978-3-319-44649-3](https://doi.org/10.1007/978-3-319-44649-3)

4. Huang, H., Sukop, M., & Lu, X. (2015). *Multiphase Lattice Boltzmann Methods: Theory and Application*. Wiley-Blackwell. ISBN: 978-1-118-97133-8.

5. Fakhari, A., & Rahimian, M. H. (2010). *Phase-field modeling by the method of lattice Boltzmann equations*. Physical Review E, 81(3), 036707. [DOI:10.1103/PhysRevE.81.036707](https://doi.org/10.1103/PhysRevE.81.036707)
