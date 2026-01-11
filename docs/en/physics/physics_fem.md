## Phase-Field Method Principle

The **Phase-Field** method coupled with **Finite Elements (FEM)** is a thermodynamically consistent approach for simulating two-phase flows. Unlike explicit interface tracking methods, it represents the interface as a diffuse transition zone of finite thickness.

### Diffuse Interface Concept

The interface between the two fluids is represented by a scalar variable, the **phase function** φ:

- φ = +1: Pure Fluid 1 (ink)
- φ = -1: Pure Fluid 2 (air)
- -1 < φ < +1: Interface zone (continuous transition)

This approach offers several advantages:
- **Thermodynamic consistency**: φ evolution minimizes a free energy
- **Natural coalescence/breakup**: topological changes are automatic
- **Multiphysics coupling**: native integration with viscoelasticity and FSI

### Variational Formulation

The finite element method transforms partial differential equations into an algebraic system via the **weak formulation**. The unknowns (velocity, pressure, phase) are approximated on a mesh using polynomial shape functions (Taylor-Hood P2-P1).

---

## 1. PHYSICAL CONTEXT

### 1.1 System Under Study

The system under consideration is an incompressible two-phase flow in a microfluidic domain, comprising:
- **Phase 1**: Ink (non-Newtonian fluid)
- **Phase 2**: Ambient air (Newtonian fluid)
- **Domain**: Cylindrical well with diameter D_w = 0.8 to 1.5mm and height h_w = 0.128mm
- **Source**: Nozzle with diameter D_s = 0.2 to 0.35mm positioned at Δz = 30 μm above the well

### 1.2 Fundamental Assumptions

1. Incompressible flow (∇·**v** = 0)
2. Laminar regime (Re << 2300)
3. Negligible gravitational forces (Bo << 1)
4. Diffuse interface with finite thickness ε
5. Constant thermal properties (isothermal)

---

## 2. MATHEMATICAL FORMULATION

### 2.1 Navier-Stokes Equations

The equations governing incompressible two-phase flow are:

#### Continuity Equation (Mass Conservation)
$\nabla \cdot \mathbf{v} = 0 \quad \text{in } \Omega \times [0,T]$

where:
- **v** = (u, v) is the velocity vector with u and v being the components along x and y respectively
- **Ω** is the spatial domain (well and nozzle geometry)
- **[0,T]** is the time interval with T = 0.1 s
- **Ω × [0,T]** means "at every point in space and at every instant"

#### Momentum Equation
$$\rho(\phi)\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho(\phi)\mathbf{g} + \mathbf{F}_\sigma$$

where:
- ρ(φ) is the local density defined by: ρ(φ) = ρ₁H(φ) + ρ₂[1-H(φ)]
- p is the pressure [Pa]
- **τ** is the viscous stress tensor defined below
- **g** = (0, -9.81) m/s² is the gravitational acceleration
- **F**_σ is the surface tension body force defined in section 2.3

#### Viscous Stress Tensor

For an incompressible fluid, the stress tensor is written as:
$$\boldsymbol{\tau} = 2\eta(\phi,\dot{\gamma})\mathbf{D}$$

with the rate of deformation tensor:
$$\mathbf{D} = \frac{1}{2}\left[\nabla \mathbf{v} + (\nabla \mathbf{v})^T\right]$$

In components:
$$D_{ij} = \frac{1}{2}\left(\frac{\partial v_i}{\partial x_j} + \frac{\partial v_j}{\partial x_i}\right)$$

The shear rate is defined by:
$$\dot{\gamma} = \sqrt{2\mathbf{D}:\mathbf{D}} = \sqrt{2\sum_{i,j} D_{ij}D_{ij}}$$

### 2.2 Carreau Rheological Model

The ink viscosity follows the Carreau model:
$$\eta_1(\dot{\gamma}) = \eta_{\infty} + (\eta_0 - \eta_{\infty})\left[1 + (\lambda\dot{\gamma})^2\right]^{\frac{n-1}{2}}$$

