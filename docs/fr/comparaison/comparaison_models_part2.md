---

## 3. Analyse Critique par Modèle

### 3.1 FEM (Finite Element Method / Phase-Field)

Méthode des éléments finis avec formulation faible des équations de Navier-Stokes. L'interface encre/air est représentée par un champ de phase $\phi$ variant de -1 (air) à +1 (encre) sur une épaisseur caractéristique $\varepsilon$.

| Avantages | Limitations |
|-----------|-------------|
| Précision interfaciale : 0.05–0.5 µm | Temps de calcul plus long que VOF/LBM |
| Maillage adaptatif selon le gradient de $\phi$ | Consommation mémoire importante en 3D |
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
| Parallélisation GPU exceptionnelle (facteur ×10-20) | Compressibilité artificielle (contrainte Ma < 0.1) |
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
| **Temps de calcul (ordre de grandeur)** | 10–50 h | 2–10 h | 1–5 h | 2–20 h |
| **Conservation masse** | Ajustement numérique | Rigoureuse | Approximative | Par sommation |
| **Rhéologie Carreau** | Natif | Natif | Implémentable | Implémentable |
| **Accélération GPU** | Limitée | Bonne | Excellente (×10-20) | Bonne (×10-15) |
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

### 5.1 Ordres de grandeur

Les temps de calcul dépendent fortement de la résolution et de la durée simulée. Pour une simulation 2D typique de dispense (20-40 ms de temps physique) :

| Modèle | Processeur | Carte graphique | Mémoire vive | Temps (ordre de grandeur) |
|--------|------------|-----------------|--------------|---------------------------|
| **FEM** | 8-32 cœurs | Peu exploitée | 16-64 Go | Quelques heures à dizaines d'heures |
| **VOF** | 8-16 cœurs | Accélération utile | 8-32 Go | Quelques heures |
| **LBM** | 4-8 cœurs | Fortement recommandée | 8-16 Go | 1-5 heures |
| **SPH** | 8-16 cœurs | Recommandée | 16-64 Go | Quelques heures |

### 5.2 Configurations indicatives

| Gamme | Configuration type | Budget indicatif | Utilisation |
|-------|-------------------|------------------|-------------|
| **Station de travail** | 12-32 cœurs, 32-64 Go RAM, GPU 8-16 Go VRAM | 3 000–8 000 € | Toutes méthodes en 2D, études paramétriques |
| **Serveur de calcul** | 64+ cœurs, 128+ Go RAM | 10 000–30 000 € | FEM/VOF 3D, grandes séries |
| **Cloud** | AWS, Google Cloud, Azure | 1-10 €/h | Calculs ponctuels intensifs |

### 5.3 Remarques pratiques

- **LBM** exploite efficacement les GPU : une carte graphique grand public peut offrir des performances comparables à un serveur multi-cœurs
- **FEM** et **VOF** peuvent être exécutés sur des stations de travail pour des cas 2D ; le cloud est utile pour les études 3D ou les grandes séries paramétriques
- **SPH** fonctionne bien sur station de travail avec GPU

---

## 6. Références

> Pour la liste complète des références scientifiques, consulter la section **Bibliographie** dans le menu Annexes.
