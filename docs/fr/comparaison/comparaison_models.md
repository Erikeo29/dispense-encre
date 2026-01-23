**Sommaire :**
1. Principe Général des 4 Modèles
2. Approches de Discrétisation
3. Analyse Critique par Modèle
4. Tableau de Synthèse
5. Besoins Hardware
6. Références

---

## 1. Principe Général des 4 Modèles

Cette section présente les quatre méthodes numériques utilisées pour simuler la dispense d'encre rhéofluidifiante dans des micro-puits.

| Modèle | Principe | Highlights |
|--------|----------|------------|
| **FEM** | Éléments finis avec champ de phase $\phi$ pour suivre l'interface | Précision locale exceptionnelle (0.05 µm), couplage multiphysique natif |
| **VOF** | Fraction volumique $\alpha \in [0,1]$ sur maillage eulérien fixe | Standard industriel, conservation de masse parfaite, robuste |
| **LBM** | Équation de Boltzmann discrétisée sur grille régulière | Scalabilité GPU x20, parallélisation massive, très rapide |
| **SPH** | Particules mobiles sans maillage, noyaux d'interpolation | Grandes déformations naturelles, coalescence/fragmentation facile |

---

## 2. Approches de Discrétisation : Eulérien vs Lagrangien

### 2.1 Concept Fondamental

| Approche | Description | Méthodes |
|----------|-------------|----------|
| **Eulérienne** | Maillage **fixe** dans l'espace. Le fluide traverse les cellules. | FEM, VOF, LBM |
| **Lagrangienne** | Particules **mobiles** qui suivent le fluide. Pas de maillage. | SPH |

### 2.2 Visualisation des 4 Approches

Les images ci-dessous illustrent les structures de discrétisation sur une géométrie comparable (puit 0.8 mm × 0.13 mm) :

#### FEM - Maillage Triangulaire Adaptatif
- Triangles de taille variable (1-10 µm), raffinement près des parois et de l'interface

#### VOF - Maillage Hexaédrique
- Cellules rectangulaires avec raffinement adaptatif (AMR)

#### LBM - Grille Uniforme
- Grille cartésienne régulière (1 cellule = 5 µm = 1 l.u.)

#### SPH - Particules Discrètes
- ~1000 particules avec rayon d'influence h
