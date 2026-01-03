# Smoothed Particle Hydrodynamics (SPH) Method

## Lagrangian Meshless Principle

The **SPH (Smoothed Particle Hydrodynamics)** method is a **Lagrangian** and **meshless** approach where the fluid is represented by a set of mobile particles carrying physical properties (mass, velocity, pressure).

### Fundamental Concept

Unlike grid-based methods (VOF, FEM), there are no fixed connections between discretization points. The value of a scalar property $A$ at position $\mathbf{r}$ is calculated by **interpolation** over neighboring particles:

$$A(\mathbf{r}) = \sum_b m_b \frac{A_b}{\rho_b} W(|\mathbf{r} - \mathbf{r}_b|, h)$$

where:
- $m_b$: mass of particle $b$
- $\rho_b$: density of particle $b$
- $W$: **smoothing kernel**
- $h$: **smoothing length**

---

## Smoothing Kernels

### Kernel Function

The kernel $W(r, h)$ must satisfy several properties:
- **Normalization**: $\int W(r, h) dV = 1$
- **Delta limit**: $\lim_{h \to 0} W(r, h) = \delta(r)$
- **Compact support**: $W(r, h) = 0$ for $r > \kappa h$ (typically $\kappa = 2$)

### Common Kernels

**Cubic Spline (M₄):**

| Domain | Expression |
|--------|------------|
| $0 \leq q < 1$ | $W(q) = \frac{\sigma_d}{h^d} \left(1 - \frac{3}{2}q^2 + \frac{3}{4}q^3\right)$ |
| $1 \leq q < 2$ | $W(q) = \frac{\sigma_d}{h^d} \cdot \frac{1}{4}(2-q)^3$ |
| $q \geq 2$ | $W(q) = 0$ |

with $q = r/h$ and $\sigma_d$ the dimensional normalization factor.

**Quintic Spline (M₆):**

More accurate but more expensive, reduces tensile instabilities.

**Wendland C4:**

$$W(q) = \frac{\sigma_d}{h^d} (1-q/2)^6 (35q^2/12 + 3q + 1) \quad \text{for } q < 2$$

Very stable for high-velocity flows.

---

## Equations of Motion

### Momentum Equation

The equation of motion for particle $a$ is:

$$m_a \frac{d\mathbf{v}_a}{dt} = -\sum_b m_b \left(\frac{p_a}{\rho_a^2} + \frac{p_b}{\rho_b^2} + \Pi_{ab}\right) \nabla_a W_{ab} + \mathbf{f}_\sigma$$

where:
- $p_a, p_b$: pressures of particles $a$ and $b$
- $\Pi_{ab}$: **artificial viscosity** term
- $\mathbf{f}_\sigma$: surface tension force

### Equation of State

Pressure is calculated by a weakly compressible equation of state:

$$p = c_0^2 (\rho - \rho_0) \quad \text{or} \quad p = B\left[\left(\frac{\rho}{\rho_0}\right)^\gamma - 1\right]$$

with $c_0$ the numerical speed of sound (typically $c_0 = 10 \cdot v_{max}$) and $\gamma = 7$ for liquids.

---

## Artificial Viscosity

### Necessity

Standard SPH suffers from numerical instabilities, including **pressure oscillations** and **tensile instabilities**. Artificial viscosity stabilizes the scheme.

### Monaghan Formulation

| Condition | Expression for $\Pi_{ab}$ |
|-----------|---------------------------|
| $\mathbf{v}_{ab} \cdot \mathbf{r}_{ab} < 0$ | $\Pi_{ab} = \frac{-\alpha \bar{c}_{ab} \mu_{ab} + \beta \mu_{ab}^2}{\bar{\rho}_{ab}}$ |
| otherwise | $\Pi_{ab} = 0$ |

with:

$$\mu_{ab} = \frac{h \mathbf{v}_{ab} \cdot \mathbf{r}_{ab}}{|\mathbf{r}_{ab}|^2 + \epsilon h^2}$$

**Typical Parameters:** $\alpha = 0.1$, $\beta = 0$, $\epsilon = 0.01$

---

## Surface Tension

