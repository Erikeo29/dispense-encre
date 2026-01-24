# OpenFOAM Code - Volume of Fluid (VOF)

This page presents the main OpenFOAM configuration files used for VOF simulations of shear-thinning ink dispensing.

---

## 1. OpenFOAM Case Structure

```
case_directory/
├── 0/                     # Initial conditions
│   ├── U                  # Velocity field
│   ├── p_rgh              # Hydrostatic pressure
│   └── alpha.water        # Volume fraction (ink/air)
├── constant/              # Physical properties
│   └── transportProperties
├── system/                # Numerical parameters
│   ├── controlDict        # Simulation control
│   ├── fvSchemes          # Discretization schemes
│   ├── fvSolution         # Solvers and algorithms
│   ├── blockMeshDict      # Mesh generation
│   └── setFieldsDict      # Field initialization
└── templates/             # Base files for parametric studies
```

---

## 2. Transport Properties (`transportProperties`)

This file defines the physical properties of both phases (ink and air) and the surface tension.

```cpp
// constant/transportProperties

phases (water air);

water  // Ink phase
{
    transportModel  Carreau;
    rho             3000;          // kg/m³ - ink density

    Carreau  // Carreau model for viscosity
    {
        nu0         1.667e-4;      // m²/s (η₀/ρ = 0.5/3000)
        nuInf       5.56e-5;       // m²/s (η∞/ρ = 0.167/3000)
        lambda      0.15;          // s - relaxation time
        n           0.7;           // power law exponent
    }
}

air  // Air phase (Newtonian)
{
    transportModel  Newtonian;
    rho             1.2;           // kg/m³
    mu              1e-5;          // Pa·s
}

sigma           0.04;              // N/m - surface tension (40 mN/m)
```

**Key points:**
- The **Carreau** model captures the shear-thinning behavior of the ink
- Kinematic viscosity $\nu = \eta / \rho$ is used by OpenFOAM
- Surface tension $\sigma$ controls capillary forces at the interface

---

## 3. Simulation Control (`controlDict`)

This file controls time parameters and stability criteria.

```cpp
// system/controlDict

application     interFoam;         // Incompressible VOF solver

startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         0.3;               // 300 ms simulation

deltaT          1e-06;             // Initial time step (1 µs)

writeControl    adjustableRunTime;
writeInterval   0.005;             // Write every 5 ms

// Adaptive time stepping (CFL criterion)
adjustTimeStep  yes;
maxCo           0.3;               // Max global Courant
maxAlphaCo      0.3;               // Max interface Courant
maxDeltaT       1e-3;              // Max time step (1 ms)
```

**Key points:**
- **interFoam**: VOF solver with surface tension (CSF method)
- **Courant < 0.3**: essential for VOF stability and mass conservation
- **Adaptive time stepping**: automatically adjusted based on CFL criterion

---

## 4. Discretization Schemes (`fvSchemes`)

Defines numerical schemes for spatial and temporal derivatives.

```cpp
// system/fvSchemes

ddtSchemes
{
    default         Euler;         // 1st order temporal scheme
}

gradSchemes
{
    default         Gauss linear;  // Gradient by finite volumes
}

divSchemes
{
    default         none;

    // Momentum convection
    div(rhoPhi,U)   Gauss linearUpwind grad(U);

    // VOF interface transport with compression
    div(phi,alpha)  Gauss interfaceCompression vanLeer 1;

    // Turbulent diffusion term
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

**Key points:**
- **interfaceCompression**: maintains a sharp interface between phases
- **vanLeer**: bounded scheme to prevent $\alpha$ oscillations
- **linearUpwind**: good accuracy/stability compromise for convection

---

## 5. Solver Configuration (`fvSolution`)

Iterative solver parameters and PIMPLE algorithm settings.

```cpp
// system/fvSolution