with parameters:
- η₀ = 0.5 to 5 Pa·s: zero-shear viscosity
- η_∞ = 0.05 Pa·s: infinite-shear viscosity
- λ = 0.15 s: characteristic relaxation time
- n = 0.7: power-law index (n < 1: shear-thinning fluid)

The air viscosity is constant: η₂ = 1×10⁻⁵ Pa·s

The mixture viscosity is:
$$\eta(\phi,\dot{\gamma}) = \eta_1(\dot{\gamma})H(\phi) + \eta_2[1-H(\phi)]$$

### 2.3 Phase-Field Method

#### Interface Transport

The interface between the two phases is tracked using the Phase-Field method:
$$\frac{\partial \phi}{\partial t} + \mathbf{v} \cdot \nabla \phi = \gamma \nabla \cdot \left[\varepsilon \nabla \phi - \phi(1-\phi^2)\mathbf{n}\right]$$

where:
- φ is the level-set function: φ = 1 in ink, φ = -1 in air
- γ = 1 is the interface mobility parameter
- ε = 5×10⁻⁶ m is the diffuse interface thickness
- **n** = ∇φ/|∇φ| is the interface normal

#### Surface Tension Force

The surface tension body force is:
$$\mathbf{F}_\sigma = \sigma \kappa \delta(\phi) \mathbf{n}$$

with:
- σ = 40×10⁻³ N/m: ink-air surface tension
- κ = ∇·**n**: interface curvature
- δ(φ) = (3/2ε)|∇φ|: Dirac delta function approximation

### 2.4 Boundary Conditions

#### Solid Walls (No-Slip Condition)
$$\mathbf{v} = \mathbf{0} \quad \text{on } \Gamma_{\text{wall}}$$

#### Wetting Condition (Contact Angle)

On wetted walls, the interface normal satisfies:
$$\mathbf{n}_w \cdot \nabla \phi = -\frac{1}{\varepsilon}\cos(\theta) \quad \text{on } \Gamma_{\text{wall}}$$

with θ the static contact angle:
- θ_gold = 35 to 75° on the gold electrode
- θ_wall_EG = 35 to 90°
- θ_wall_EG = 35 to 90°
- θ_top = 180° on the top surface (no wetting on the piston)

#### Inlet (Syringe)
$$\mathbf{v} = v_{\text{inlet}}(t)\mathbf{e}_y \quad \text{on } \Gamma_{\text{inlet}}$$
$$\phi = 1 \quad \text{(ink)}$$

with v_inlet(t) = v₀·H(t)·H(t_dispense - t) where v₀ = 0.1 m/s

#### Outlet (Atmospheric Pressure)
$$p = p_{\text{atm}} = 0 \quad \text{on } \Gamma_{\text{outlet}}$$

### 2.5 Initial Conditions

At t = 0:
- **v**(x,y,0) = **0** throughout the domain
- φ(x,y,0) = -1 (air) in the well
- φ(x,y,0) = 1 (ink) in the syringe

---

## 3. SYSTEM PHYSICAL PARAMETERS

### 3.1 Fluid Properties

| Property | Ink (Phase 1) | Air (Phase 2) | Unit |
|----------|---------------|---------------|------|
| Density ρ | 3000 |- | kg/m³ |
| Viscosity η₀ | 1.5 to 5 | 1×10⁻⁵ | Pa·s |
| Viscosity η_∞ | 0.5 | - | Pa·s |
| Relaxation time λ | 0.15 | - | s |
| Index n | 0.7 | - | - |

### 3.2 Interfacial Properties

| Property | Value | Unit |
|----------|-------|------|
| Surface tension σ | 40×10⁻³ | mN/m |
| Interface thickness ε | 5×10⁻⁶ | m |
| Interface mobility γ | 1 | - |

### 3.3 System Geometry

| Element | Parameter | Value | Unit |
|---------|-----------|-------|------|
| Well | Diameter D_w | 0.8 to 1.5 | mm |
| | Height h_w | 0.128 | mm |
| | Volume V_w | 64.3 | nL |
| Syringe | Diameter D_s | 0.20 to 0.30 | mm |
| | Distance Δz | +30 | μm |
| | Surface ratio | 0.8 | - | (i.e., 80% well fill)

