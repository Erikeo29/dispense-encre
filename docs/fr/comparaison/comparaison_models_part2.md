---

## 3. Analyse Critique par Modèle

### 3.1 FEM (Finite Element Method / Phase-Field)

**En bref :** On découpe le domaine en éléments (triangles en 2D, tétraèdres en 3D) et on résout les équations de Navier-Stokes sur chaque élément. L'interface encre/air est représentée par un "champ de phase" $\phi$ qui varie progressivement de -1 (air) à +1 (encre).

| ✅ Points forts | ⚠️ Limitations |
|----------------|----------------|
| Précision exceptionnelle (jusqu'à 0.05 µm) | Temps de calcul élevé en 3D |
| Maillage adaptatif (fin où nécessaire) | Nécessite des ressources mémoire importantes |
| Couple facilement plusieurs physiques | Sensible aux paramètres de stabilisation |
| Logiciels : COMSOL (commercial), FEniCS (open-source) | |

---

### 3.2 VOF (Volume of Fluid)

**En bref :** Chaque cellule du maillage contient une fraction volumique $\alpha$ entre 0 (100% air) et 1 (100% encre). L'interface est reconstruite géométriquement à chaque pas de temps (méthode PLIC).

| ✅ Points forts | ⚠️ Limitations |
|----------------|----------------|
| Standard industriel depuis 30 ans | Interface parfois "diffuse" numériquement |
| Conservation de masse parfaite | Coût mémoire élevé pour maillages très fins |
| Très robuste et bien documenté | Coalescence de gouttes difficile à gérer |
| Logiciels : OpenFOAM (open-source), Fluent (commercial) | |

---

### 3.3 LBM (Lattice Boltzmann Method)

**En bref :** Au lieu de résoudre directement Navier-Stokes, on simule des "paquets de particules" qui se déplacent et collisionnent sur une grille régulière. Les propriétés macroscopiques (vitesse, pression) émergent statistiquement.

| ✅ Points forts | ⚠️ Limitations |
|----------------|----------------|
| Parallélisation GPU exceptionnelle (×20) | Compressibilité artificielle (limiter Ma < 0.1) |
| Grille simple, pas de maillage complexe | Précision sub-micronique difficile |
| Algorithme local (chaque cellule indépendante) | Calibration rhéologique délicate |
| Logiciels : Palabos (open-source), waLBerla | Documentation moins abondante que VOF |

---

### 3.4 SPH (Smoothed Particle Hydrodynamics)

**En bref :** Le fluide est représenté par des particules qui se déplacent librement. Chaque particule "sent" ses voisines via un noyau d'interpolation (comme un champ d'influence autour d'elle).

| ✅ Points forts | ⚠️ Limitations |
|----------------|----------------|
| Pas de maillage → pas de déformation | Bruit numérique dans les champs de pression |
| Coalescence et fragmentation naturelles | Instabilités à haute vitesse |
| Adapté aux grandes déformations | Moins mature que les méthodes eulériennes |
| Logiciels : PySPH (Python), DualSPHysics | Coût mémoire élevé en 3D |

---

## 4. Tableau de Synthèse

Ce tableau résume les caractéristiques clés pour vous aider à choisir la méthode adaptée à votre cas :

| Critère | FEM | VOF | LBM | SPH |
|---------|-----|-----|-----|-----|
| **Précision interface** | 0.05–0.5 µm | 0.1–1 µm | 0.2–2 µm | 0.5–5 µm |
| **Temps de calcul typique** | 10–50 h | 2–10 h | 1–5 h | 5–20 h |
| **Conservation masse** | Bonne (ajustement) | Parfaite | Approximative | Par sommation |
| **Rhéologie Carreau** | ✓ Natif | ✓ Natif | ✓ Possible | ✓ Possible |
| **Accélération GPU** | Limitée | Bonne | Excellente (×20) | Bonne |
| **Courbe d'apprentissage** | Moyenne (GUI avec COMSOL) | Difficile (C++, CLI) | Difficile (physique spécifique) | Moyenne (Python) |
| **Maturité industrielle** | Haute | Très haute | Moyenne | En développement |
| **Coût logiciel** | COMSOL ~10k€/an ou FEniCS gratuit | OpenFOAM gratuit | Palabos gratuit | PySPH gratuit |

### Quelle méthode choisir ?

| Votre situation | Méthode recommandée | Pourquoi |
|-----------------|---------------------|----------|
| Production industrielle, besoin de robustesse | **VOF** (OpenFOAM) | Standard éprouvé, grande communauté |
| Couplage multiphysique (thermique, électrique...) | **FEM** (COMSOL ou FEniCS) | Conçu pour le couplage |
| Calculs intensifs, nombreuses simulations | **LBM** (Palabos) | Le plus rapide sur GPU |
| Recherche académique, nouvelles physiques | **SPH** (PySPH) | Flexible, facile à modifier |

---

## 5. Besoins Hardware

### 5.1 Comprendre les besoins

Pour simuler 1 milliseconde de dispense avec environ 1 million de cellules/particules, voici ce qu'il faut prévoir :

| Modèle | Processeur (CPU) | Carte graphique (GPU) | Mémoire vive (RAM) | Temps estimé |
|--------|------------------|----------------------|--------------------| -------------|
| **FEM** | Puissant (64-128 cœurs) | Peu utile | Beaucoup (64-128 Go) | 10-50 heures |
| **VOF** | Moyen (16-32 cœurs) | Utile pour accélérer | Moyen (16-32 Go) | 2-10 heures |
| **LBM** | Modeste (4-8 cœurs) | Indispensable (haute gamme) | Modeste (8-16 Go) | 1-5 heures |
| **SPH** | Moyen (8-16 cœurs) | Très utile | Élevée (32-64 Go) | 5-20 heures |

### 5.2 Traduction en budget

| Gamme | Exemples de configuration | Budget approximatif | Adapté pour |
|-------|---------------------------|---------------------|-------------|
| **Entrée de gamme** | PC de bureau avec GPU milieu de gamme (ex: GTX 1660, 8 Go VRAM) | 1 000 – 2 000 € | LBM/SPH simples, VOF maillage grossier |
| **Milieu de gamme** | Workstation avec GPU gaming (ex: RTX 3080/4070, 12-16 Go VRAM) | 3 000 – 6 000 € | VOF, LBM, SPH standard |
| **Haut de gamme** | Serveur multi-cœurs ou GPU professionnel (ex: RTX 4090, A100) | 10 000 – 30 000 € | FEM 3D, études paramétriques |
| **Cloud** | Location à l'heure (AWS, Google Cloud, Azure) | 1-10 €/heure | Calculs ponctuels intensifs |

### 5.3 Conseil pratique

- **LBM** tire le meilleur parti des GPU : avec une carte graphique à 500€, vous pouvez obtenir des performances équivalentes à un serveur CPU à 5000€
- **FEM** reste gourmand en CPU et RAM : privilégiez un serveur de calcul partagé ou le cloud
- **VOF** et **SPH** sont de bons compromis : ils tournent bien sur un PC de bureau moderne

---

## 6. Références

> **Note** : Pour la liste complète des références scientifiques, consultez la section **Bibliographie** dans le menu Annexes.
