**Sommaire :**
1. Synthèse des Performances
2. Tableau Comparatif Global
3. Approches de Discrétisation
4. Adaptabilité aux Encres Rhéofluidifiantes
5. Analyse Critique par Modèle
6. Défis Communs et Solutions
7. Recommandations par Application
8. Besoins Hardware Détaillés
9. Références

---

## 1. Synthèse des Performances

Cette section présente une comparaison exhaustive des quatre méthodes numériques pour la simulation de dispense de microgouttes d'encre rhéofluidifiante, basée sur une méta-analyse de 62 études publiées entre 2010 et 2025.

---

## 2. Tableau Comparatif Global

| Critère | VOF | FEM | LBM | SPH |
|---------|-----|-----|-----|-----|
| **Précision interfaciale** | 0.1–1 µm (PLIC) | 0.05–0.5 µm (éléments adaptatifs) | 0.2–2 µm (Free Energy) | 0.5–5 µm (CSF artificielle) |
| **Temps de calcul** | 2–10 h (CPU) / 30 min (GPU) | 10–50 h (multi-core) | 1–5 h (GPU) | 5–20 h (GPU) |
| **Support rhéologique** | Loi de puissance, Carreau-Yasuda | Herschel-Bulkley, Oldroyd-B | Loi de puissance, Oldroyd-B | Loi de puissance, viscoélastique |
| **Hardware requis** | 10–50 TFLOPS (GPU modéré) | 20–100 TFLOPS (CPU multi-core) | 5–30 TFLOPS (GPU haute perf.) | 10–40 TFLOPS (GPU modéré) |
| **Avantages** | Robustesse, précision interfaciale | Précision locale, couplage multiphysique | Scalabilité GPU, rapidité | Adaptabilité, coalescence naturelle |
| **Limitations** | Diffusivité numérique, coût mémoire | Maillages déformables coûteux | Compressibilité artificielle | Bruit numérique, instabilité tenseur |
| **Citations moyennes** | 250 | 180 | 320 | 210 |

---

## 3. Approches de Discrétisation : Eulérien vs Lagrangien

### 3.1 Concept Fondamental

Les méthodes numériques pour la simulation de fluides se divisent en deux grandes familles selon leur traitement de l'espace :

| Approche | Description | Méthodes |
|----------|-------------|----------|
| **Eulérienne** | Maillage/grille **fixe** dans l'espace. Le fluide "traverse" les cellules. | FEM, VOF, LBM |
| **Lagrangienne** | Particules **mobiles** qui se déplacent avec le fluide. Pas de maillage fixe. | SPH |

### 3.2 Visualisation des 4 Approches

Les images ci-dessous illustrent les différentes structures de discrétisation utilisées par chaque méthode, sur une géométrie comparable (puit de 0.8 mm × 0.13 mm) :

#### FEM - Maillage Triangulaire Adaptatif
- **Type** : Eulérien
- **Éléments** : Triangles de taille variable (1-10 µm)
- **Avantage** : Raffinement local près des zones critiques (parois, interface)

#### VOF - Maillage Hexaédrique avec AMR
- **Type** : Eulérien
- **Éléments** : Cellules rectangulaires avec raffinement adaptatif (AMR)
- **Avantage** : Conservation de masse stricte, robustesse industrielle

#### LBM - Grille Uniforme
- **Type** : Eulérien
- **Éléments** : Grille cartésienne régulière (1 cellule = 5 µm = 1 l.u.)
- **Avantage** : Simplicité, parallélisation GPU excellente

#### SPH - Particules Discrètes
- **Type** : Lagrangien
- **Éléments** : Particules (~1000) avec rayon d'influence h
- **Avantage** : Pas de maillage à déformer, adapté aux grandes déformations

### 3.3 Implications Pratiques

| Aspect | Eulérien (FEM/VOF/LBM) | Lagrangien (SPH) |
|--------|------------------------|------------------|
| **Interface** | Reconstruction nécessaire (VOF: PLIC, FEM: Phase-Field) | Implicite via densité de particules |
| **Déformations** | Limitées (remaillage si excessif) | Naturelles |
| **Conservation masse** | Par construction (VOF) ou ajustement | Via sommation des particules |
| **Parallélisation** | Excellente (surtout LBM) | Bonne mais plus complexe |
