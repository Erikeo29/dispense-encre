# Volume of Fluid (VOF) Method

## Fundamental Principle

The **VOF (Volume of Fluid)** method is an Eulerian approach for interface tracking in two-phase flows. It represents the industry standard for free surface simulations, particularly in OpenFOAM with the `interFoam` solver.

### Volume Fraction Concept

The interface between the two fluids is captured by a scalar variable, the **volume fraction** $\alpha$:

- $\alpha = 1$: Pure Fluid 1 (ink)
- $\alpha = 0$: Pure Fluid 2 (air)
- $0 < \alpha < 1$: Interface zone (transition)

This approach is called "diffuse interface" because the interface is not a sharp line but a transition zone spanning several cells.

---

## Fundamental Equations

### Transport Equation for $\alpha$

The evolution of the volume fraction is governed by the advection equation:

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

where $\mathbf{v}$ is the velocity field.

### Surface Tension Force (CSF)

Surface tension is modeled via Brackbill's **Continuum Surface Force (CSF)** model:

$$\mathbf{f}_\sigma = \sigma \kappa \nabla \alpha$$

where:
- $\sigma$: surface tension [N/m]
- $\kappa = -\nabla \cdot \left(\frac{\nabla \alpha}{|\nabla \alpha|}\right)$: interface curvature

### Mixture Properties

Physical properties are linearly interpolated:

$$\rho = \alpha \rho_1 + (1-\alpha) \rho_2$$

$$\eta = \alpha \eta_1 + (1-\alpha) \eta_2$$

---

## Interface Reconstruction Schemes

### Numerical Diffusion Problem

Transporting $\alpha$ by pure advection leads to **numerical diffusion** of the interface, spreading it over several cells. Several schemes exist to maintain a sharp interface:

### PLIC (Piecewise Linear Interface Calculation)

The **PLIC** scheme reconstructs the interface as a plane within each cell:

$$\mathbf{n} \cdot \mathbf{x} = d$$

where $\mathbf{n} = \frac{\nabla \alpha}{|\nabla \alpha|}$ is the interface normal and $d$ the distance from the origin.

**Advantages:**
- Interface precision of 0.1–1 µm
- Exact mass conservation
- Standard in OpenFOAM

### Geometric VOF

Uses geometric algorithms to compute $\alpha$ fluxes between cells:
- Exact calculation of fluid volumes crossing each face
- More expensive but more accurate than algebraic schemes

### Compressive VOF (OpenFOAM)

OpenFOAM adds an **artificial compression** term (MULES):

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\mathbf{v} \alpha) + \nabla \cdot [\mathbf{v}_r \alpha (1-\alpha)] = 0$$

where $\mathbf{v}_r = c_\alpha |\mathbf{v}| \mathbf{n}$ is an artificial compression velocity acting **only at the interface** ($\alpha(1-\alpha) \neq 0$) to counteract diffusion.

**Key Parameter:** $c_\alpha = 1$ (default value in OpenFOAM)

---

## Adaptation for Non-Newtonian Fluids

### Stress Tensor

For shear-thinning inks, the stress tensor $\boldsymbol{\tau}$ is modified to include shear rate $\dot{\gamma}$ dependence:

$$\boldsymbol{\tau} = K|\dot{\gamma}|^{n-1}\dot{\gamma}$$

where $\dot{\gamma} = \sqrt{2\mathbf{D}:\mathbf{D}}$ and $\mathbf{D} = \frac{1}{2}\left(\nabla \mathbf{v} + (\nabla \mathbf{v})^T\right)$.

### Carreau Model in OpenFOAM

The effective viscosity $\eta_{eff}$ follows the Carreau model:

$$\eta_{eff}(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) [1 + (\lambda \dot{\gamma})^2]^{(n-1)/2}$$

**Typical Parameters for Ag/AgCl Ink:**

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Density | $\rho$ | 3000 | kg/m³ |
| Zero-shear viscosity | $\eta_0$ | 0.5 – 5 | Pa·s |
| Infinite-shear viscosity | $\eta_\infty$ | 0.05 – 0.167 | Pa·s |
| Relaxation time | $\lambda$ | 0.15 | s |
| Power-law index | $n$ | 0.7 | - |
| Surface tension | $\sigma$ | 0.04 | N/m |

---

## OpenFOAM Configuration

### `transportProperties` File

```cpp
transportModel Carreau;

CarreauCoeffs
{
    nu0     nu0 [0 2 -1 0 0 0 0] 1.667e-4;  // η₀/ρ
    nuInf   nuInf [0 2 -1 0 0 0 0] 5.56e-5;  // η∞/ρ
    k       k [0 0 1 0 0 0 0] 0.15;          // λ
    n       n [0 0 0 0 0 0 0] 0.7;           // n
}

sigma   sigma [1 0 -2 0 0 0 0] 0.04;  // Surface tension
```

### `interFoam` Solver

The `interFoam` solver solves:
1. Transport equation for $\alpha$ (MULES)
2. Navier-Stokes equations with variable properties
3. Pressure-velocity coupling (PIMPLE)

---

## Advantages and Limitations

### Strengths

- **Proven robustness**: Industry standard with >25 years of development
- **Perfect mass conservation**: Intrinsic property of the formulation
- **Open-source implementations**: OpenFOAM, Basilisk
- **Interface precision**: 0.1–1 µm with PLIC and adaptive mesh refinement (AMR)

### Limitations

- **Numerical diffusivity**: Requires expensive reconstruction schemes
- **Memory cost**: Fine meshes required for thin interfaces
- **Multiple coalescences**: Difficult to handle properly
- **Newtonian rheology**: Simple laws (Carreau) work, complex laws (thixotropy) are difficult

---

## Validation Results

### Duarte et al. Study (2019)

**Configuration:**
- Solver: OpenFOAM (`interFoam`)
- Adaptive mesh refinement (AMR) with minimum cell size = 0.2 µm
- Newtonian ink ($\sigma = 35$ mN/m, $\eta = 4$ mPa·s)

**Results:**
- Filament length before detachment: 150 µm (experimental: 148 ± 2 µm)
- Droplet velocity: 12 m/s (error < 2%)
- Satellite formation: 8% of total volume at $t = 15$ µs

### Li et al. Study (2021) - Non-Newtonian Fluids

**Configuration:**
- Power law ($n = 0.7$, $K = 0.1$ Pa·sⁿ)
- $We = 3.5$, $Oh = 0.05$

**Results:**

| Parameter | Newtonian ($n=1$) | Shear-thinning ($n=0.7$) |
|-----------|-------------------|--------------------------|
| Pinch-off time (µs) | 18 ± 0.5 | 22 ± 0.8 |
| Satellite volume (%) | 12 | 8 |
| Droplet velocity (m/s) | 12.1 | 11.8 |

**Mechanism:** Shear-thinning reduces the effective viscosity in high-shear zones (filament), accelerating pinch-off while reducing satellites.

---

## Computational Cost

### Typical Configuration

For a 2D axisymmetric simulation (1 ms ejection):

| Configuration | Mesh | Time (h) | Hardware |
|---------------|------|----------|----------|
| Standard | 100k cells | 2–4 | 8 CPU cores |
| High resolution | 500k cells | 8–12 | 16 CPU cores |
| AMR | 100k–1M (adaptive) | 4–8 | 16 cores + GPU |

**GPU Impact:** OpenFOAM has supported CUDA since version 10, with x5–x10 speedups for matrix operations.

---

## References

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.
