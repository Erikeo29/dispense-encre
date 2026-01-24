**Sommaire :**
1. Principe général des 4 modèles
2. Approches de discrétisation
3. Analyse critique par modèle
4. Besoins hardware
5. Tableau de synthèse
6. Références

---

## 1. Principe général des 4 modèles

Cette section présente les quatre méthodes numériques utilisées pour simuler la dispense d'encre rhéofluidifiante dans des micro-puits.

| Modèle | Principe | Caractéristique principale |
|--------|----------|---------------------------|
| **FEM** | Discrétisation en éléments finis avec champ de phase $\phi$ pour le suivi d'interface | Précision locale élevée, couplage multiphysique natif |
| **VOF** | Suivi d'interface via fraction volumique $\alpha \in [0,1]$ sur maillage eulérien | Standard industriel, conservation de masse rigoureuse |
| **LBM** | Résolution de l'équation de Boltzmann sur grille régulière | Parallélisation GPU optimale, rapidité de calcul |
| **SPH** | Méthode particulaire lagrangienne sans maillage | Gestion naturelle des grandes déformations |

---

## 2. Approches de discrétisation : eulérien vs lagrangien

### 2.1 Classification des méthodes

Les méthodes numériques pour la simulation de fluides se divisent en deux familles selon le traitement de l'espace :

| Approche | Principe | Avantage | Méthodes |
|----------|----------|----------|----------|
| **Eulérienne** | Maillage fixe, le fluide traverse les cellules | Stabilité, implémentation directe | FEM, VOF, LBM |
| **Lagrangienne** | Particules mobiles suivant le fluide | Suivi naturel des déformations | SPH |

L'approche eulérienne observe le fluide depuis un référentiel fixe, tandis que l'approche lagrangienne suit les éléments de fluide dans leur mouvement.

### 2.2 Visualisation des 4 approches

Les figures ci-dessous illustrent les structures de discrétisation utilisées **dans cette étude** sur la géométrie de référence (puit : 800 µm × 130 µm) :

#### FEM - Maillage triangulaire adaptatif
- Éléments triangulaires de taille variable (1-10 µm dans cette étude)
- Raffinement local aux zones critiques (interface, parois)

#### VOF - Maillage hexaédrique
- Cellules rectangulaires (résolution ~5 µm dans cette étude)
- Fraction volumique $\alpha$ dans chaque cellule

#### LBM - Grille uniforme
- Grille cartésienne régulière (5 µm/cellule dans cette étude)
- Propriétés macroscopiques obtenues par moments statistiques

#### SPH - Distribution particulaire
- Environ 1000 particules dans cette étude (valeur dépendante de la résolution souhaitée)
- Interpolation via noyaux (cubic spline, Wendland)


