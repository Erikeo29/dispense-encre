---

## 4. Adaptability to Shear-Thinning Inks

### 4.1 Supported Rheological Laws

| Rheological Law | VOF | FEM | LBM | SPH |
|-----------------|-----|-----|-----|-----|
| Newtonian | Yes | Yes | Yes | Yes |
| Power law | Yes | Yes | Yes | Yes |
| Carreau-Yasuda | Yes | Yes | Yes | Yes |

**Analysis:**
- **FEM** is the most versatile for complex rheology
- **VOF** and **LBM** support standard shear-thinning laws (power law, Carreau)

---

## 5. Critical Analysis by Model

### 5.1 VOF (Volume of Fluid)

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

### 5.2 FEM (Finite Element Method / Phase-Field)

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

### 5.3 LBM (Lattice Boltzmann Method)

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

### 5.4 SPH (Smoothed Particle Hydrodynamics)

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

## 6. Common Challenges and Solutions

### 6.1 Identified Problems

| Challenge | Affected models | Solution |
|-----------|-----------------|----------|
| **Numerical diffusivity** | VOF, LBM | Reconstruction schemes (PLIC for VOF, Free Energy for LBM) |
| **Stress tensor instability** | SPH | Higher-order kernels (quintic spline) + artificial viscosity |
| **Computational cost** | FEM | Multi-core CPU parallelization + hybridization (FEM-SPH) |
| **Artificial compressibility** | LBM | Low-Mach schemes (two-relaxation-time LBM) |

### 6.2 Innovative Solutions

**Hybridization:**
- **VOF-LBM**: Combines VOF interface precision with LBM scalability (Thiery et al., 2023)
- **FEM-SPH**: Uses FEM for rheology and SPH for interfaces (Patel et al., 2024)

**Machine Learning:**
- **PINN (Physics-Informed Neural Networks)**: Accelerates VOF simulations by learning interface dynamics (Raissi et al., 2020)
- **Surrogate Models**: Replaces expensive simulations with trained neural networks

---

## 7. Recommendations by Application

### 7.1 For Industry

| Application | Recommended model | Hardware | Justification |
|-------------|-------------------|----------|---------------|
| Standard inkjet printing (< 1200 dpi) | VOF (OpenFOAM) | GPU RTX 3080–4090 | Robustness and interface precision |
| High-resolution printing (> 2400 dpi) | Hybrid VOF-LBM | GPU A100 (40 GB) | Interface precision + scalability |
| Viscoelastic inks | FEM (COMSOL) | CPU 64–128 cores + 128 GB RAM | Ability to handle complex rheological laws |

### 7.2 For Academic R&D

| Application | Recommended model | Justification |
|-------------|-------------------|---------------|
| Fundamental rheology studies | SPH (PySPH) | Flexibility and thixotropy handling capability |
| Hybrid model development | VOF-SPH, FEM-LBM | Combine advantages of each method |
| AI integration | PINN + VOF/FEM | Accelerate simulations and optimize parameters |

---

## 8. Detailed Hardware Requirements

### 8.1 Typical Configuration per Model

For a standard simulation (1 ms ejection, 10⁶ cells/particles):

| Model | CPU (cores) | GPU | Memory (GB) | Time (h) |
|-------|-------------|-----|-------------|----------|
| **VOF** | 16–32 | RTX 3080–4090 | 16–32 | 2–10 |
| **FEM** | 64–128 | Inefficient | 64–128 | 10–50 |
| **LBM** | 4–8 | A100 (40 GB) | 8–16 | 1–5 |
| **SPH** | 8–16 | RTX 4090 (24 GB) | 32–64 | 5–20 |

### 8.2 Scalability Analysis

- **LBM**: Most efficient on GPU, with x20 speedup vs CPU
- **FEM**: Limited by multi-core CPUs and memory
- **VOF and SPH**: Good compromise for consumer GPUs

---

## 9. References

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.
