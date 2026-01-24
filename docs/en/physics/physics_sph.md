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

The **SPH (Smoothed Particle Hydrodynamics)** method is a **Lagrangian** and **meshless** approach where the fluid is represented by a set of mobile particles carrying physical properties.

### Main Variable: Particles

Unlike grid-based methods (VOF, FEM, LBM), there are no fixed connections between points. The value of a property A at position **r** is calculated by **interpolation**:

$$A(\mathbf{r}) = \sum_b m_b \frac{A_b}{\rho_b} W(|\mathbf{r} - \mathbf{r}_b|, h)$$

where W is the **smoothing kernel** and h the **smoothing length**.

**Key Advantage:** Natural handling of complex free surfaces (breakup, splashing) without mesh deformation.

---

## 2. Fundamental Equations

### 2.1 Momentum Equation

$$m_a \frac{d\mathbf{v}_a}{dt} = -\sum_b m_b \left(\frac{p_a}{\rho_a^2} + \frac{p_b}{\rho_b^2} + \Pi_{ab}\right) \nabla_a W_{ab} + \mathbf{f}_\sigma$$

where:
- p_a, p_b = particle pressures
- Π_ab = artificial viscosity term
- **f**_σ = surface tension force

### 2.2 Equation of State (Weakly Compressible)

$$p = c_0^2 (\rho - \rho_0) \quad \text{or} \quad p = B\left[\left(\frac{\rho}{\rho_0}\right)^\gamma - 1\right]$$

with c_0 = 10·v_max (numerical speed of sound) and γ = 7 for liquids.

### 2.3 Surface Tension (Adapted CSF)

$$\mathbf{F}_{st} = -\sigma \kappa \mathbf{n}$$

where **n** = ∇c is the normal calculated from the color field gradient c.

---

## 3. Mathematical Formulation

### 3.1 Cubic Spline Smoothing Kernel

| Domain | Expression |
|--------|------------|
| 0 ≤ q < 1 | W(q) = σ_d/h^d · (1 - 3q²/2 + 3q³/4) |
| 1 ≤ q < 2 | W(q) = σ_d/h^d · (2-q)³/4 |
| q ≥ 2 | W(q) = 0 |

with q = r/h and σ_d the normalization factor.

### 3.2 Artificial Viscosity (Monaghan)

| Condition | Π_ab |
|-----------|------|
| **v**_ab · **r**_ab < 0 | Π_ab = (-α c̄_ab μ_ab + β μ_ab²) / ρ̄_ab |
| otherwise | Π_ab = 0 |

**Typical parameters:** α = 0.1, β = 0

### 3.3 Boundary Conditions (Ghost Particles)

Walls are made of layers of fixed **ghost particles** that:
- Exert a repulsive pressure
- Impose the no-slip condition
- Extrapolate properties from the fluid

### 3.4 Non-Newtonian Fluids

The stress tensor depends on the shear rate:

$$\boldsymbol{\tau}_a = K|\dot{\gamma}_a|^{n-1} \dot{\gamma}_a$$

**SPH Advantage:** Natural handling of **thixotropy** (time-dependent viscosity) thanks to the Lagrangian approach.

---

## 4. Advantages and Limitations

| Advantages | Limitations |
|------------|-------------|
| Complex free surfaces (breakup, splashing) | Numerical noise (pressure oscillations) |
| Exact advection (no numerical diffusion) | Difficult boundary conditions |
| Natural coalescence | High memory cost (10⁶ particles) |
| Native thixotropy (Lagrangian) | Instabilities at high velocity (> 20 m/s) |
| GPU scalability (x10-x15) | Delicate calibration (h, α) |

---

## 5. Computational Cost

**Reference domain:** 1.2 mm × 0.5 mm (micro-via dispensing)

| Configuration | Particles | Spacing | Time | Hardware |
|---------------|-----------|---------|------|----------|
| **This project** | ~1k | 15–20 µm | **1–2 h** | 8 cores |
| High resolution | ~10k | 5–10 µm | 4–8 h | 8 cores |
| 3D standard | ~1M | 5 µm | 5–10 h | GPU |

> **Interpretation:** ~1000 particles on 1.2×0.5 mm yield an average spacing of 15–20 µm. The smoothing length $h$ is typically 1.3× this spacing. Unoptimized PySPH code.

**GPU Acceleration:** x10–x15 vs CPU for simulations > 100k particles.

---

## 6. Open-Source Libraries

| Library | Language | GPU | Focus |
|---------|----------|-----|-------|
| **PySPH** | Python/Cython | CUDA, OpenCL | Flexibility, prototyping |
| **DualSPHysics** | C++/CUDA | Native CUDA | Performance, coastal applications |
| **GPUSPH** | C++/CUDA | CUDA | Geophysical flows |
| **SPHinXsys** | C++ | OpenMP | Multiphysics coupling |

---

## 7. References

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.
