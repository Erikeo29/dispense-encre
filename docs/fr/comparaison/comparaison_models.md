**Sommaire :**
1. Principe Général des 4 Modèles
2. Approches de Discrétisation
3. Analyse Critique par Modèle
4. Tableau de Synthèse
5. Besoins Hardware
6. Références

---

## 1. Principe Général des 4 Modèles

Cette section présente les quatre méthodes numériques utilisées pour simuler la dispense d'encre rhéofluidifiante dans des micro-puits. Chaque méthode a ses forces et ses faiblesses selon le contexte d'utilisation.

| Modèle | Principe en une phrase | Ce qui le distingue |
|--------|------------------------|---------------------|
| **FEM** | Découpe le domaine en petits triangles/tétraèdres et résout les équations sur chaque élément | Très précis localement, idéal pour coupler plusieurs physiques (thermique, électrique...) |
| **VOF** | Suit l'interface encre/air via une fraction volumique $\alpha$ (0 = air, 1 = encre) | Référence industrielle, conserve parfaitement la masse, très robuste |
| **LBM** | Simule le fluide comme des "paquets de particules" sur une grille régulière | Extrêmement rapide sur GPU, parallélisation naturelle |
| **SPH** | Représente le fluide par des particules qui se déplacent librement | Gère naturellement les grandes déformations et la fragmentation |

---

## 2. Approches de Discrétisation : Eulérien vs Lagrangien

### 2.1 Deux grandes familles

En simulation numérique, on distingue deux philosophies fondamentales :

| Approche | Comment ça marche ? | Avantage principal | Méthodes |
|----------|---------------------|-------------------|----------|
| **Eulérienne** | Le maillage reste **fixe**, le fluide "coule à travers" les cellules | Simple à implémenter, stable | FEM, VOF, LBM |
| **Lagrangienne** | Les particules **bougent avec** le fluide, pas de maillage fixe | Suit naturellement les déformations | SPH |

**Analogie :** Imaginez observer une rivière. L'approche eulérienne revient à placer des capteurs fixes sur les berges. L'approche lagrangienne revient à suivre des bouchons qui flottent sur l'eau.

### 2.2 Visualisation des 4 Approches

Les images ci-dessous montrent comment chaque méthode "voit" la même géométrie (puit de 800 µm × 130 µm) :

#### FEM - Maillage Triangulaire Adaptatif
- Petits triangles là où c'est important (interface, parois), grands triangles ailleurs
- Taille des éléments : 1 à 10 µm selon la zone

#### VOF - Maillage Rectangulaire
- Cellules carrées/rectangulaires uniformes ou avec raffinement local (AMR)
- Chaque cellule contient une fraction d'encre entre 0 et 1

#### LBM - Grille Uniforme
- Grille régulière très simple (ici : 1 cellule = 5 µm)
- La physique émerge des collisions entre "paquets de particules"

#### SPH - Nuage de Particules
- Environ 1000 particules mobiles
- Chaque particule "influence" ses voisines dans un rayon h


