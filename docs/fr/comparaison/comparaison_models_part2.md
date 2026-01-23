---

## 3. Analyse Critique par Modèle

### 3.1 VOF (Volume of Fluid)

**Principe :** Fraction volumique $\alpha$ ($0 \leq \alpha \leq 1$) représente la proportion de fluide dans chaque cellule.

| Points forts | Limitations |
|--------------|-------------|
| Robustesse éprouvée (standard industriel) | Diffusivité numérique aux interfaces fines |
| Conservation de masse parfaite | Coût mémoire élevé pour maillages fins |
| Implémentations open-source matures (OpenFOAM, Basilisk) | Coalescences multiples difficiles |
| Précision interfaciale 0.1–1 µm avec PLIC | |

---

### 3.2 FEM / Phase-Field

**Principe :** Éléments finis avec formulation faible. Interface représentée par un champ de phase $\phi$ d'épaisseur $\varepsilon$.

| Points forts | Limitations |
|--------------|-------------|
| Précision locale 0.05–0.5 µm | Coût computationnel élevé en 3D |
| Géométries complexes et couplage multiphysique | Interfaces libres difficiles sans hybridation |
| Implémentations commerciales (COMSOL, Ansys) | Sensibilité aux paramètres de stabilisation |

---

### 3.3 LBM (Lattice Boltzmann)

**Principe :** Équation de Boltzmann discrétisée sur grille régulière (D2Q9, D3Q19). Grandeurs macroscopiques par moments statistiques.

| Points forts | Limitations |
|--------------|-------------|
| Scalabilité GPU exceptionnelle (x20 vs CPU) | Compressibilité artificielle ($Ma < 0.1$) |
| Parallélisation massive | Précision sub-micronique difficile |
| Implémentations open-source (Palabos, waLBerla) | Calibration rhéologique délicate |

---

### 3.4 SPH (Smoothed Particle Hydrodynamics)

**Principe :** Méthode sans maillage avec particules mobiles. Navier-Stokes résolues via noyaux d'interpolation (cubic spline).

| Points forts | Limitations |
|--------------|-------------|
| Déformations extrêmes (coalescence, fragmentation) | Bruit numérique (pression, vitesse) |
| Pas de maillage → pas de distorsion | Instabilité tenseur contraintes haute vitesse |
| Open-source (DualSPHysics, PySPH) | Coût mémoire élevé en 3D |

---

## 4. Tableau de Synthèse

| Critère | VOF | FEM | LBM | SPH |
|---------|-----|-----|-----|-----|
| **Précision interfaciale** | 0.1–1 µm | 0.05–0.5 µm | 0.2–2 µm | 0.5–5 µm |
| **Temps de calcul** | 2–10 h | 10–50 h | 1–5 h | 5–20 h |
| **Conservation masse** | Parfaite | Ajustement | Approximative | Sommation |
| **Rhéologie Carreau** | ✓ | ✓ | ✓ | ✓ |
| **Parallélisation GPU** | Bonne | Limitée | Excellente | Bonne |
| **Facilité d'utilisation** | Élevée | Moyenne | Moyenne | Moyenne |
| **Maturité industrielle** | Très haute | Haute | Moyenne | Faible |

**Recommandations :**
- **Inkjet standard** (< 1200 dpi) → **VOF** (robustesse + précision)
- **Haute résolution** (> 2400 dpi) → **Hybride VOF-LBM** (précision + vitesse)
- **Encres viscoélastiques** → **FEM** (lois rhéologiques complexes)
- **R&D académique** → **SPH** (flexibilité, nouvelles physiques)

---

## 5. Besoins Hardware

Pour une simulation standard (1 ms d'éjection, 10⁶ cellules/particules) :

| Modèle | CPU (cœurs) | GPU | Mémoire (GB) | Temps (h) |
|--------|-------------|-----|--------------|-----------|
| **VOF** | 16–32 | RTX 3080–4090 | 16–32 | 2–10 |
| **FEM** | 64–128 | Peu efficace | 64–128 | 10–50 |
| **LBM** | 4–8 | A100 (40 GB) | 8–16 | 1–5 |
| **SPH** | 8–16 | RTX 4090 (24 GB) | 32–64 | 5–20 |

**Scalabilité :**
- **LBM** : le plus efficace sur GPU (x20 vs CPU)
- **FEM** : limité par CPU multi-cœurs et mémoire
- **VOF / SPH** : bon compromis GPU grand public

---

## 6. Références

> **Note** : Pour la liste complète des références, consultez la section **Bibliographie** dans le menu Annexes.
