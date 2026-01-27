# Code OpenFOAM - Volume of Fluid (VOF)

Cette page présente les principaux fichiers de configuration OpenFOAM utilisés pour les simulations VOF de dispense d'encre rhéofluidifiante.

---

## 1. Structure du cas OpenFOAM

```
case_directory/
├── 0/                     # Conditions initiales
│   ├── U                  # Champ de vitesse
│   ├── p_rgh              # Pression hydrostatique
│   └── alpha.water        # Fraction volumique (encre/air)
├── constant/              # Propriétés physiques
│   └── transportProperties
├── system/                # Paramètres numériques
│   ├── controlDict        # Contrôle de la simulation
│   ├── fvSchemes          # Schémas de discrétisation
│   ├── fvSolution         # Solveurs et algorithmes
│   ├── blockMeshDict      # Génération du maillage
│   └── setFieldsDict      # Initialisation des champs
└── templates/             # Fichiers de base pour études paramétriques
```

---

## 2. Propriétés de transport (`transportProperties`)

Ce fichier définit les propriétés physiques des deux phases (encre et air) ainsi que la tension de surface.

```cpp
// constant/transportProperties

phases (water air);

water  // Phase encre
{
    transportModel  Carreau;
    rho             3000;          // kg/m³ - densité encre

    Carreau  // Modèle de Carreau pour la viscosité
    {
        nu0         1.667e-4;      // m²/s (η₀/ρ = 0.5/3000)
        nuInf       5.56e-5;       // m²/s (η∞/ρ = 0.167/3000)
        lambda      0.15;          // s - temps de relaxation
        n           0.7;           // exposant loi de puissance
    }
}

air  // Phase air (newtonienne)
{
    transportModel  Newtonian;
    rho             1.2;           // kg/m³
    mu              1e-5;          // Pa·s
}

sigma           0.04;              // N/m - tension de surface (40 mN/m)
```

**Points clés :**
- Le modèle de **Carreau** capture le comportement rhéofluidifiant de l'encre
- La viscosité cinématique $\nu = \eta / \rho$ est utilisée par OpenFOAM
- La tension de surface $\sigma$ contrôle les forces capillaires à l'interface

---

## 3. Contrôle de la simulation (`controlDict`)

Ce fichier contrôle les paramètres temporels et les critères de stabilité.

```cpp
// system/controlDict

application     interFoam;         // Solveur VOF incompressible

startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         0.3;               // 300 ms de simulation

deltaT          1e-06;             // Pas de temps initial (1 µs)

writeControl    adjustableRunTime;
writeInterval   0.005;             // Écriture toutes les 5 ms

// Contrôle adaptatif du pas de temps (critère CFL)
adjustTimeStep  yes;
maxCo           0.3;               // Courant max global
maxAlphaCo      0.3;               // Courant max à l'interface
maxDeltaT       1e-3;              // Pas de temps max (1 ms)
```

**Points clés :**
- **interFoam** : solveur VOF avec tension de surface (CSF)
- **Courant < 0.3** : essentiel pour la stabilité VOF et la conservation de masse
- **Pas de temps adaptatif** : ajusté automatiquement selon le critère CFL

---

## 4. Schémas de discrétisation (`fvSchemes`)

Définit les schémas numériques pour les dérivées spatiales et temporelles.

```cpp
// system/fvSchemes

ddtSchemes
{
    default         Euler;         // Schéma temporel 1er ordre
}

gradSchemes
{
    default         Gauss linear;  // Gradient par volumes finis
}

divSchemes
{
    default         none;

    // Convection de la quantité de mouvement
    div(rhoPhi,U)   Gauss linearUpwind grad(U);

    // Transport de l'interface VOF avec compression
    div(phi,alpha)  Gauss interfaceCompression vanLeer 1;

    // Terme de diffusion turbulente
    div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;
}

laplacianSchemes
{
    default         Gauss linear corrected;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         corrected;
}
```

**Points clés :**
- **interfaceCompression** : maintient une interface nette entre les phases
- **vanLeer** : schéma borné pour éviter les oscillations de $\alpha$
- **linearUpwind** : bon compromis précision/stabilité pour la convection