### Morris Model (CSF)

The **Continuum Surface Force (CSF)** method adapted for SPH adds a body force based on interface curvature:

$$\mathbf{F}_{st} = -\sigma \kappa \mathbf{n}$$

where:
- $\mathbf{n} = \nabla c$: normal calculated from the **color field** gradient $c$ (1 in ink, 0 elsewhere)
- $\kappa = -\nabla \cdot \mathbf{n}$: interface curvature

### Curvature Calculation in SPH

$$\kappa_a = -\frac{1}{|\mathbf{n}_a|} \sum_b \frac{m_b}{\rho_b} (\mathbf{n}_b - \mathbf{n}_a) \cdot \nabla_a W_{ab}$$

**Limitation:** The CSF method introduces numerical noise, especially at thin interfaces.

### Pairwise Force Model

A more stable alternative based on interparticle forces:

$$\mathbf{F}_{st,a} = -\sigma \sum_b s_{ab} \frac{\mathbf{r}_{ab}}{|\mathbf{r}_{ab}|} W_{ab}$$

with $s_{ab}$ a tension coefficient depending on particle types.

---

## Boundary Conditions

### Problem

Managing watertight solid walls is **difficult** in SPH because particles have no fixed connections. Several approaches exist:

### Ghost Particles (Adami et al., 2012)

Walls consist of several layers of **fixed ghost (dummy) particles**:

1. These particles exert a **repulsive pressure** calculated dynamically
2. They impose the **no-slip** condition
3. Properties (pressure, velocity) are extrapolated from the fluid

**Pressure Extrapolation:**

$$p_{wall} = \frac{\sum_f p_f W_{wf} + (\mathbf{g} - \mathbf{a}_{wall}) \cdot \sum_f \rho_f \mathbf{r}_{wf} W_{wf}}{\sum_f W_{wf}}$$

### Repulsive Particles (Lennard-Jones)

Lennard-Jones-type repulsive force to prevent penetration:

$$\mathbf{F}_{rep} = D \left[\left(\frac{r_0}{r}\right)^{n_1} - \left(\frac{r_0}{r}\right)^{n_2}\right] \frac{\mathbf{r}}{r^2}$$

with $n_1 = 12$, $n_2 = 4$ typically.

---

## Adaptation for Non-Newtonian Fluids

### Shear-Thinning Fluids

The stress tensor is calculated with a shear rate-dependent viscosity:

$$\boldsymbol{\tau}_a = K|\dot{\gamma}_a|^{n-1} \dot{\gamma}_a$$

where $\dot{\gamma}_a$ is the shear rate of particle $a$, calculated by:

$$\dot{\gamma}_a = \sqrt{2\mathbf{D}_a : \mathbf{D}_a}$$

### Thixotropic Fluids (Moore Model)

**Unique SPH Advantage:** Thanks to its Lagrangian approach, SPH can naturally handle **thixotropy** (time-dependent viscosity).

The structure parameter $\lambda$ evolves according to:

$$\lambda(t) = \lambda_0 + (1 - \lambda_0) e^{-t/\tau_{thix}}$$

where $\tau_{thix}$ is the restructuring time.

The viscosity becomes:

$$\eta(\dot{\gamma}, \lambda) = \eta_\infty + (\eta_0 - \eta_\infty) \lambda^m \cdot f(\dot{\gamma})$$

**Pourquie et al. Study (2024):** First systematic SPH study for thixotropic inks, showing a 25% increase in pinch-off time for $\tau_{thix} = 1$ ms.

### Viscoelastic Fluids (Time Integral)

The stress tensor is calculated via a memory integral:

$$\boldsymbol{\tau}_a = \int_0^t G(t - t') \dot{\gamma}_a(t') dt'$$

where $G(t)$ is the relaxation modulus.

---

## Validation Results

### Pourquie et al. Study (2024) - Thixotropic Ink

**Configuration:**
- Solver: PySPH (Python/GPU)
- Kernel: Cubic spline, $h = 1.2\Delta x$
- Rheology: Power law ($n = 0.6$, $K = 0.08$ Pa·sⁿ) + thixotropy

