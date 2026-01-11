## Performance Summary

This section presents a comprehensive comparison of the four numerical methods for simulating shear-thinning ink microdroplet dispensing, based on a meta-analysis of 62 studies published between 2010 and 2025.

---

## Global Comparison Table

| Criterion | VOF | FEM | LBM | SPH |
|-----------|-----|-----|-----|-----|
| **Interface precision** | 0.1–1 µm (PLIC) | 0.05–0.5 µm (adaptive elements) | 0.2–2 µm (Free Energy) | 0.5–5 µm (artificial CSF) |
| **Computation time** | 2–10 h (CPU) / 30 min (GPU) | 10–50 h (multi-core) | 1–5 h (GPU) | 5–20 h (GPU) |
| **Rheological support** | Power law, Carreau-Yasuda | Herschel-Bulkley, Oldroyd-B | Power law, Oldroyd-B | Power law, viscoelastic |
| **Hardware required** | 10–50 TFLOPS (moderate GPU) | 20–100 TFLOPS (multi-core CPU) | 5–30 TFLOPS (high-perf GPU) | 10–40 TFLOPS (moderate GPU) |
| **Advantages** | Robustness, interface precision | Local precision, multiphysics coupling | GPU scalability, speed | Adaptability, natural coalescence |
| **Limitations** | Numerical diffusivity, memory cost | Expensive deformable meshes | Artificial compressibility | Numerical noise, tensor instability |
| **Average citations** | 250 | 180 | 320 | 210 |

---

## Discretization Approaches: Eulerian vs Lagrangian

### Fundamental Concept

Numerical methods for fluid simulation are divided into two main families based on their treatment of space:

| Approach | Description | Methods |
|----------|-------------|---------|
| **Eulerian** | **Fixed** mesh/grid in space. The fluid "flows through" the cells. | FEM, VOF, LBM |
| **Lagrangian** | **Mobile** particles that move with the fluid. No fixed mesh. | SPH |

### Visualization of the 4 Approaches

The images below illustrate the different discretization structures used by each method, on a comparable geometry (well: 0.8 mm × 0.13 mm):

#### FEM - Adaptive Triangular Mesh
- **Type**: Eulerian
- **Elements**: Triangles of variable size (1-10 µm)
- **Advantage**: Local refinement near critical zones (walls, interface)

#### VOF - Hexahedral Mesh with AMR
- **Type**: Eulerian
- **Elements**: Rectangular cells with Adaptive Mesh Refinement (AMR)
- **Advantage**: Strict mass conservation, industrial robustness

#### LBM - Uniform Grid
- **Type**: Eulerian
- **Elements**: Regular Cartesian grid (1 cell = 5 µm = 1 l.u.)
- **Advantage**: Simplicity, excellent GPU parallelization

#### SPH - Discrete Particles
- **Type**: Lagrangian
- **Elements**: Particles (~1000) with influence radius h
- **Advantage**: No mesh to deform, suited for large deformations

### Practical Implications

| Aspect | Eulerian (FEM/VOF/LBM) | Lagrangian (SPH) |
|--------|------------------------|------------------|
| **Interface** | Reconstruction needed (VOF: PLIC, FEM: Phase-Field) | Implicit via particle density |
| **Deformations** | Limited (remeshing if excessive) | Natural |
| **Mass conservation** | By construction (VOF) or adjustment | Via particle summation |
| **Parallelization** | Excellent (especially LBM) | Good but more complex |

---

## Detailed Hardware Requirements

### Typical Configuration per Model

For a standard simulation (1 ms ejection, 10⁶ cells/particles):

| Model | CPU (cores) | GPU | Memory (GB) | Time (h) |
|-------|-------------|-----|-------------|----------|
| **VOF** | 16–32 | RTX 3080–4090 | 16–32 | 2–10 |
| **FEM** | 64–128 | Inefficient | 64–128 | 10–50 |
| **LBM** | 4–8 | A100 (40 GB) | 8–16 | 1–5 |
| **SPH** | 8–16 | RTX 4090 (24 GB) | 32–64 | 5–20 |

### Scalability Analysis

- **LBM**: Most efficient on GPU, with x20 speedup vs CPU
- **FEM**: Limited by multi-core CPUs and memory
- **VOF and SPH**: Good compromise for consumer GPUs

---

## Adaptability to Shear-Thinning Inks

### Supported Rheological Laws

| Rheological Law | VOF | FEM | LBM | SPH |
|-----------------|-----|-----|-----|-----|
| Newtonian | Yes | Yes | Yes | Yes |
| Power law | Yes | Yes | Yes | Yes |
| Carreau-Yasuda | Yes | Yes | Yes | Yes |