### 3.4 Process Parameters

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Dispense time | t_dispense | 40 | ms |
| Initial velocity | v₀ | 0.1 | m/s |
| Initial pressure | p₀ | 700 | Pa | (not used in model)
| Fill ratio | 80 | % |

---

## 4. FINITE ELEMENT DISCRETIZATION

### 4.1 Weak Formulation

The finite element method is based on the **variational** (or weak) formulation of the equations. We multiply the equations by test functions and integrate over the domain.

#### Weak Formulation of Navier-Stokes

Find $(\mathbf{v}, p) \in V \times Q$ such that for all $(\mathbf{w}, q) \in V \times Q$:

$$\int_\Omega \rho \frac{\partial \mathbf{v}}{\partial t} \cdot \mathbf{w} \, d\Omega + \int_\Omega \rho (\mathbf{v} \cdot \nabla)\mathbf{v} \cdot \mathbf{w} \, d\Omega + \int_\Omega 2\eta \mathbf{D}(\mathbf{v}) : \mathbf{D}(\mathbf{w}) \, d\Omega$$

$$- \int_\Omega p \, \nabla \cdot \mathbf{w} \, d\Omega + \int_\Omega q \, \nabla \cdot \mathbf{v} \, d\Omega = \int_\Omega \mathbf{f} \cdot \mathbf{w} \, d\Omega$$

where:
- $V$: velocity function space (satisfying boundary conditions)
- $Q$: pressure function space
- $\mathbf{w}$: velocity test function
- $q$: pressure test function

### 4.2 Mixed Finite Elements

The choice of approximation spaces for velocity and pressure is crucial to avoid **spurious pressure modes** (non-physical oscillations).

#### Inf-Sup Compatibility Condition (Ladyzhenskaya-Babuška-Brezzi)

The spaces must satisfy:

$$\sup_{\mathbf{v} \in V_h} \frac{\int_\Omega q \, \nabla \cdot \mathbf{v} \, d\Omega}{\|\mathbf{v}\|_V} \geq \beta \|q\|_Q \quad \forall q \in Q_h$$

with $\beta > 0$ independent of mesh size $h$.

#### Taylor-Hood Elements (P2-P1)

The **Taylor-Hood** element is the standard for incompressible flows:

| Component | Space | Degree | Continuity |
|-----------|-------|--------|------------|
| Velocity $\mathbf{v}$ | P2 (quadratic Lagrange) | 2 | C⁰ |
| Pressure $p$ | P1 (linear Lagrange) | 1 | C⁰ |

**Advantages:**
- Guaranteed inf-sup stability
- Quadratic accuracy for velocity
- Improved local mass conservation

**Number of DOFs per triangle:** 6 (velocity) + 3 (pressure) = 9 DOFs per element

#### MINI Elements (P1b-P1)

An economical alternative to Taylor-Hood:

| Component | Space | Description |
|-----------|-------|-------------|
| Velocity $\mathbf{v}$ | P1 + bubble | Linear enriched with bubble function |
| Pressure $p$ | P1 | Linear |

The **bubble function** $b(\mathbf{x})$ is defined by:

$$b(\mathbf{x}) = 27 \lambda_1 \lambda_2 \lambda_3$$

where $\lambda_i$ are the barycentric coordinates of the triangle.

**Advantage:** Fewer DOFs than Taylor-Hood (stability at the cost of lower accuracy).

### 4.3 Stabilization for Convection

At high Reynolds numbers ($Re > 10$), standard finite element schemes suffer from **numerical instabilities** (oscillations, numerical diffusion).

#### SUPG (Streamline Upwind Petrov-Galerkin)

The **SUPG** method adds artificial diffusion in the flow direction:

$$\int_\Omega \left(\mathbf{w} + \tau_{SUPG} \mathbf{v} \cdot \nabla \mathbf{w}\right) \cdot \mathcal{R}(\mathbf{v}, p) \, d\Omega = 0$$

