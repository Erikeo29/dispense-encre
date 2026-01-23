**Contents:**
1. Method Principle
2. Fundamental Equations
3. Mathematical Formulation
4. Advantages and Limitations
5. Computational Cost
6. Open-Source Libraries
7. References

---

## 1. Method Principle

The **Phase-Field** method coupled with **Finite Elements (FEM)** is an Eulerian approach for simulating two-phase flows. The interface between the two fluids is represented as a **diffuse transition zone** of finite thickness ε.

### Main Variable: Phase Function φ

| Value | Meaning |
|-------|---------|
| φ = +1 | Ink (fluid 1) |
| φ = -1 | Air (fluid 2) |
| -1 < φ < +1 | Interface zone |

**Key Advantage:** Topological changes (coalescence, breakup) are handled automatically without numerical intervention.

---

## 2. Fundamental Equations

### 2.1 Navier-Stokes Equations

**Mass conservation (incompressible):**
$$\nabla \cdot \mathbf{v} = 0$$

**Momentum conservation:**
$$\rho(\phi)\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p + \nabla \cdot [2\eta(\phi,\dot{\gamma})\mathbf{D}] + \mathbf{F}_\sigma$$

where **D** is the strain rate tensor and **F**_σ the surface tension force.

### 2.2 Phase-Field Transport Equation

$$\frac{\partial \phi}{\partial t} + \mathbf{v} \cdot \nabla \phi = \gamma \nabla \cdot \left[\varepsilon \nabla \phi - \phi(1-\phi^2)\mathbf{n}\right]$$

with γ = interface mobility, ε = interface thickness, **n** = interface normal.

### 2.3 Surface Tension Force

$$\mathbf{F}_\sigma = \sigma \kappa \delta(\phi) \mathbf{n}$$

where σ = surface tension, κ = curvature, δ(φ) = delta function localized at the interface.

---

## 3. Mathematical Formulation

### 3.1 Carreau Rheological Model

The shear-thinning ink viscosity follows:

$$\eta(\dot{\gamma}) = \eta_{\infty} + (\eta_0 - \eta_{\infty})\left[1 + (\lambda\dot{\gamma})^2\right]^{\frac{n-1}{2}}$$

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Zero-shear viscosity | η₀ | 1.5 – 5 | Pa·s |
| Infinite-shear viscosity | η∞ | 0.05 | Pa·s |
| Relaxation time | λ | 0.15 | s |
| Power-law index | n | 0.7 | - |

### 3.2 Mixture Properties

$$\rho(\phi) = \rho_1 H(\phi) + \rho_2 [1-H(\phi)]$$
$$\eta(\phi) = \eta_1 H(\phi) + \eta_2 [1-H(\phi)]$$

where H(φ) is a regularized Heaviside function.

### 3.3 Boundary Conditions

| Surface | Condition |
|---------|-----------|
| Walls | No-slip: **v** = **0** |
| Gold electrode | Contact angle: θ = 35–75° |
| Micro-via walls | Contact angle: θ = 35–90° |
| Inlet (nozzle) | Imposed velocity: v = 0.1 m/s |
| Outlet | Atmospheric pressure: p = 0 |

### 3.4 Taylor-Hood Finite Elements (P2-P1)

| Variable | Element | Degree |
|----------|---------|--------|
| Velocity **v** | Quadratic Lagrange (P2) | 2 |
| Pressure p | Linear Lagrange (P1) | 1 |

This combination ensures inf-sup stability and avoids pressure oscillations.

---

## 4. Advantages and Limitations

| Advantages | Limitations |
|------------|-------------|
| Thermodynamic consistency | High memory cost (fine mesh required) |
| Automatic coalescence/breakup | Limited GPU scalability |
| Native multiphysics coupling (FSI) | Interface resolution depends on ε |
| High accuracy (error < 2%) | Significant computation time in 3D |
| Complex rheology support | Delicate γ and ε calibration |

---

## 5. Computational Cost

| Configuration | Elements | Time | Hardware |
|---------------|----------|------|----------|
| 2D standard | 20k | 4–8 h | 8 CPU cores |
| 2D high resolution | 100k | 15–30 h | 32 CPU cores |
| 3D complete | 500k | 30–50 h | 64 cores + 128 GB RAM |

**Note:** Classical FEM (matrix assembly) benefits little from GPU acceleration, unlike LBM.

---

## 6. Open-Source Libraries

| Library | Language | Focus | Parallelization |
|---------|----------|-------|-----------------|
| **FEniCS** | Python/C++ | Flexibility, prototyping | MPI, PETSc |
| **Firedrake** | Python | Automation, GPU | MPI, PETSc |
| **deal.II** | C++ | Performance, adaptivity | MPI, Trilinos |
| **FreeFEM** | DSL | Rapid implementation | MPI, MUMPS |

---

## 7. References

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.
