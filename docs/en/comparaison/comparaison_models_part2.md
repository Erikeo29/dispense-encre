---

## 3. Critical Analysis by Model

### 3.1 FEM (Finite Element Method / Phase-Field)

Finite element method with weak formulation of Navier-Stokes equations. The ink/air interface is represented by a phase field $\phi$ varying from -1 (air) to +1 (ink) over a characteristic thickness $\varepsilon$.

| Advantages | Limitations |
|------------|-------------|
| Interface precision: 0.05–0.5 µm | Longer computation time than VOF/LBM |
| Adaptive mesh following $\phi$ gradient | Significant memory consumption in 3D |
| Native multiphysics coupling | Sensitivity to stabilization parameters |
| Software: COMSOL (commercial), FEniCS (open-source) | |

---

### 3.2 VOF (Volume of Fluid)

Eulerian method where each cell contains a volume fraction $\alpha \in [0,1]$. The interface is geometrically reconstructed via the PLIC algorithm (Piecewise Linear Interface Construction).

| Advantages | Limitations |
|------------|-------------|
| Rigorous mass conservation | Numerical diffusion at fine interfaces |
| Industry standard for 30 years | Memory cost for fine meshes |
| Extensive documentation and community | Droplet coalescence difficult |
| Software: OpenFOAM (open-source), Fluent (commercial) | |

---

### 3.3 LBM (Lattice Boltzmann Method)

Mesoscopic method solving the discretized Boltzmann equation on a regular grid (D2Q9, D3Q19). Macroscopic quantities (velocity, pressure) are obtained through statistical moment computation.

| Advantages | Limitations |
|------------|-------------|
| Exceptional GPU parallelization (factor ×10-20) | Artificial compressibility (constraint Ma < 0.1) |
| Local algorithm (each node independent) | Sub-micron precision difficult |
| No complex mesh generation required | Delicate rheological calibration |
| Software: Palabos (open-source), waLBerla | Less extensive documentation than VOF |

---

### 3.4 SPH (Smoothed Particle Hydrodynamics)

Meshless Lagrangian method. The fluid is discretized into particles whose properties are interpolated via smoothing kernels (cubic spline, Wendland).

| Advantages | Limitations |
|------------|-------------|
| No mesh: no distortion issues | Numerical noise in pressure fields |
| Natural coalescence and fragmentation | Tensorial instabilities at high velocity |
| Suited for large deformations | Lower industrial maturity |
| Software: PySPH (Python), DualSPHysics | High memory cost in 3D |

---

## 4. Hardware Requirements

### 4.1 Orders of magnitude

Computation times depend on resolution and simulated duration. For a typical 2D dispensing simulation (20-40 ms physical time):

| Model | Processor | Graphics card | RAM | Time |
|-------|-----------|---------------|-----|------|
| **FEM** | 8-16 cores | Underutilized | 16-32 GB | 5-30 h |
| **VOF** | 8-16 cores | Useful acceleration | 8-16 GB | 2-10 h |
| **LBM** | 4-8 cores | Strongly recommended | 8-16 GB | 1-5 h |
| **SPH** | 8-16 cores | Recommended | 16-32 GB | 2-10 h |

### 4.2 Indicative configurations

| Range | Typical configuration | Indicative budget | Usage |
|-------|----------------------|-------------------|-------|
| **Standard PC** | 8-12 cores, 16-32 GB RAM | €800–1,500 | Simple VOF/LBM, 2D SPH |
| **Upgraded PC** | 12-16 cores, 32-64 GB RAM, GPU 8 GB | €1,500–3,000 | 2D FEM, parametric studies |
| **Server** | 32+ cores, 128+ GB RAM | €5,000–15,000 | 3D FEM/VOF, large series |
| **Cloud** | AWS, Google Cloud, Azure | €1-5/h | Intensive one-off calculations |

### 4.3 Practical remarks

- **LBM** efficiently exploits GPUs: a consumer graphics card significantly accelerates computations
- **FEM** and **VOF** run on standard PCs for 2D cases
- Cloud is useful for 3D studies or large parametric series

---

## 5. Summary Table

| Criterion | FEM | VOF | LBM | SPH |
|-----------|-----|-----|-----|-----|
| **Interface precision** | 0.05–0.5 µm | 0.1–1 µm | 0.2–2 µm | 0.5–5 µm |
| **2D computation time** | 5–30 h | 2–10 h | 1–5 h | 2–10 h |
| **Mass conservation** | Numerical adjustment | Rigorous | Approximate | By summation |
| **Carreau rheology** | Native | Native | Implementable | Implementable |
| **GPU acceleration** | Limited | Good | Excellent (×10-20) | Good (×10-15) |
| **Learning curve** | Medium (GUI available) | Steep (C++, CLI) | Steep (specific physics) | Medium (Python) |
| **Industrial maturity** | High | Very high | Medium | Developing |
| **Software cost** | COMSOL ~€10k/year, FEniCS free | OpenFOAM free | Palabos free | PySPH free |

### Recommendations by application context

| Context | Recommended method | Justification |
|---------|-------------------|---------------|
| Industrial production | VOF (OpenFOAM) | Proven robustness, large community |
| Multiphysics coupling | FEM (COMSOL, FEniCS) | Native coupling architecture |
| Intensive parametric studies | LBM (Palabos) | Optimal GPU performance |
| Fundamental research | SPH (PySPH) | Flexibility for new physics |

---

## 6. References

> For the complete list of scientific references, see the **Bibliography** section in the Appendices menu.