where $\mathcal{R}$ is the residual of the Navier-Stokes equations and:

$$\tau_{SUPG} = \left[\left(\frac{2}{\Delta t}\right)^2 + \left(\frac{2|\mathbf{v}|}{h}\right)^2 + \left(\frac{4\nu}{h^2}\right)^2\right]^{-1/2}$$

with $h$ the characteristic element size.

#### PSPG (Pressure Stabilizing Petrov-Galerkin)

For elements that do not satisfy the inf-sup condition (e.g., P1-P1), **PSPG** stabilizes the pressure:

$$\int_\Omega \tau_{PSPG} \nabla q \cdot \mathcal{R}(\mathbf{v}, p) \, d\Omega$$

with $\tau_{PSPG} = \tau_{SUPG}$ (same stabilization parameter).

#### GLS (Galerkin Least-Squares)

Combining SUPG and PSPG in a unified formulation (**GLS**) provides stabilization and consistency:

$$a(\mathbf{v}, p; \mathbf{w}, q) + \sum_K \int_K \tau \mathcal{L}(\mathbf{w}, q) \cdot \mathcal{R}(\mathbf{v}, p) \, dK = \ell(\mathbf{w}, q)$$

where $\mathcal{L}$ is the adjoint operator.

---

## 5. ADVANCED RHEOLOGICAL MODELS

### 5.1 Herschel-Bulkley Model (Yield Stress Fluids)

For inks exhibiting a **yield stress**, the Herschel-Bulkley model is:

| Condition | Stress tensor $\boldsymbol{\tau}$ |
|-----------|-----------------------------------|
| $\|\boldsymbol{\tau}\| > \tau_0$ | $\boldsymbol{\tau} = \left(\frac{\tau_0}{\dot{\gamma}} + K\dot{\gamma}^{n-1}\right)\dot{\boldsymbol{\gamma}}$ |
| otherwise | $\boldsymbol{\tau} = \mathbf{0}$ |

where:
- $\tau_0$: yield stress [Pa]
- $K$: consistency [Pa·sⁿ]
- $n$: flow behavior index

**Papanastasiou Regularization** (avoids singularity at $\dot{\gamma} = 0$):

$$\eta_{eff}(\dot{\gamma}) = K\dot{\gamma}^{n-1} + \tau_0 \frac{1 - e^{-m\dot{\gamma}}}{\dot{\gamma}}$$

with $m$ a regularization parameter (typically $m = 100$ s).

### 5.2 Oldroyd-B Model (Viscoelasticity)

For **viscoelastic** inks (with elastic memory), the polymeric stress tensor $\boldsymbol{\tau}_p$ evolves according to:

$$\boldsymbol{\tau}_p + \lambda_1 \stackrel{\nabla}{\boldsymbol{\tau}_p} = 2\eta_p \mathbf{D}$$

where $\stackrel{\nabla}{\boldsymbol{\tau}_p}$ is the **upper-convected derivative**:

$$\stackrel{\nabla}{\boldsymbol{\tau}_p} = \frac{\partial \boldsymbol{\tau}_p}{\partial t} + (\mathbf{v} \cdot \nabla)\boldsymbol{\tau}_p - (\nabla \mathbf{v})^T \cdot \boldsymbol{\tau}_p - \boldsymbol{\tau}_p \cdot \nabla \mathbf{v}$$

**Parameters:**
- $\lambda_1$: relaxation time [s]
- $\eta_p$: polymer viscosity [Pa·s]
- $\eta_s$: solvent viscosity [Pa·s]

The total viscosity is $\eta = \eta_s + \eta_p$.

**Deborah Number:** $De = \lambda_1 \dot{\gamma}$ (measures the importance of elastic effects)

### 5.3 Giesekus Model (Nonlinear)

For strongly nonlinear inks, the **Giesekus** model adds a quadratic term:

