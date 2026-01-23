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

## 4. Summary Table

| Criterion | FEM | VOF | LBM | SPH |
|-----------|-----|-----|-----|-----|
| **Interface precision** | 0.05–0.5 µm | 0.1–1 µm | 0.2–2 µm | 0.5–5 µm |
| **Computation time (order of magnitude)** | 10–50 h | 2–10 h | 1–5 h | 2–20 h |
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

## 5. Hardware Requirements

### 5.1 Orders of magnitude

Computation times strongly depend on resolution and simulated duration. For a typical 2D dispensing simulation (20-40 ms physical time):

| Model | Processor | Graphics card | RAM | Time (order of magnitude) |
|-------|-----------|---------------|-----|---------------------------|
| **FEM** | 8-32 cores | Underutilized | 16-64 GB | Several hours to tens of hours |
| **VOF** | 8-16 cores | Useful acceleration | 8-32 GB | Several hours |
| **LBM** | 4-8 cores | Strongly recommended | 8-16 GB | 1-5 hours |
| **SPH** | 8-16 cores | Recommended | 16-64 GB | Several hours |

### 5.2 Indicative configurations

| Range | Typical configuration | Indicative budget | Usage |
|-------|----------------------|-------------------|-------|
| **Workstation** | 12-32 cores, 32-64 GB RAM, GPU 8-16 GB VRAM | €3,000–8,000 | All methods in 2D, parametric studies |
| **Compute server** | 64+ cores, 128+ GB RAM | €10,000–30,000 | FEM/VOF 3D, large series |
| **Cloud** | AWS, Google Cloud, Azure | €1-10/h | Intensive one-off calculations |

### 5.3 Practical remarks

- **LBM** efficiently exploits GPUs: a consumer graphics card can offer performance comparable to a multi-core server
- **FEM** and **VOF** can be run on workstations for 2D cases; cloud is useful for 3D studies or large parametric series
- **SPH** runs well on workstations with GPU

---

## 6. References

> For the complete list of scientific references, see the **Bibliography** section in the Appendices menu.
