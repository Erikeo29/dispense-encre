---

## 3. Critical Analysis by Model

### 3.1 FEM (Finite Element Method / Phase-Field)

Finite element method with weak formulation of Navier-Stokes equations. The ink/air interface is represented by a phase field $\phi$ varying from -1 (air) to +1 (ink) over a characteristic thickness $\varepsilon$.

| Advantages | Limitations |
|------------|-------------|
| Interface precision: 0.05–0.5 µm | High computation time in 3D |
| Adaptive mesh following $\phi$ gradient | Significant memory consumption |
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
| Exceptional GPU parallelization (factor ×20) | Artificial compressibility (constraint Ma < 0.1) |
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
| **Typical computation time** | 10–50 h | 2–10 h | 1–5 h | 5–20 h |
| **Mass conservation** | Numerical adjustment | Rigorous | Approximate | By summation |
| **Carreau rheology** | Native | Native | Implementable | Implementable |
| **GPU acceleration** | Limited | Good | Excellent (×20) | Good |
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

### 5.1 Resources by model

For a reference simulation (1 ms dispensing, ~10⁶ cells/particles):

| Model | Processor | Graphics card | RAM | Estimated time |
|-------|-----------|---------------|-----|----------------|
| **FEM** | 64-128 cores | Underutilized | 64-128 GB | 10-50 h |
| **VOF** | 16-32 cores | Acceleration possible | 16-32 GB | 2-10 h |
| **LBM** | 4-8 cores | Essential (high-end) | 8-16 GB | 1-5 h |
| **SPH** | 8-16 cores | Recommended | 32-64 GB | 5-20 h |

### 5.2 Typical configurations

| Range | Configuration | Indicative budget | Usage |
|-------|---------------|-------------------|-------|
| **Entry** | Desktop PC, GPU 8 GB VRAM (e.g., GTX 1660) | €1,000–2,000 | Simple LBM/SPH, coarse VOF mesh |
| **Intermediate** | Workstation, GPU 12-16 GB VRAM (e.g., RTX 3080) | €3,000–6,000 | Standard VOF, LBM, SPH |
| **High performance** | Multi-core server or GPU 24+ GB (e.g., RTX 4090, A100) | €10,000–30,000 | 3D FEM, parametric studies |
| **Cloud** | AWS, Google Cloud, Azure | €1-10/h | Intensive one-off calculations |

### 5.3 Practical considerations

- **LBM** optimally exploits GPU architectures: a €500 graphics card can match a €5,000 CPU server
- **FEM** primarily requires CPU and memory resources: cloud computing or compute clusters are often preferable
- **VOF** and **SPH** offer a good compromise and run efficiently on modern workstations

---

## 6. References

> For the complete list of scientific references, see the **Bibliography** section in the Appendices menu.