$$\boldsymbol{\tau}_p + \lambda_1 \stackrel{\nabla}{\boldsymbol{\tau}_p} + \frac{\alpha \lambda_1}{\eta_p} \boldsymbol{\tau}_p \cdot \boldsymbol{\tau}_p = 2\eta_p \mathbf{D}$$

where $\alpha \in [0, 0.5]$ is the anisotropic mobility parameter.

---

## 6. FLUID-STRUCTURE INTERACTION (FSI)

### 6.1 Piezoelectric Actuation

In piezoelectric print heads, ejection is caused by membrane deformation under an electric voltage.

#### Piezo Equations (Linear Formulation)

$$\boldsymbol{\sigma}^{piezo} = \mathbf{C}^E : \boldsymbol{\varepsilon} - \mathbf{e}^T \cdot \mathbf{E}$$

$$\mathbf{D} = \mathbf{e} : \boldsymbol{\varepsilon} + \boldsymbol{\epsilon}^S \cdot \mathbf{E}$$

where:
- $\boldsymbol{\sigma}^{piezo}$: mechanical stress tensor
- $\boldsymbol{\varepsilon}$: strain tensor
- $\mathbf{E}$: electric field
- $\mathbf{D}$: electric displacement
- $\mathbf{C}^E$: elasticity tensor at constant electric field
- $\mathbf{e}$: piezoelectric tensor
- $\boldsymbol{\epsilon}^S$: permittivity at constant strain

### 6.2 Fluid-Solid Interface

At the interface between the fluid and the piezoelectric membrane:

**Velocity Continuity:**
$$\mathbf{v}_{fluid} = \frac{\partial \mathbf{u}_{solid}}{\partial t}$$

**Stress Equilibrium:**
$$\boldsymbol{\sigma}_{fluid} \cdot \mathbf{n} = \boldsymbol{\sigma}_{solid} \cdot \mathbf{n}$$

### 6.3 Moving Mesh (ALE)

To handle fluid domain deformation, we use the **ALE (Arbitrary Lagrangian-Eulerian)** formulation:

$$\rho \left[\left.\frac{\partial \mathbf{v}}{\partial t}\right|_{\chi} + (\mathbf{v} - \mathbf{v}_{mesh}) \cdot \nabla \mathbf{v}\right] = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \mathbf{F}$$

where:
- $\left.\frac{\partial}{\partial t}\right|_{\chi}$: derivative at fixed ALE coordinates
- $\mathbf{v}_{mesh}$: mesh velocity

**Mesh Smoothing:** Laplace equation for nodal displacements:

$$\nabla^2 \mathbf{d}_{mesh} = 0$$

with boundary conditions fixed on immobile boundaries.

---

## 7. VALIDATION RESULTS

### 7.1 Hirsa & Basaran Study (2017) - Viscoelastic Inks

**Configuration:**
- Solver: COMSOL Multiphysics (FEM Phase-Field)
- Elements: Taylor-Hood (P2-P1)
- Mesh: 50,000 elements with adaptive refinement
- Rheology: Oldroyd-B ($\lambda_1 = 0.1$ ms, $De = 0.5$)

**Conditions:**
- Nozzle diameter: $D = 30$ µm
- Ejection velocity: $v_{max} = 15$ m/s
- $We = 4.5$, $Oh = 0.08$

**Results:**

| Parameter | Simulation | Experimental | Error (%) |
|-----------|------------|--------------|-----------|
| Droplet velocity (m/s) | 14.8 | 15.0 ± 0.2 | 1.3 |
| Droplet diameter (µm) | 29.2 | 29.5 ± 0.5 | 1.0 |
| Pinch-off time (µs) | 18.5 | 18.0 ± 0.5 | 2.8 |
| Filament length (µm) | 145 | 148 ± 3 | 2.0 |

**Key Observation:** Viscoelasticity delays filament pinch-off (stabilizing effect) and reduces satellite volume by 25% compared to an equivalent Newtonian fluid.

### 7.2 Patel et al. Study (2020) - Piezo Coupling