---

## 5. Configuration des solveurs (`fvSolution`)

Paramètres des solveurs itératifs et de l'algorithme PIMPLE.

```cpp
// system/fvSolution

solvers
{
    "alpha.water.*"
    {
        nAlphaCorr      3;         // Corrections de l'interface
        nAlphaSubCycles 2;         // Sous-cycles pour robustesse

        // Configuration MULES (flux limité)
        MULESCorr       no;        // MULES explicite (Co < 0.5)
        nLimiterIter    3;         // Itérations du limiteur

        // Bornage strict de alpha dans [0,1]
        globalBounds    yes;
        limiterTolerance 1e-8;

        interfaceCompression on;

        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-09;
        relTol          0;
    }

    p_rgh
    {
        solver          PCG;
        preconditioner  diagonal;
        tolerance       1e-08;
        relTol          0.01;
    }

    U
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-06;
        relTol          0;
    }
}

PIMPLE
{
    momentumPredictor   no;
    nOuterCorrectors    1;         // 1 correction externe (VOF best practice)
    nCorrectors         3;         // 3 corrections pression-vitesse
    nNonOrthogonalCorrectors 0;

    maxCo               0.2;       // Courant réduit pour stabilité
    maxAlphaCo          0.2;

    pRefCell            0;
    pRefValue           0;
}

relaxationFactors
{
    fields
    {
        p_rgh           0.3;       // Sous-relaxation pression
        alpha.water     0.5;       // Sous-relaxation interface
    }
}
```

**Points clés :**
- **MULES** : algorithme de transport multidimensionnel pour préserver $0 \leq \alpha \leq 1$
- **globalBounds** : assure le bornage strict de la fraction volumique
- **PIMPLE** : algorithme de couplage pression-vitesse

---

## 6. Conditions aux limites - Vitesse (`U`)

Définit les conditions aux limites pour le champ de vitesse.

```cpp
// 0/U

dimensions      [0 1 -1 0 0 0 0];

internalField   uniform (0 0 0);

boundaryField
{
    // Faces 2D (géométrie axisymétrique)
    front { type empty; }
    back  { type empty; }

    // Substrat et parois - condition no-slip
    substrate           { type noSlip; }
    wall_isolant_left   { type noSlip; }
    wall_isolant_right  { type noSlip; }
    wall_buse_left_int  { type noSlip; }
    wall_buse_right_int { type noSlip; }

    // Inlet - profil temporel de vitesse d'injection
    inlet
    {
        type            uniformFixedValue;
        uniformValue    table
        (
            (0.000    (0 -0.00683 0))   // 6.83 mm/s vers le bas
            (0.080    (0 -0.00683 0))   // fin dispense à 80 ms
            (0.0801   (0 0 0))          // arrêt brutal
            (0.300    (0 0 0))          // reste à 0
        );
    }

    // Atmosphère et outlets - pression ambiante
    atmosphere   { type pressureInletOutletVelocity; value uniform (0 0 0); }
    outlet_left  { type pressureInletOutletVelocity; value uniform (0 0 0); }
    outlet_right { type pressureInletOutletVelocity; value uniform (0 0 0); }
}
```

**Points clés :**
- **table** : permet de définir un profil temporel d'injection
- **noSlip** : condition d'adhérence sur toutes les parois solides
- **pressureInletOutletVelocity** : permet l'entrée/sortie libre à la pression ambiante

---

## 7. Angles de contact (`alpha.water`)

Les angles de contact sont définis dans les conditions aux limites de $\alpha$.

```cpp
// 0/alpha.water (extrait)

boundaryField
{
    // Substrat (or) - angle hydrophile
    substrate
    {
        type            constantAlphaContactAngle;
        theta0          35;        // Angle de contact en degrés
        limit           gradient;
        value           uniform 0;
    }

    // Parois isolant gauche - angle variable
    wall_isolant_left
    {
        type            constantAlphaContactAngle;
        theta0          15;        // Peut varier: 15° ou 60°
        limit           gradient;
        value           uniform 0;
    }

    // Parois isolant droite - angle variable
    wall_isolant_right
    {
        type            constantAlphaContactAngle;
        theta0          60;        // Peut varier: 60° ou 90°
        limit           gradient;
        value           uniform 0;
    }
}
```