solvers
{
    "alpha.water.*"
    {
        nAlphaCorr      3;         // Interface corrections
        nAlphaSubCycles 2;         // Sub-cycles for robustness

        // MULES configuration (flux limiting)
        MULESCorr       no;        // Explicit MULES (Co < 0.5)
        nLimiterIter    3;         // Limiter iterations

        // Strict bounding of alpha in [0,1]
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
    nOuterCorrectors    1;         // 1 outer correction (VOF best practice)
    nCorrectors         3;         // 3 pressure-velocity corrections
    nNonOrthogonalCorrectors 0;

    maxCo               0.2;       // Reduced Courant for stability
    maxAlphaCo          0.2;

    pRefCell            0;
    pRefValue           0;
}

relaxationFactors
{
    fields
    {
        p_rgh           0.3;       // Pressure under-relaxation
        alpha.water     0.5;       // Interface under-relaxation
    }
}
```

**Key points:**
- **MULES**: multidimensional transport algorithm to preserve $0 \leq \alpha \leq 1$
- **globalBounds**: ensures strict volume fraction bounding
- **PIMPLE**: pressure-velocity coupling algorithm

---

## 6. Boundary Conditions - Velocity (`U`)

Defines boundary conditions for the velocity field.

```cpp
// 0/U

dimensions      [0 1 -1 0 0 0 0];

internalField   uniform (0 0 0);

boundaryField
{
    // 2D faces (axisymmetric geometry)
    front { type empty; }
    back  { type empty; }

    // Substrate and walls - no-slip condition
    substrate           { type noSlip; }
    wall_isolant_left   { type noSlip; }
    wall_isolant_right  { type noSlip; }
    wall_buse_left_int  { type noSlip; }
    wall_buse_right_int { type noSlip; }

    // Inlet - temporal velocity profile for injection
    inlet
    {
        type            uniformFixedValue;
        uniformValue    table
        (
            (0.000    (0 -0.00683 0))   // 6.83 mm/s downward
            (0.080    (0 -0.00683 0))   // dispense ends at 80 ms
            (0.0801   (0 0 0))          // abrupt stop
            (0.300    (0 0 0))          // remains at 0
        );
    }

    // Atmosphere and outlets - ambient pressure
    atmosphere   { type pressureInletOutletVelocity; value uniform (0 0 0); }
    outlet_left  { type pressureInletOutletVelocity; value uniform (0 0 0); }
    outlet_right { type pressureInletOutletVelocity; value uniform (0 0 0); }
}
```

**Key points:**
- **table**: allows defining a temporal injection profile
- **noSlip**: adhesion condition on all solid walls
- **pressureInletOutletVelocity**: allows free inlet/outlet at ambient pressure

---

## 7. Contact Angles (`alpha.water`)

Contact angles are defined in the $\alpha$ boundary conditions.

```cpp
// 0/alpha.water (excerpt)

boundaryField
{
    // Substrate (gold) - hydrophilic angle
    substrate
    {
        type            constantAlphaContactAngle;
        theta0          35;        // Contact angle in degrees
        limit           gradient;
        value           uniform 0;
    }

    // Left isolant walls - variable angle
    wall_isolant_left
    {
        type            constantAlphaContactAngle;
        theta0          15;        // Can vary: 15° or 60°
        limit           gradient;
        value           uniform 0;
    }

    // Right isolant walls - variable angle
    wall_isolant_right
    {
        type            constantAlphaContactAngle;
        theta0          60;        // Can vary: 60° or 90°
        limit           gradient;
        value           uniform 0;
    }
}
```

**Key points:**
- **constantAlphaContactAngle**: imposes a static contact angle
- **theta0**: contact angle in degrees (0° = total wetting, 90° = neutral)
- **limit: gradient**: ensures smooth transition at the interface

---

## 8. Parametric Study Script (`parametric_runner.py`)

This Python script automates parametric studies by modifying OpenFOAM parameters.

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
    """Modifies OpenFOAM files according to YAML parameters."""

    def set_parameter(self, param_path: str, value):
        """
        Modifies an OpenFOAM parameter.

        Args:
            param_path: Path (e.g., 'rheology.eta0', 'contact_angles.substrate')
            value: New value
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
        Modifies rheology parameters.

        IMPORTANT: Dynamic to kinematic viscosity conversion
        - eta0, eta_inf are in Pa·s (dynamic viscosity)
        - OpenFOAM expects nu0, nuInf in m²/s (kinematic viscosity)
        - Conversion: nu = eta / rho
        """
        RHO_INK = 3000  # kg/m³

        if param == 'eta0':
            nu_value = value / RHO_INK
            # Update nu_0 in system/parameters
            print(f"  → η = {value} Pa·s → ν = {nu_value:.6e} m²/s")


class StudyRunner:
    """Parametric study manager."""

    def run_study(self, study_name: str, dry_run: bool = False):
        """Executes a parametric study (simple or grid)."""

        # Generate all parameter combinations
        combinations = self._generate_grid_combinations(parameters)

        for i, params in enumerate(combinations, 1):
            run_dir = study_results / f"run_{i:03d}"

            # Copy templates
            shutil.copytree(TEMPLATES_DIR / "0", run_dir / "0")
            shutil.copytree(TEMPLATES_DIR / "constant", run_dir / "constant")
            shutil.copytree(TEMPLATES_DIR / "system", run_dir / "system")

            # Modify parameters
            modifier = ParameterModifier(run_dir)
            for param_path, value in params.items():
                modifier.set_parameter(param_path, value)

            # Run simulation
            cmd = f"blockMesh && setFields && foamRun -solver incompressibleVoF"
            subprocess.run(cmd, shell=True, cwd=run_dir)
```

**Key points:**
- **Grid sweep**: generates all parameter combinations
- **Unit conversion**: dynamic → kinematic viscosity automatic
- **Pipeline**: blockMesh → setFields → foamRun

---

## 9. GIF Creation Script (`create_vof_gif.py`)

This script generates animated GIFs from OpenFOAM results.

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

# Configuration - FEM compatible style
WIDTH, HEIGHT = 640, 480
FPS = 10
BACKGROUND = 'white'
PHASE_COLOR = 'black'

# Fixed camera view (SI coordinates in meters)
FIXED_VIEW = {
    'x_min': -0.0008,   # -0.8 mm
    'x_max': 0.0008,    # +0.8 mm
    'y_min': 0.0,       # substrate at y=0
    'y_max': 0.00065,   # 0.65 mm
}


def render_timestep(case_dir: Path, time: float, params: dict) -> np.ndarray:
    """
    Renders a timestep as an image.

    Args:
        case_dir: OpenFOAM case directory
        time: Time in seconds
        params: Parameters for annotations

    Returns:
        Image numpy array (RGB)
    """
    # Load VTK/VTU file
    vtk_file = case_dir / f"VTK/case_{time}.vtk"
    mesh = pv.read(vtk_file)

    # Extract iso-surface alpha = 0.5 (ink/air interface)
    contour = mesh.contour([0.5], scalars='alpha.water')

    # Configure plotter
    plotter = pv.Plotter(off_screen=True, window_size=[WIDTH, HEIGHT])
    plotter.background_color = BACKGROUND

    # Add interface
    plotter.add_mesh(contour, color=PHASE_COLOR)

    # Add walls
    for patch in WALL_PATCHES:
        wall_mesh = extract_boundary_patch(mesh, patch)
        if wall_mesh:
            plotter.add_mesh(wall_mesh, color='black', line_width=2)

    # Capture image
    plotter.camera_position = get_fixed_camera()
    return plotter.screenshot(return_img=True)


def create_gif(run_dir: Path, output_path: Path):
    """
    Creates an animated GIF from timesteps.
    """
    params = read_openfoam_parameters(run_dir)
    times = get_time_directories(run_dir)

    frames = []
    for t in times:
        img = render_timestep(run_dir, t, params)
        img_annotated = add_annotations(img, params, t * 1000)  # ms
        frames.append(img_annotated)

    # Save GIF
    imageio.mimsave(output_path, frames, fps=FPS, loop=0)
    print(f"GIF created: {output_path}")
```

**Key points:**
- **PyVista**: reads VTK results and 3D rendering
- **Iso-surface alpha=0.5**: visualizes the ink/air interface
- **Fixed camera view**: ensures consistency between simulations
- **Annotations**: physical parameters displayed on each frame

---

## 10. Study YAML Configuration

Example configuration file for a parametric study.

```yaml
# config/studies/contact_angles.yaml

name: contact_angles_study
description: Study of contact angle influence

sweep_type: grid
sweep:
  parameters:
    - name: rheology.eta0
      values: [0.5, 1.5]          # Pa·s

    - name: contact_angles.substrate
      values: [15, 60]            # degrees

    - name: contact_angles.wall_isolant_left
      values: [15, 60]            # degrees

    - name: contact_angles.wall_isolant_right
      values: [60, 90]            # degrees

    - name: geometry.ratio_surface
      values: [0.8, 1.0, 1.2]     # drop/well ratio

overrides:
  numerical:
    endTime: 0.1                   # 100 ms
    writeInterval: 0.005           # 5 ms

execution:
  parallel: false
  timeout: 3600                    # 1 hour max per simulation

postprocessing:
  generate_animations: true
  comparison_plots: true
  export_csv: true
```

**Key points:**
- **sweep_type: grid**: generates all combinations (2×2×2×2×3 = 48 simulations)
- **overrides**: common parameters for all simulations
- **postprocessing**: automatic visualization generation

---

## Variable Parameters Summary

| Parameter | Tested values | Unit |
|-----------|---------------|------|
| Drop/well surface ratio | 0.8, 1.0, 1.2 | - |
| Viscosity η₀ | 0.5, 1.5 | Pa·s |
| CA substrate | 15, 60 | ° |
| CA left wall | 15, 60 | ° |
| CA right wall | 60, 90 | ° |

**Total: 40 simulations** (unique combinations after filtering)