**Configuration:**
- Solver: FEniCS + piezo model
- Coupling: Monolithic (fluid + structure)
- Mesh: 80,000 elements (refinement at meniscus)
- Actuation: Trapezoidal wave ($V_{max} = 20$ V, $\tau_{rise} = 2$ µs)

**Results:**

| Actuation parameter | Effect on droplet |
|---------------------|-------------------|
| $\tau_{rise}$ ↓ | Velocity ↑, satellites ↑ |
| $V_{max}$ ↑ | Volume ↑, velocity ↑ |
| Trapezoidal shape | Fewer satellites than sinusoidal wave |

**Optimization:** 40% reduction in satellites by adjusting $\tau_{fall}/\tau_{rise} = 1.5$.

### 7.3 Comparison with Other Methods

| Criterion | FEM (Phase-Field) | VOF | LBM | SPH |
|-----------|-------------------|-----|-----|-----|
| Velocity error (%) | **0.8** | 1.2 | 1.8 | 2.5 |
| Diameter error (%) | **1.5** | 2.1 | 3.0 | 4.2 |
| Oldroyd-B support | **Yes** | No | Yes | Yes |
| FSI coupling | **Native** | Difficult | Difficult | Medium |

---

## 8. COMPUTATIONAL COST

### 8.1 Typical Configuration

For a 2D axisymmetric simulation (1 ms ejection, Taylor-Hood elements):

| Configuration | Elements | Time (h) | Hardware |
|---------------|----------|----------|----------|
| Standard | 20k | 4–8 | 8 CPU cores |
| High resolution | 100k | 15–30 | 32 CPU cores |
| Full 3D | 500k | 30–50 | 64–128 cores + 128 GB RAM |

### 8.2 Scaling and Parallelization

The FEM method is **memory-bound** and limited by the cost of linear system assembly/solving.

**Typical Scaling (Hirsa 2017 study):**

| CPU Cores | Speed-up | Efficiency |
|-----------|----------|------------|
| 1 | 1× | 100% |
| 8 | 6.5× | 81% |
| 32 | 20× | 63% |
| 64 | 32× | 50% |

**GPU Limitation:** Classic FEM solvers (matrix assembly) do not significantly benefit from GPU acceleration, unlike LBM.

### 8.3 Optimizations

- **Adaptive Mesh Refinement (AMR)**: Refine only near the interface ($\alpha \in [0.05, 0.95]$)
- **Algebraic Preconditioners**: ILU, AMG for linear systems
- **Adaptive Time-Stepping**: Variable CFL with $\Delta t_{max} = 10^{-5}$ s

---

## 9. OPEN-SOURCE LIBRARIES

| Library | Language | Focus | Parallelization |
|---------|----------|-------|-----------------|
| **FEniCS** | Python/C++ | Flexibility, prototyping | MPI, PETSc |
| **deal.II** | C++ | Performance, adaptivity | MPI, Trilinos |
| **FreeFEM** | DSL | Rapid implementation | MPI, MUMPS |
| **Firedrake** | Python | Automation, GPU | MPI, PETSc |
| **COMSOL** | GUI/MATLAB | Commercial, multiphysics | Multi-core |

### 9.1 FEniCS Example (Phase-Field)

```python
from fenics import *

# Mesh and spaces
mesh = RectangleMesh(Point(0, 0), Point(L, H), nx, ny)
V = VectorFunctionSpace(mesh, "P", 2)  # Velocity P2
Q = FunctionSpace(mesh, "P", 1)        # Pressure P1
W = MixedFunctionSpace([V, Q])

# Variational formulation
(v, p) = TrialFunctions(W)
(w, q) = TestFunctions(W)

F = (rho * dot((v - v_n) / dt, w) * dx
     + rho * dot(dot(v, nabla_grad(v)), w) * dx
     + 2 * eta * inner(sym(grad(v)), sym(grad(w))) * dx
     - p * div(w) * dx
     + q * div(v) * dx
     - dot(f_sigma, w) * dx)

# Solve
solve(lhs(F) == rhs(F), w_sol, bcs)
```

---

## 10. REFERENCES

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.

