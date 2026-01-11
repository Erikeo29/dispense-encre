<div style="font-size: 0.9em; line-height: 1.3; background: #f8f9fa; padding: 8px 12px; border-radius: 4px; margin-bottom: 1em;">

**Contents:** 1. Mesoscopic Principle • 2. Discrete Boltzmann Equation • 3. Discretization Grids • 4. Relationship with Viscosity • 5. Multiphase Models • 6. Wetting Management • 7. GPU Scalability • 8. Open-Source Libraries • 9. Validation Results • 10. Limitations and Solutions • 11. Computational Cost • 12. References
</div>

## 1. Mesoscopic Principle

The **LBM (Lattice Boltzmann Method)** is a mesoscopic approach that does not directly solve the Navier-Stokes equations, but rather the **discretized Boltzmann equation** on a regular lattice.

### 1.1 Fundamental Concept

We track the evolution of **distribution functions** $f_i(\mathbf{x}, t)$ representing the probability of finding particles at position $\mathbf{x}$ at time $t$, moving in discrete directions $\mathbf{c}_i$.

Macroscopic quantities (density $\rho$, velocity $\mathbf{u}$) are obtained through **statistical moments**:

$$\rho = \sum_i f_i \quad \text{and} \quad \rho \mathbf{u} = \sum_i f_i \mathbf{c}_i$$

---

## 2. Discrete Boltzmann Equation

### 2.1 BGK Formulation

The fundamental equation is:

$$f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = \Omega_i(f) + F_i$$

where:
- $\Omega_i(f)$: collision operator (relaxation toward equilibrium)
- $F_i$: external force term

### 2.2 BGK Collision Operator

The BGK (Bhatnagar-Gross-Krook) approximation simplifies collision as linear relaxation toward equilibrium:

$$\Omega_i = -\frac{1}{\tau}(f_i - f_i^{eq})$$

where $\tau$ is the **relaxation time** and $f_i^{eq}$ the discretized Maxwell-Boltzmann equilibrium distribution:

$$f_i^{eq} = w_i \rho \left[1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2c_s^4} - \frac{\mathbf{u}^2}{2c_s^2}\right]$$

with $c_s = 1/\sqrt{3}$ the lattice speed of sound and $w_i$ the quadrature weights.

---

## 3. Discretization Grids

### 3.1 DdQq Nomenclature

The **DdQq** notation indicates:
- **d**: number of spatial dimensions
- **q**: number of discrete velocities

### 3.2 Common Grids

| Grid | Application | Velocities |
|------|-------------|------------|
| **D2Q9** | 2D standard | 9 directions (rest + 4 axes + 4 diagonals) |
| **D3Q15** | 3D economical | 15 directions |
| **D3Q19** | 3D standard | 19 directions (good precision/cost compromise) |
| **D3Q27** | 3D high precision | 27 directions (full cube) |

**Typical Choice for Inkjet:** D3Q19 with $\Delta x = 0.3$ µm

---

## 4. Relationship with Viscosity

### 4.1 Fundamental Relation

Kinematic viscosity $\nu$ is related to relaxation time $\tau$ by:

$$\nu = c_s^2 \left(\tau - \frac{1}{2}\right) \Delta t$$

This relation is **fundamental**: it allows modeling fluids of different viscosities by simply adjusting $\tau$.

### 4.2 Adaptation for Non-Newtonian Fluids

For shear-thinning fluids, $\tau$ depends locally on shear rate $\dot{\gamma}$:

$$\tau(\dot{\gamma}) = \frac{1}{2} + \frac{\nu(\dot{\gamma})}{c_s^2 \Delta t}$$

where $\nu(\dot{\gamma})$ is given by a rheological law (e.g., power law, Carreau).

---

## 5. Multiphase Models

### 5.1 Shan-Chen (Pseudopotential)

The **Shan-Chen** model represents fluid interactions via an **interparticle force**:

$$\mathbf{F}_{int}(\mathbf{x}) = -G\psi(\mathbf{x}) \sum_i w_i \psi(\mathbf{x} + \mathbf{c}_i \Delta t) \mathbf{c}_i$$

where:
- $G$: interaction parameter (controls surface tension)
- $\psi(\mathbf{x})$: pseudopotential function depending on local density

**Phase Separation:** This force causes spontaneous phase separation (like oil/water) without explicit interface tracking.

**Surface Tension:** $\sigma \propto G(\psi_{max} - \psi_{min})^2$

### 5.2 Free Energy Model

The **Free Energy** model is based on a free energy functional:

$$\mathcal{F} = \int_V \left[\psi(\rho) + \frac{\kappa}{2}|\nabla\rho|^2\right] dV$$

The interface force is derived from the energy gradient:

$$\mathbf{F} = -\nabla \cdot \boldsymbol{\sigma}^{chem}$$

**Advantages vs Shan-Chen:**
- Better stability for large density ratios
- More precise surface tension control
- Fewer spurious currents

### 5.3 Color Gradient Model

Uses two fluid populations (red/blue) with a segregation force:

$$\mathbf{F}_{seg} = A|\nabla \rho^N| \mathbf{n}$$

where $\rho^N = (\rho^R - \rho^B)/(\rho^R + \rho^B)$ is the normalized color fraction.

---

## 6. Wetting Management

### 6.1 Contact Angles

Contact angles on solid walls are managed by assigning a **fictitious density** (or potential) to solid nodes:

$$\rho_{solid} = \rho_0 + \Delta \rho \cdot \cos(\theta_{eq})$$

where $\theta_{eq}$ is the desired equilibrium contact angle.

**Major Advantage:** Wetting is handled **naturally** without complex explicit boundary conditions, which is ideal for complex geometries (micro-wells, roughness).

---

## 7. GPU Scalability

### 7.1 Exceptional Performance

LBM is **intrinsically parallel**: each node can be updated independently during collision and streaming steps.

**Typical Speedup:** x20 on GPU vs CPU (measured on NVIDIA A100)

### 7.2 Li et al. Benchmark (2022)

| Configuration | Computation Time |
|---------------|------------------|
| CPU (20 h) | Reference |
| GPU A100 (1 GPU) | 2 h |
| GPU A100 (4 GPUs) | 35 min |
| GPU A100 (16 GPUs) | 10 min |

**Near-linear scalability** up to 16 GPUs.

---

## 8. Open-Source Libraries

### 8.1 Palabos

**Palabos** (Parallel Lattice Boltzmann Solver) is the open-source reference:

- **Language:** Object-oriented C++
- **Parallelization:** Native MPI, excellent cluster scaling
- **Models:** Shan-Chen, Free Energy, Color Gradient
- **Documentation:** Excellent with tutorials

### 8.2 Alternatives

| Library | Focus | GPU |
|---------|-------|-----|
| **OpenLB** | Engineering, industrial applications | OpenMP/CUDA |
| **waLBerla** | Extreme HPC, millions of cores | Native CUDA |
| **Sailfish** | GPU native, Python interface | CUDA priority |
| **Musubi** | Multiphysics coupling | MPI |

---

## 9. Validation Results

### 9.1 Li et al. Study (2022) - Shear-Thinning Ink

**Configuration:**
- Solver: Palabos (C++/CUDA)
- Grid: D3Q19, $\Delta x = 0.3$ µm
- Interface: Free Energy (Shan-Chen)
- Rheology: MRT with $\tau(\dot{\gamma})$, $n = 0.72$

**Conditions:**
- $Re = 40$, $We = 3.5$
- $T = 298$ K
- Hardware: NVIDIA A100 GPU

**Results:**
- Maximum droplet velocity: 15.2 m/s (experimental: 15.0 m/s)
- Droplet diameter: 28 µm (error < 2%)
- Computation time: 2 h (vs 20 h on CPU)

**Mechanism:** Shear-thinning reduces viscosity in the filament, accelerating pinch-off. The Free Energy model correctly captures surface tension ($\sigma = 35$ mN/m).

### 9.2 VOF-LBM Hybridization (Thiery et al., 2023)

**Objective:** Combine VOF interface precision with LBM scalability.

**Methodology:**
- VOF (PLIC) for interface tracking
- LBM (D2Q9) for Navier-Stokes resolution
- Coupling: transfer of $\alpha$ and $\mathbf{v}$ between the two methods

**Results:**

| Model | Precision (µm) | Time (h) | GPU Scalability |
|-------|----------------|----------|-----------------|
| VOF only | 0.5 | 10 | Medium |
| LBM only | 1.2 | 2 | Excellent |
| Hybrid VOF-LBM | 0.3 | 3 | Good |

---

## 10. Limitations and Solutions

### 10.1 Artificial Compressibility

**Problem:** LBM simulates a weakly compressible fluid. To maintain the incompressible approximation:

$$Ma = \frac{u}{c_s} < 0.1$$

**Solution:** Use low-Mach schemes (two-relaxation-time LBM, entropic LBM).

### 10.2 Spurious Currents

**Problem:** Artificial convection currents appear at interfaces (Shan-Chen).

**Solutions:**
- Free Energy model (reduces spurious currents by 90%)
- Improved isotropy of gradient operators
- Higher-order discretization schemes

### 10.3 Rheological Calibration

**Problem:** The $\nu(\tau)$ relation is linear, limiting the range of simulable viscosities.

**Solution:** Multiple relaxation time matrices (MRT) with separate relaxation times for odd and even moments.

---

## 11. Computational Cost

### 11.1 Typical Configuration

For a 3D simulation (1 ms ejection, D3Q19):

| Configuration | Grid | Time (h) | Hardware |
|---------------|------|----------|----------|
| Standard | 100³ nodes | 4–8 | 4 CPU cores |
| High resolution | 300³ nodes | 1–2 | A100 GPU |
| Multi-GPU | 500³ nodes | 0.5–1 | 4× A100 |

**GPU Memory:** ~16 GB for 300³ nodes in D3Q19 (19 distributions × 8 bytes × 27M nodes)

---

## 12. References

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.
