# Code Palabos - Lattice Boltzmann (LBM)

Cette page présente les fichiers sources C++ et la configuration XML utilisés pour les simulations LBM de dispense d'encre rhéofluidifiante.

---

## 1. Structure du code

Le code est basé sur la bibliothèque **Palabos** et structuré pour séparer la logique du solveur (C++) de la configuration (XML).

```
project_directory/
├── src/
│   └── lbm_solver/
│       └── dropletCavity2D.cpp    # Code source principal C++
├── templates_lbm/
│   └── config/
│       └── simulation_template.xml # Fichier de configuration
├── scripts/                       # Scripts de compilation et post-traitement
└── results/                       # Sorties de simulation (VTK/VTI)
```

---

## 2. Configuration de la simulation (`simulation_template.xml`)

Ce fichier définit les paramètres numériques et physiques. Il est lu par le solveur au démarrage ou généré par des scripts d'étude paramétrique.

```xml
<!-- templates_lbm/config/simulation_template.xml -->

<simulation>
  <lbm>
    <nx>320</nx>                <!-- Résolution X -->
    <ny>120</ny>                <!-- Résolution Y -->
    <tau>1.0</tau>              <!-- Temps de relaxation (tau > 0.5) -->
    <G_fluid>-112.0</G_fluid>   <!-- Force d'interaction Shan-Chen -->
  </lbm>

  <contact_angles>
    <substrate>30</substrate>         <!-- Fond du puit (hydrophile) -->
    <isolant_left>45</isolant_left>   <!-- Mur gauche -->
    <isolant_right>90</isolant_right> <!-- Mur droit (neutre) -->
    <left_platform>41</left_platform> <!-- Plateau gauche -->
  </contact_angles>

  <rheology>
    <enable_carreau>true</enable_carreau>
    <eta0>1.5</eta0>            <!-- Viscosité zéro-cisaillement -->
    <eta_inf>0.001</eta_inf>    <!-- Viscosité infinie -->
    <n>0.5</n>                  <!-- Indice de loi de puissance -->
  </rheology>
</simulation>
```

**Points clés :**
- **G_fluid** : paramètre critique du modèle Shan-Chen qui contrôle la tension de surface et la séparation de phase.
- **tau** : lié à la viscosité cinématique par $\nu = c_s^2 (\tau - 0.5)$.
- **contact_angles** : définit la mouillabilité de chaque surface de la cavité.

---

## 3. Géométrie et régions (`dropletCavity2D.cpp`)

La géométrie de la cavité est définie analytiquement dans le code C++. La fonction `getWallRegion` identifie la nature de chaque cellule (mur, fond, plateau) pour lui appliquer la bonne condition limite.

```cpp
// src/lbm_solver/dropletCavity2D.cpp

enum WallRegion {
    WALL_NONE = 0,
    WALL_LEFT_PLATFORM,    // Plateau gauche
    WALL_LEFT_VERTICAL,    // Mur vertical gauche
    WALL_BOTTOM,           // Fond du puit
    WALL_RIGHT_VERTICAL,   // Mur vertical droit
    // ...
};

WallRegion getWallRegion(plint iX, plint iY) {
    // Fond du puit (y = 0, entre les murs)
    if (iY == 0 && iX > wellStartX && iX < wellEndX) return WALL_BOTTOM;

    // Mur vertical gauche (x fixe, hauteur limitée)
    if (iX == wellStartX && iY < wellDepth) return WALL_LEFT_VERTICAL;

    // Plateau gauche (y surélevé)
    if (iY == wellDepth && iX <= wellStartX) return WALL_LEFT_PLATFORM;

    // ... autres conditions géométriques ...
    return WALL_NONE;
}
```

**Points clés :**
- **Géométrie explicite** : permet une définition précise des arêtes vives de la cavité.
- **Régions distinctes** : chaque zone peut avoir un angle de contact différent.

---

## 4. Gestion des angles de contact

En LBM Shan-Chen, l'angle de contact est imposé par une densité fictive dans la paroi. La fonction `computeWallDensity` calcule cette densité en fonction de l'angle souhaité.

```cpp
// Calcul de la densité de paroi pour un angle donné
T computeWallDensity(T theta, T rhoGas, T rhoLiq) {
    if (theta >= 90.0) {
        // Cas hydrophobe / neutre
        return rhoGas * (180.0 - theta) / 90.0;
    } else {
        // Cas hydrophile
        return rhoGas + (rhoLiq - rhoGas) * (90.0 - theta) / 90.0;
    }
}

// Application progressive pour éviter les artefacts de condensation
// (Seulement quand le liquide touche la paroi)
if (liquidNearby) {
    T rhoWall = rho_neutral;
    switch (region) {
        case WALL_BOTTOM: rhoWall = rhoWall_bottom; break;
        case WALL_LEFT_VERTICAL: rhoWall = rhoWall_leftVert; break;
        // ...
    }
    defineDynamics(lattice, box, new BounceBack<T, DESCRIPTOR>(rhoWall));
}
```