**Points clés :**
- **constantAlphaContactAngle** : impose un angle de contact statique
- **theta0** : angle de contact en degrés (0° = mouillage total, 90° = neutre)
- **limit: gradient** : assure une transition douce à l'interface

---

## 8. Script d'étude paramétrique (`parametric_runner.py`)

Ce script Python automatise les études paramétriques en modifiant les paramètres OpenFOAM.

```python
#!/usr/bin/env python3
"""
Parametric Study Runner for OpenFOAM VOF Simulations
Usage:
    python3 parametric_runner.py create --name study_name
    python3 parametric_runner.py run --study study_name
    python3 parametric_runner.py status --study study_name
"""

class ParameterModifier:
    """Modifie les fichiers OpenFOAM selon les paramètres YAML."""

    def set_parameter(self, param_path: str, value):
        """
        Modifie un paramètre OpenFOAM.

        Args:
            param_path: Chemin (ex: 'rheology.eta0', 'contact_angles.substrate')
            value: Nouvelle valeur
        """
        section, param = param_path.split('.', 1)

        if section == 'rheology':
            self._modify_transport_properties(param, value)
        elif section == 'contact_angles':
            self._modify_alpha_water(param, value)
        elif section == 'geometry':
            self._modify_geometry(param, value)

    def _modify_transport_properties(self, param: str, value):
        """
        Modifie les paramètres de rhéologie.

        IMPORTANT: Conversion viscosité dynamique → cinématique
        - eta0, eta_inf sont en Pa·s (viscosité dynamique)
        - OpenFOAM attend nu0, nuInf en m²/s (viscosité cinématique)
        - Conversion: nu = eta / rho
        """
        RHO_INK = 3000  # kg/m³

        if param == 'eta0':
            nu_value = value / RHO_INK
            # Mise à jour de nu_0 dans system/parameters
            print(f"  → η = {value} Pa·s → ν = {nu_value:.6e} m²/s")


class StudyRunner:
    """Gestionnaire d'études paramétriques."""

    def run_study(self, study_name: str, dry_run: bool = False):
        """Exécute une étude paramétrique (simple ou grid)."""

        # Génère toutes les combinaisons de paramètres
        combinations = self._generate_grid_combinations(parameters)

        for i, params in enumerate(combinations, 1):
            run_dir = study_results / f"run_{i:03d}"

            # Copier les templates
            shutil.copytree(TEMPLATES_DIR / "0", run_dir / "0")
            shutil.copytree(TEMPLATES_DIR / "constant", run_dir / "constant")
            shutil.copytree(TEMPLATES_DIR / "system", run_dir / "system")

            # Modifier les paramètres
            modifier = ParameterModifier(run_dir)
            for param_path, value in params.items():
                modifier.set_parameter(param_path, value)

            # Lancer la simulation
            cmd = f"blockMesh && setFields && foamRun -solver incompressibleVoF"
            subprocess.run(cmd, shell=True, cwd=run_dir)
```

**Points clés :**
- **Grid sweep** : génère toutes les combinaisons de paramètres
- **Conversion d'unités** : viscosité dynamique → cinématique automatique
- **Pipeline** : blockMesh → setFields → foamRun

---

## 9. Script de création de GIF (`create_vof_gif.py`)

Ce script génère les animations GIF à partir des résultats OpenFOAM.