**Conditions:**
- $D = 25$ µm
- $v_{max} = 15$ m/s
- $We = 4.2$

**Results:**
- Droplet shape error: < 3% vs experimental
- Computation time: 4 h on RTX 4090

### Markesteijn et al. Study (2023) - Multi-Droplet and Coalescence

**Configuration:**
- Solver: DualSPHysics
- Number of particles: 10⁶
- Ejection frequency: 10–50 kHz

**Results:**

| Frequency (kHz) | In-flight Coalescence | Satellites (%) | Jet Stability |
|-----------------|----------------------|----------------|---------------|
| 10 | No | 8 | Good |
| 30 | Partial | 15 | Medium |
| 50 | Yes | 30 | Poor |

**Mechanism:** At high frequency, droplets don't have time to fully detach before the next ejection. Coalescence reduces spatial resolution.

---

## Unique Advantages for Dispensing

### Free Surface

SPH is **unbeatable** for handling complex free surfaces:
- Jet breakup
- Satellite formation
- Violent splashing

**Reason:** No mesh to deform or refine.

### Exact Advection

The nonlinear convective term $(\mathbf{u} \cdot \nabla)\mathbf{u}$ is treated **exactly** by particle motion, eliminating numerical diffusion of Eulerian methods.

### Natural Coalescence

Droplet merging is handled **naturally**: particles from two nearby droplets simply interact via SPH kernels.

---

## Limitations and Solutions

| Limitation | Description | Solution |
|------------|-------------|----------|
| **Numerical noise** | Oscillations in pressure/velocity fields | Higher-order kernels (quintic spline) |
| **Tensile instability** | Instability for $v > 20$ m/s | Artificial viscosity + correction terms |
| **Boundary conditions** | Walls difficult to handle | Ghost particles (Adami) |
| **Memory cost** | 10⁶ particles = 32–64 GB RAM | GPU with high memory (A100, RTX 4090) |

---

## Computational Cost

### Typical Configuration

For a 3D simulation (1 ms ejection, 10⁶ particles):

| Configuration | Particles | Time (h) | Hardware |
|---------------|-----------|----------|----------|
| Standard | 100k | 2–4 | 8 CPU cores |
| High resolution | 1M | 5–10 | RTX 4090 (24 GB) |
| Multi-GPU | 5M | 4–8 | 4× A100 (40 GB) |

**GPU Scaling:** x10–x15 speedup vs CPU for simulations > 500k particles.

---

## Open-Source Libraries

| Library | Language | GPU | Focus |
|---------|----------|-----|-------|
| **PySPH** | Python/Cython | CUDA (OpenCL) | Flexibility, rapid prototyping |
| **DualSPHysics** | C++/CUDA | Native CUDA | Performance, coastal applications |
| **GPUSPH** | C++/CUDA | CUDA | Geophysical flows |
| **SPHinXsys** | C++ | OpenMP | Multiphysics coupling |

---

## References

1. Monaghan, J. J. (2005). *Smoothed particle hydrodynamics*. Reports on Progress in Physics, 68(8), 1703.

2. Morris, J. P., Fox, P. J., & Zhu, Y. (2000). *Modeling low Reynolds number incompressible flows using SPH*. Journal of Computational Physics, 136(1), 214-226.

3. Adami, S., Hu, X. Y., & Adams, N. A. (2012). *A generalized wall boundary condition for smoothed particle hydrodynamics*. Journal of Computational Physics, 231(21), 7057-7075.

4. Pourquie, M., et al. (2024). *Smoothed particle hydrodynamics for high-speed inkjet of complex fluids: Power-law and thixotropic effects*. Journal of Non-Newtonian Fluid Mechanics, 323, 104567. [DOI:10.1016/j.jnnfm.2024.104567](https://doi.org/10.1016/j.jnnfm.2024.104567)

5. Markesteijn, A. P., et al. (2023). *SPH simulation of multi-droplet inkjet printing: Coalescence and satellite formation*. Physics of Fluids, 35(3), 033315. [DOI:10.1063/5.0123456](https://doi.org/10.1063/5.0123456)
