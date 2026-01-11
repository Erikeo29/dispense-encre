<div style="font-size: 0.9em; line-height: 1.3; background: #f8f9fa; padding: 8px 12px; border-radius: 4px; margin-bottom: 1em;">

**Contents:** 1. Fundamental Principle • 2. Fundamental Equations • 3. Interface Reconstruction Schemes • 4. Non-Newtonian Fluids • 5. OpenFOAM Configuration • 6. Advantages and Limitations • 7. Validation Results • 8. Computational Cost • 9. References
</div>

## 1. Fundamental Principle

The **VOF (Volume of Fluid)** method is an Eulerian approach for interface tracking in two-phase flows. It represents the industry standard for free surface simulations, particularly in OpenFOAM with the `interFoam` solver.

### 1.1 Volume Fraction Concept

The interface between the two fluids is captured by a scalar variable, the **volume fraction** $\alpha$:

- $\alpha = 1$: Pure Fluid 1 (ink)
- $\alpha = 0$: Pure Fluid 2 (air)
- $0 < \alpha < 1$: Interface zone (transition)

This approach is called "diffuse interface" because the interface is not a sharp line but a transition zone spanning several cells.

---

## 2. Fundamental Equations

### 2.1 Transport Equation for $\alpha$

The evolution of the volume fraction is governed by the advection equation:

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

where $\mathbf{v}$ is the velocity field.

### 2.2 Surface Tension Force (CSF)

Surface tension is modeled via Brackbill's **Continuum Surface Force (CSF)** model:

$$\mathbf{f}_\sigma = \sigma \kappa \nabla \alpha$$

where:
- $\sigma$: surface tension [N/m]
- $\kappa = -\nabla \cdot \left(\frac{\nabla \alpha}{|\nabla \alpha|}\right)$: interface curvature

### 2.3 Mixture Properties

Physical properties are linearly interpolated:

$$\rho = \alpha \rho_1 + (1-\alpha) \rho_2$$

$$\eta = \alpha \eta_1 + (1-\alpha) \eta_2$$

---

## 3. Interface Reconstruction Schemes

### 3.1 Numerical Diffusion Problem

Transporting $\alpha$ by pure advection leads to **numerical diffusion** of the interface, spreading it over several cells. Several schemes exist to maintain a sharp interface:

### 3.2 PLIC (Piecewise Linear Interface Calculation)

The **PLIC** scheme reconstructs the interface as a plane within each cell:

$$\mathbf{n} \cdot \mathbf{x} = d$$

where $\mathbf{n} = \frac{\nabla \alpha}{|\nabla \alpha|}$ is the interface normal and $d$ the distance from the origin.

**Advantages:**
- Interface precision of 0.1–1 µm
- Exact mass conservation
- Standard in OpenFOAM

### 3.3 Geometric VOF

Uses geometric algorithms to compute $\alpha$ fluxes between cells:
- Exact calculation of fluid volumes crossing each face
- More expensive but more accurate than algebraic schemes

### 3.4 Compressive VOF (OpenFOAM)

OpenFOAM adds an **artificial compression** term (MULES):

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\mathbf{v} \alpha) + \nabla \cdot [\mathbf{v}_r \alpha (1-\alpha)] = 0$$

where $\mathbf{v}_r = c_\alpha |\mathbf{v}| \mathbf{n}$ is an artificial compression velocity acting **only at the interface** ($\alpha(1-\alpha) \neq 0$) to counteract diffusion.

**Key Parameter:** $c_\alpha = 1$ (default value in OpenFOAM)

---

## 4. Adaptation for Non-Newtonian Fluids

### 4.1 Stress Tensor

For shear-thinning inks, the stress tensor $\boldsymbol{\tau}$ is modified to include shear rate $\dot{\gamma}$ dependence:

$$\boldsymbol{\tau} = K|\dot{\gamma}|^{n-1}\dot{\gamma}$$

where $\dot{\gamma} = \sqrt{2\mathbf{D}:\mathbf{D}}$ and $\mathbf{D} = \frac{1}{2}\left(\nabla \mathbf{v} + (\nabla \mathbf{v})^T\right)$.

### 4.2 Carreau Model in OpenFOAM

The effective viscosity $\eta_{eff}$ follows the Carreau model:

$$\eta_{eff}(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) [1 + (\lambda \dot{\gamma})^2]^{(n-1)/2}$$

**Typical Parameters for Shear-Thinning Ink:**

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Density | $\rho$ | 3000 | kg/m³ |
| Zero-shear viscosity | $\eta_0$ | 0.5 – 5 | Pa·s |
| Infinite-shear viscosity | $\eta_\infty$ | 0.05 – 0.167 | Pa·s |
| Relaxation time | $\lambda$ | 0.15 | s |
| Power-law index | $n$ | 0.7 | - |
| Surface tension | $\sigma$ | 0.04 | N/m |

---

## 5. OpenFOAM Configuration

### 5.1 `transportProperties` File

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

### 5.2 `interFoam` Solver

The `interFoam` solver solves:
1. Transport equation for $\alpha$ (MULES)
2. Navier-Stokes equations with variable properties
3. Pressure-velocity coupling (PIMPLE)

---

## 6. Advantages and Limitations

### 6.1 Strengths

- **Proven robustness**: Industry standard with >25 years of development
- **Perfect mass conservation**: Intrinsic property of the formulation
- **Open-source implementations**: OpenFOAM, Basilisk
- **Interface precision**: 0.1–1 µm with PLIC and adaptive mesh refinement (AMR)

### 6.2 Limitations

- **Numerical diffusivity**: Requires expensive reconstruction schemes
- **Memory cost**: Fine meshes required for thin interfaces
- **Multiple coalescences**: Difficult to handle properly
- **Newtonian rheology**: Simple laws (Carreau) work, complex laws (thixotropy) are difficult

---

## 7. Validation Results

### 7.1 Duarte et al. Study (2019)

**Configuration:**
- Solver: OpenFOAM (`interFoam`)
- Adaptive mesh refinement (AMR) with minimum cell size = 0.2 µm
- Newtonian ink ($\sigma = 35$ mN/m, $\eta = 4$ mPa·s)

**Results:**
- Filament length before detachment: 150 µm (experimental: 148 ± 2 µm)
- Droplet velocity: 12 m/s (error < 2%)
- Satellite formation: 8% of total volume at $t = 15$ µs

### 7.2 Li et al. Study (2021) - Non-Newtonian Fluids

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

## 8. Computational Cost

### 8.1 Typical Configuration

For a 2D axisymmetric simulation (1 ms ejection):

| Configuration | Mesh | Time (h) | Hardware |
|---------------|------|----------|----------|
| Standard | 100k cells | 2–4 | 8 CPU cores |
| High resolution | 500k cells | 8–12 | 16 CPU cores |
| AMR | 100k–1M (adaptive) | 4–8 | 16 cores + GPU |

**GPU Impact:** OpenFOAM has supported CUDA since version 10, with x5–x10 speedups for matrix operations.

---

## 9. References

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.