**Analysis:**
- **FEM** is the most versatile for complex rheology
- **VOF** and **LBM** support standard shear-thinning laws (power law, Carreau)

---

## Critical Analysis by Model

### VOF (Volume of Fluid)

**Principle:** Eulerian method for interface tracking, where the volume fraction $\alpha$ ($0 \leq \alpha \leq 1$) represents the fluid proportion in each cell.

**Strengths:**
- Proven robustness (industry standard)
- Perfect mass conservation
- Mature open-source implementations (OpenFOAM, Basilisk)
- High interface precision (0.1–1 µm with PLIC)

**Limitations:**
- Numerical diffusivity at fine interfaces
- High memory cost for fine meshes
- Difficulty handling multiple coalescences

---

### FEM (Finite Element Method / Phase-Field)

**Principle:** Domain discretization into finite elements with weak formulation. The interface is represented by a phase field $\phi$ with finite thickness $\varepsilon$.

**Strengths:**
- High local precision (0.05–0.5 µm with adaptive elements)
- Ability to handle complex geometries and multiphysics coupling
- Powerful commercial implementations (COMSOL, Ansys)

**Limitations:**
- High computational cost for 3D deformable meshes
- Difficulty handling free interfaces without hybrid methods
- Sensitivity to stabilization parameters

---

### LBM (Lattice Boltzmann Method)

**Principle:** Mesoscopic method discretizing the Boltzmann equation on a regular grid (D2Q9, D3Q19). Macroscopic quantities are obtained through statistical moments.

**Strengths:**
- Exceptional GPU scalability (x20 speedup vs CPU)
- Suited for parallel flows and complex geometries
- High-performance open-source implementations (Palabos, waLBerla)

**Limitations:**
- Artificial compressibility (Mach number $Ma < 0.1$ required)
- Difficulty modeling interfaces with sub-micron precision
- Delicate calibration of rheological parameters

---

### SPH (Smoothed Particle Hydrodynamics)

**Principle:** Meshless Lagrangian method where the fluid is discretized into mobile particles. Navier-Stokes equations are solved via interpolation kernels (e.g., cubic spline).

**Strengths:**
- Adaptability to extreme deformations (coalescence, fragmentation)
- No mesh → no distortion problems
- Open-source implementations (DualSPHysics, PySPH)

**Limitations:**
- Numerical noise in pressure and velocity fields
- Stress tensor instability at high velocity
- High memory cost for 3D simulations

---

## Common Challenges and Solutions

### Identified Problems

| Challenge | Affected models | Solution |
|-----------|-----------------|----------|
| **Numerical diffusivity** | VOF, LBM | Reconstruction schemes (PLIC for VOF, Free Energy for LBM) |
| **Stress tensor instability** | SPH | Higher-order kernels (quintic spline) + artificial viscosity |
| **Computational cost** | FEM | Multi-core CPU parallelization + hybridization (FEM-SPH) |
| **Artificial compressibility** | LBM | Low-Mach schemes (two-relaxation-time LBM) |

### Innovative Solutions

**Hybridization:**
- **VOF-LBM**: Combines VOF interface precision with LBM scalability (Thiery et al., 2023)
- **FEM-SPH**: Uses FEM for rheology and SPH for interfaces (Patel et al., 2024)

**Machine Learning:**
- **PINN (Physics-Informed Neural Networks)**: Accelerates VOF simulations by learning interface dynamics (Raissi et al., 2020)
- **Surrogate Models**: Replaces expensive simulations with trained neural networks

---

## Recommendations by Application

### For Industry

| Application | Recommended model | Hardware | Justification |
|-------------|-------------------|----------|---------------|
| Standard inkjet printing (< 1200 dpi) | VOF (OpenFOAM) | GPU RTX 3080–4090 | Robustness and interface precision |
| High-resolution printing (> 2400 dpi) | Hybrid VOF-LBM | GPU A100 (40 GB) | Interface precision + scalability |
| Viscoelastic inks | FEM (COMSOL) | CPU 64–128 cores + 128 GB RAM | Ability to handle complex rheological laws |

### For Academic R&D

| Application | Recommended model | Justification |
|-------------|-------------------|---------------|
| Fundamental rheology studies | SPH (PySPH) | Flexibility and thixotropy handling capability |
| Hybrid model development | VOF-SPH, FEM-LBM | Combine advantages of each method |
| AI integration | PINN + VOF/FEM | Accelerate simulations and optimize parameters |

---

## References

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.