```python
#!/usr/bin/env python3
"""
Generate Streamlit-compatible GIFs from OpenFOAM VOF results.
Format: 640x480, white background, black phase.
"""

import pyvista as pv
import numpy as np
from PIL import Image
import imageio

# Configuration - Style compatible avec FEM
WIDTH, HEIGHT = 640, 480
FPS = 10
BACKGROUND = 'white'
PHASE_COLOR = 'black'

# Vue caméra fixe (coordonnées SI en mètres)
FIXED_VIEW = {
    'x_min': -0.0008,   # -0.8 mm
    'x_max': 0.0008,    # +0.8 mm
    'y_min': 0.0,       # substrat à y=0
    'y_max': 0.00065,   # 0.65 mm
}


def render_timestep(case_dir: Path, time: float, params: dict) -> np.ndarray:
    """
    Rend un pas de temps en image.

    Args:
        case_dir: Répertoire du cas OpenFOAM
        time: Temps en secondes
        params: Paramètres pour les annotations

    Returns:
        Image numpy array (RGB)
    """
    # Charger le fichier VTK/VTU
    vtk_file = case_dir / f"VTK/case_{time}.vtk"
    mesh = pv.read(vtk_file)

    # Extraire l'iso-surface alpha = 0.5 (interface encre/air)
    contour = mesh.contour([0.5], scalars='alpha.water')

    # Configuration du plotter
    plotter = pv.Plotter(off_screen=True, window_size=[WIDTH, HEIGHT])
    plotter.background_color = BACKGROUND

    # Ajouter l'interface
    plotter.add_mesh(contour, color=PHASE_COLOR)

    # Ajouter les parois
    for patch in WALL_PATCHES:
        wall_mesh = extract_boundary_patch(mesh, patch)
        if wall_mesh:
            plotter.add_mesh(wall_mesh, color='black', line_width=2)

    # Capturer l'image
    plotter.camera_position = get_fixed_camera()
    return plotter.screenshot(return_img=True)


def create_gif(run_dir: Path, output_path: Path):
    """
    Crée un GIF animé à partir des pas de temps.
    """
    params = read_openfoam_parameters(run_dir)
    times = get_time_directories(run_dir)

    frames = []
    for t in times:
        img = render_timestep(run_dir, t, params)
        img_annotated = add_annotations(img, params, t * 1000)  # ms
        frames.append(img_annotated)

    # Sauvegarder le GIF
    imageio.mimsave(output_path, frames, fps=FPS, loop=0)
    print(f"GIF créé: {output_path}")
```

**Points clés :**
- **PyVista** : lecture des résultats VTK et rendu 3D
- **Iso-surface alpha=0.5** : visualise l'interface encre/air
- **Vue caméra fixe** : assure la cohérence entre les simulations
- **Annotations** : paramètres physiques affichés sur chaque frame

---

## 10. Configuration YAML d'une étude

Exemple de fichier de configuration pour une étude paramétrique.

```yaml
# config/studies/contact_angles.yaml

name: contact_angles_study
description: Étude de l'influence des angles de contact

sweep_type: grid
sweep:
  parameters:
    - name: rheology.eta0
      values: [0.5, 1.5]          # Pa·s

    - name: contact_angles.substrate
      values: [15, 60]            # degrés

    - name: contact_angles.wall_isolant_left
      values: [15, 60]            # degrés

    - name: contact_angles.wall_isolant_right
      values: [60, 90]            # degrés

    - name: geometry.ratio_surface
      values: [0.8, 1.0, 1.2]     # ratio goutte/puit

overrides:
  numerical:
    endTime: 0.1                   # 100 ms
    writeInterval: 0.005           # 5 ms

execution:
  parallel: false
  timeout: 3600                    # 1 heure max par simulation

postprocessing:
  generate_animations: true
  comparison_plots: true
  export_csv: true
```

**Points clés :**
- **sweep_type: grid** : génère toutes les combinaisons (2×2×2×2×3 = 48 simulations)
- **overrides** : paramètres communs à toutes les simulations
- **postprocessing** : génération automatique des visualisations

---

## Résumé des paramètres variables

| Paramètre | Valeurs testées | Unité |
|-----------|-----------------|-------|
| Gap buse | 30, 120 | µm |
| Shift buse | −150, −75, 0 | µm |
| Viscosité η₀ | 0.5, 1.5, 5.0 | Pa·s |
| Ratio surface goutte/puit | 0.8, 1.2 | - |
| CA substrat | 15, 35 | ° |
| CA mur droit | 15, 120 | ° |
| CA mur gauche | 15 | ° |

**Total : 144 simulations** (2 × 3 × 3 × 2 × 2 × 2 × 1 combinaisons)
