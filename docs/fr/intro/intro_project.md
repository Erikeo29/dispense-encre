# Modélisation de la Dispense de Fluides Rhéofluidifiants

## Contexte Scientifique et Industriel

### Technologies de Dispense Microfluidique

La dispense de fluides en microfluidique englobe un ensemble de techniques permettant le dépôt contrôlé de volumes de l'ordre du nanolitre au microlitre. Ces procédés trouvent des applications dans de nombreux domaines :

**Applications industrielles :**
- Fabrication de capteurs électrochimiques (dépôt d'encres conductrices)
- Électronique imprimée (circuits conducteurs, antennes RFID)
- Bioprinting et dépôt de biomatériaux
- Revêtements fonctionnels et couches minces
- Dosage pharmaceutique de précision

### Mécanismes Physiques

La dispense de fluides implique plusieurs phénomènes physiques couplés :
- **Écoulement diphasique** : interaction fluide/air à l'interface
- **Capillarité** : tension superficielle et mouillage sur les parois
- **Rhéologie** : comportement non-newtonien des fluides complexes
- **Dynamique interfaciale** : déformation, pincement et stabilité

---

## Propriétés des Fluides Rhéofluidifiants

### Comportement Non-Newtonien

Les fluides rhéofluidifiants sont des fluides **non-newtoniens** dont la viscosité apparente diminue sous l'effet d'un cisaillement. Ce comportement est essentiel pour la dispense : le fluide s'écoule facilement sous pression mais conserve sa forme au repos.

**Loi de puissance (Ostwald-de Waele) :**

$$\tau = K\dot{\gamma}^n \quad \text{avec } n < 1$$

où $\tau$ est la contrainte de cisaillement, $K$ l'indice de consistance, $\dot{\gamma}$ le taux de cisaillement, et $n$ l'indice de comportement.

**Modèle de Carreau-Yasuda :**

$$\eta(\dot{\gamma}) = \eta_\infty + \frac{\eta_0 - \eta_\infty}{[1 + (k\dot{\gamma})^a]^{(1-n)/a}}$$

où $\eta_0$ et $\eta_\infty$ sont les viscosités à cisaillement nul et infini, et $k$, $a$ des paramètres d'ajustement.

**Exemple :** Une encre rhéofluidifiante typique présente $\eta_0 = 0.5$–$5$ Pa·s (au repos) et $\eta_\infty = 0.05$ Pa·s sous fort cisaillement.

---

## Défis de la Modélisation Numérique

### Enjeux Techniques

| Défi | Description | Approche |
|------|-------------|----------|
| **Suivi d'interface** | Capturer la déformation de l'interface fluide/air | VOF, Phase-Field, Level-Set |
| **Rhéologie complexe** | Modéliser le comportement non-newtonien | Lois constitutives (Carreau, Herschel-Bulkley) |
| **Mouillage** | Gérer les angles de contact dynamiques | Conditions aux limites spécifiques |
| **Multi-échelles** | Du micron (interface) au millimètre (puit) | Maillages adaptatifs, méthodes sans maillage |
| **Coût calcul** | Simulations 3D transitoires coûteuses | GPU, parallélisation, méthodes hybrides |

---

## Système Physique Étudié

### Configuration Géométrique

Le système modélisé consiste en :
- **Buse de dispense** : diamètre 200–350 µm, positionnée au-dessus du puit
- **Micro-puit** : diamètre 800–1500 µm, profondeur ~130 µm
- **Fluide** : encre rhéofluidifiante ($\rho$ = 3000 kg/m³)
- **Environnement** : température ambiante (~20°C) et pression atmosphérique

### Paramètres de Simulation

| Paramètre | Plage | Unité |
|-----------|-------|-------|
| Diamètre puit | 800 – 1500 | µm |
| Diamètre buse | 200 – 350 | µm |
| Décalage horizontal (buse vs centre puit) | 0, -75, -150 | µm |
| Viscosité $\eta_\infty$ | 0.05 – 0.5 | Pa·s |
| Angle de contact paroi | 35 – 90 | ° |
| Angle de contact fond du puit | 35 – 75 | ° |
| Angle de contact substrat (plateau) | 15, 35, 90 | ° |
| Temps de dispense | 20 – 40 | ms |

---

## Approche Multi-Modèles

Ce projet compare quatre méthodes numériques complémentaires :

| Modèle | Approche | Avantage Principal |
|--------|----------|-------------------|
| **FEM / Phase-Field** | Eulérienne, éléments finis | Précision thermodynamique, couplages multiphysiques |
| **VOF** | Eulérienne, volumes finis | Robustesse, standard industriel |
| **LBM** | Mésoscopique, réseau | Performance GPU, géométries complexes |
| **SPH** | Lagrangienne, sans maillage | Surfaces libres, grandes déformations |

---

## Références

> **Note** : Pour la liste complète des références, consultez la section **Bibliographie** dans le menu Annexes.
