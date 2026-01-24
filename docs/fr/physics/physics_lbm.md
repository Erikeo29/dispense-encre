**Sommaire :**
1. Principe de la méthode
2. Équations fondamentales
3. Formulation mathématique
4. Avantages et limitations
5. Coût computationnel
6. Bibliothèques open-source
7. Références

---

## 1. Principe de la méthode

La méthode **LBM (Lattice Boltzmann Method)** est une approche **mésoscopique** qui ne résout pas directement les équations de Navier-Stokes, mais l'**équation de Boltzmann discrétisée** sur un réseau régulier (lattice).

### Variable principale : fonctions de distribution f_i

On suit l'évolution de fonctions de distribution f_i(**x**, t) représentant la probabilité de trouver des particules à la position **x** se déplaçant selon des directions discrètes **c**_i.

Les grandeurs macroscopiques sont obtenues par **moments statistiques** :

$$\rho = \sum_i f_i \quad \text{et} \quad \rho \mathbf{u} = \sum_i f_i \mathbf{c}_i$$

**Avantage clé :** Parallélisation massive sur GPU (chaque nœud est indépendant).

---

## 2. Équations fondamentales

### 2.1 Équation de Boltzmann discrète (BGK)

$$f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = -\frac{1}{\tau}(f_i - f_i^{eq}) + F_i$$

où :
- τ = temps de relaxation
- f_i^eq = distribution d'équilibre de Maxwell-Boltzmann
- F_i = terme de force externe

### 2.2 Distribution d'équilibre

$$f_i^{eq} = w_i \rho \left[1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2c_s^4} - \frac{\mathbf{u}^2}{2c_s^2}\right]$$

avec c_s = 1/√3 la vitesse du son sur le réseau et w_i les poids de quadrature.

### 2.3 Lien viscosité - temps de relaxation

$$\nu = c_s^2 \left(\tau - \frac{1}{2}\right) \Delta t$$

Cette relation permet de modéliser des fluides de viscosités différentes en ajustant τ.

---

## 3. Formulation mathématique

### 3.1 Grilles de discrétisation (DdQq)

| Grille | Dimensions | Vitesses | Application |
|--------|------------|----------|-------------|
| **D2Q9** | 2D | 9 | Standard 2D |
| **D3Q19** | 3D | 19 | Standard 3D (bon compromis) |
| **D3Q27** | 3D | 27 | Haute précision |

**Choix typique :** D3Q19 avec Δx = 0.3–5 µm

### 3.2 Modèle multiphasique Shan-Chen

La force interparticulaire modélise les interactions entre fluides :

$$\mathbf{F}_{int}(\mathbf{x}) = -G\psi(\mathbf{x}) \sum_i w_i \psi(\mathbf{x} + \mathbf{c}_i \Delta t) \mathbf{c}_i$$

où G contrôle la tension superficielle et ψ est le pseudopotentiel.

**Tension superficielle :** σ ∝ G(ψ_max - ψ_min)²

### 3.3 Fluides non-newtoniens

Pour les fluides rhéofluidifiants, τ dépend localement du taux de cisaillement :

$$\tau(\dot{\gamma}) = \frac{1}{2} + \frac{\nu(\dot{\gamma})}{c_s^2 \Delta t}$$

### 3.4 Gestion du mouillage

Les angles de contact sont gérés par une **densité fictive** aux nœuds solides :

$$\rho_{solid} = \rho_0 + \Delta \rho \cdot \cos(\theta_{eq})$$

Le mouillage est géré naturellement sans conditions aux limites explicites.

---

## 4. Avantages et limitations

| Avantages | Limitations |
|-----------|-------------|
| Scalabilité GPU exceptionnelle (x20) | Compressibilité artificielle (Ma < 0.1) |
| Parallélisation intrinsèque | Courants parasites aux interfaces |
| Mouillage naturel (géométries complexes) | Calibration rhéologique délicate |
| Coalescence/rupture automatiques | Mémoire GPU limitante en 3D |
| Précision interfaciale ~1 µm | Rapport de densité limité (~1000) |

---

## 5. Coût computationnel

| Configuration | Grille | Temps | Hardware |
|---------------|--------|-------|----------|
| 2D standard (D2Q9) | 1000² | 1–2 h | 4 cœurs CPU |
| 3D standard (D3Q19) | 300³ | 1–2 h | 1× A100 GPU |
| 3D haute résolution | 500³ | 0.5–1 h | 4× A100 GPU |

**Scalabilité GPU :** Quasi-linéaire jusqu'à 16 GPUs.

**Mémoire GPU :** ~16 GB pour 300³ nœuds en D3Q19.

---

## 6. Bibliothèques open-source

| Bibliothèque | Langage | GPU | Focus |
|--------------|---------|-----|-------|
| **Palabos** | C++ | MPI | Référence open-source, tutoriels |
| **OpenLB** | C++ | CUDA/OpenMP | Applications industrielles |
| **waLBerla** | C++ | CUDA | HPC extrême, millions de cœurs |
| **Sailfish** | Python/CUDA | CUDA natif | Interface Python |

---

## 7. Références

> **Note** : Pour la liste complète des références, consultez la section **Bibliographie** dans le menu Annexes.

