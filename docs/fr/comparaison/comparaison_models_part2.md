---

## 3. Analyse Critique par Modèle

### 3.1 FEM (Finite Element Method / Phase-Field)

Méthode des éléments finis avec formulation faible des équations de Navier-Stokes. L'interface encre/air est représentée par un champ de phase $\phi$ variant de -1 (air) à +1 (encre) sur une épaisseur caractéristique $\varepsilon$.

| Avantages | Limitations |
|-----------|-------------|
| Précision interfaciale : 0.05–0.5 µm | Temps de calcul élevé en 3D |
| Maillage adaptatif selon le gradient de $\phi$ | Consommation mémoire importante |
| Couplage multiphysique natif | Sensibilité aux paramètres de stabilisation |
| Logiciels : COMSOL (commercial), FEniCS (open-source) | |

---

### 3.2 VOF (Volume of Fluid)

Méthode eulérienne où chaque cellule contient une fraction volumique $\alpha \in [0,1]$. L'interface est reconstruite géométriquement via l'algorithme PLIC (Piecewise Linear Interface Construction).

| Avantages | Limitations |
|-----------|-------------|
| Conservation de masse rigoureuse | Diffusion numérique aux interfaces fines |
| Standard industriel depuis 30 ans | Coût mémoire pour maillages fins |
| Documentation et communauté étendues | Coalescence de gouttes difficile |
| Logiciels : OpenFOAM (open-source), Fluent (commercial) | |

---

### 3.3 LBM (Lattice Boltzmann Method)

Méthode mésoscopique résolvant l'équation de Boltzmann discrétisée sur grille régulière (D2Q9, D3Q19). Les grandeurs macroscopiques (vitesse, pression) sont obtenues par calcul des moments statistiques.

| Avantages | Limitations |
|-----------|-------------|
| Parallélisation GPU exceptionnelle (facteur ×20) | Compressibilité artificielle (contrainte Ma < 0.1) |
| Algorithme local (chaque nœud indépendant) | Précision sub-micronique difficile |
| Pas de maillage complexe à générer | Calibration rhéologique délicate |
| Logiciels : Palabos (open-source), waLBerla | Documentation moins fournie que VOF |

---

### 3.4 SPH (Smoothed Particle Hydrodynamics)

Méthode lagrangienne sans maillage. Le fluide est discrétisé en particules dont les propriétés sont interpolées via des noyaux de lissage (cubic spline, Wendland).

| Avantages | Limitations |
|-----------|-------------|
| Pas de maillage : pas de problème de distorsion | Bruit numérique dans les champs de pression |
| Coalescence et fragmentation naturelles | Instabilités tensorielles à haute vitesse |
| Adapté aux grandes déformations | Maturité industrielle moindre |
| Logiciels : PySPH (Python), DualSPHysics | Coût mémoire élevé en 3D |

---

## 4. Tableau de Synthèse

| Critère | FEM | VOF | LBM | SPH |
|---------|-----|-----|-----|-----|
| **Précision interface** | 0.05–0.5 µm | 0.1–1 µm | 0.2–2 µm | 0.5–5 µm |
| **Temps de calcul typique** | 10–50 h | 2–10 h | 1–5 h | 5–20 h |
| **Conservation masse** | Ajustement numérique | Rigoureuse | Approximative | Par sommation |
| **Rhéologie Carreau** | Natif | Natif | Implémentable | Implémentable |
| **Accélération GPU** | Limitée | Bonne | Excellente (×20) | Bonne |
| **Courbe d'apprentissage** | Moyenne (GUI disponible) | Élevée (C++, CLI) | Élevée (physique spécifique) | Moyenne (Python) |
| **Maturité industrielle** | Haute | Très haute | Moyenne | En développement |
| **Coût logiciel** | COMSOL ~10k€/an, FEniCS gratuit | OpenFOAM gratuit | Palabos gratuit | PySPH gratuit |

### Recommandations selon le contexte applicatif

| Contexte | Méthode recommandée | Justification |
|----------|---------------------|---------------|
| Production industrielle | VOF (OpenFOAM) | Robustesse éprouvée, large communauté |
| Couplage multiphysique | FEM (COMSOL, FEniCS) | Architecture native pour le couplage |
| Études paramétriques intensives | LBM (Palabos) | Performance GPU optimale |
| Recherche fondamentale | SPH (PySPH) | Flexibilité pour nouvelles physiques |

---

## 5. Besoins Hardware

### 5.1 Ressources par modèle

Pour une simulation de référence (1 ms de dispense, ~10⁶ cellules/particules) :

| Modèle | Processeur | Carte graphique | Mémoire vive | Temps estimé |
|--------|------------|-----------------|--------------|--------------|
| **FEM** | 64-128 cœurs | Peu exploitée | 64-128 Go | 10-50 h |
| **VOF** | 16-32 cœurs | Accélération possible | 16-32 Go | 2-10 h |
| **LBM** | 4-8 cœurs | Indispensable (haute gamme) | 8-16 Go | 1-5 h |
| **SPH** | 8-16 cœurs | Recommandée | 32-64 Go | 5-20 h |

### 5.2 Configurations types

| Gamme | Configuration | Budget indicatif | Utilisation |
|-------|---------------|------------------|-------------|
| **Entrée** | PC bureau, GPU 8 Go VRAM (ex: GTX 1660) | 1 000–2 000 € | LBM/SPH simples, VOF maillage grossier |
| **Intermédiaire** | Workstation, GPU 12-16 Go VRAM (ex: RTX 3080) | 3 000–6 000 € | VOF, LBM, SPH standard |
| **Haute performance** | Serveur multi-cœurs ou GPU 24+ Go (ex: RTX 4090, A100) | 10 000–30 000 € | FEM 3D, études paramétriques |
| **Cloud** | AWS, Google Cloud, Azure | 1-10 €/h | Calculs ponctuels intensifs |

### 5.3 Considérations pratiques

- **LBM** exploite de manière optimale les architectures GPU : une carte graphique à 500 € peut égaler un serveur CPU à 5 000 €
- **FEM** nécessite principalement des ressources CPU et mémoire : le recours au cloud ou à des clusters de calcul est souvent préférable
- **VOF** et **SPH** offrent un bon compromis et fonctionnent efficacement sur des stations de travail modernes

---

## 6. Références

> Pour la liste complète des références scientifiques, consulter la section **Bibliographie** dans le menu Annexes.