**Points clés :**
- **Densité virtuelle** : modifie le potentiel d'interaction près des murs.
- **Activation dynamique** : les propriétés de mouillage ne sont activées qu'au contact du fluide pour éviter la condensation parasite sur les surfaces hydrophiles.

---

## 5. Rhéologie non-newtonienne (modèle de Carreau)

Le comportement rhéofluidifiant de l'encre est implémenté via un processeur de données qui ajuste localement le temps de relaxation $\tau$ (et donc la viscosité) en fonction du taux de cisaillement.

```cpp
// src/lbm_solver/dropletCavity2D.cpp - CarreauRheologyProcessor

// 1. Calcul du tenseur des taux de déformation S_ab
T Sxx = -1.5 * omegaRef * Pi_xx / rho;
T Syy = -1.5 * omegaRef * Pi_yy / rho;
T Sxy = -1.5 * omegaRef * Pi_xy / rho;

// 2. Magnitude du cisaillement (gamma point)
T gammaDot = std::sqrt(2.0 * (Sxx*Sxx + Syy*Syy + 2.0*Sxy*Sxy));

// 3. Calcul de la viscosité locale (Modèle Carreau)
// nu = nuInf + (nu0 - nuInf) * [1 + (lambda * gammaDot)^2]^((n-1)/2)
T factor = std::pow(1.0 + std::pow(lambda * gammaDot, 2), (n - 1.0) / 2.0);
T nuLocal = nuInf + (nu0 - nuInf) * factor;

// 4. Mise à jour de la relaxation
T omegaLocal = 1.0 / (3.0 * nuLocal + 0.5);
```

**Points clés :**
- **Calcul local** : la viscosité est recalculée en chaque point et à chaque pas de temps.
- **Stabilité** : des bornes (`tauMin`, `tauMax`) sont appliquées pour assurer la stabilité numérique.

---

## 6. Initialisation de la goutte

La goutte est initialisée avec un profil de densité lissé (tangente hyperbolique) pour minimiser les ondes acoustiques au démarrage.

```cpp
// Initialisation douce de l'interface
T interfaceWidth = 4.0;
T phi = 0.5 * (1.0 - tanh(2.0 * (dist - radius) / interfaceWidth));
T rho = rhoOut + phi * (rhoIn - rhoOut);
```

**Points clés :**
- **Interface diffuse** : caractéristique intrinsèque du modèle Shan-Chen (3-4 cellules d'épaisseur).
- **Équilibre** : une phase de "warmup" sans gravité permet à la goutte de prendre sa forme sphérique et ses densités d'équilibre avant l'impact.

---

## 7. Boucle principale et Sorties

Le programme principal gère l'itération temporelle et l'écriture des fichiers VTK pour la visualisation.

```cpp
// src/lbm_solver/dropletCavity2D.cpp - main

// Boucle principale
for (int iT = 1; iT <= maxIter; ++iT) {
    lattice.collideAndStream();

    // Application progressive des angles de contact
    if (iT % 10 == 0) {
        // ... détection du contact liquide/mur ...
    }

    // Écriture des résultats (fichiers .vti lisibles par ParaView)
    if (iT % saveIter == 0) {
        std::unique_ptr<MultiScalarField2D<T>> rho(computeDensity(lattice));
        
        // Masquage des zones solides internes pour une visualisation propre
        maskInternalSolids(*rho, rhoGas);
        
        string filename = "droplet_" + util::val2str(iT);
        VtkImageOutput2D<T> vtkOut(filename, 1.0);
        vtkOut.writeData<float>(*rho, "density", 1.0);
    }
}
```

**Points clés :**
- **VTK/VTI** : format standard pour les données volumétriques (images 2D/3D).
- **Post-traitement** : le masquage des solides est purement visuel pour faciliter l'analyse des résultats.

---

## 8. Résumé des paramètres physiques

Le code convertit les unités physiques (SI) en unités de réseau (Lattice Units - l.u.).

| Paramètre Physique | Valeur Typique | Conversion LBM |
|-------------------|----------------|----------------|
| Diamètre goutte | 300 µm | 60 l.u. (dx = 5 µm) |
| Profondeur puits | 130 µm | 26 l.u. |
| Largeur puits | 800 µm | 160 l.u. |
| Densité encre | 3000 kg/m³ | $\rho_{liq} \approx 458$ (Shan-Chen) |
| Tension surface | 0.040 N/m | Contrôlé par $G = -112$ |
| Gravité | 9.81 m/s² | $g_{lb} \approx 5 \times 10^{-5}$ |

**Note :** Le choix de $G$ est crucial. Il doit être calibré pour obtenir le bon rapport de densité et une tension de surface stable sans provoquer d'instabilités numériques (courants parasites).

```