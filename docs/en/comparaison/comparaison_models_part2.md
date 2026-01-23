---

## 3. Critical Analysis by Model

### 3.1 VOF (Volume of Fluid)

**Principle:** Volume fraction $\alpha$ ($0 \leq \alpha \leq 1$) represents the fluid proportion in each cell.

| Strengths | Limitations |
|-----------|-------------|
| Proven robustness (industry standard) | Numerical diffusivity at fine interfaces |
| Perfect mass conservation | High memory cost for fine meshes |
| Mature open-source implementations (OpenFOAM, Basilisk) | Multiple coalescences difficult |
| Interface precision 0.1–1 µm with PLIC | |

---

### 3.2 FEM / Phase-Field

**Principle:** Finite elements with weak formulation. Interface represented by phase field $\phi$ with thickness $\varepsilon$.

| Strengths | Limitations |
|-----------|-------------|
| Local precision 0.05–0.5 µm | High computational cost in 3D |
| Complex geometries and multiphysics coupling | Free interfaces difficult without hybridization |
| Commercial implementations (COMSOL, Ansys) | Sensitivity to stabilization parameters |

---

### 3.3 LBM (Lattice Boltzmann)

**Principle:** Discretized Boltzmann equation on regular grid (D2Q9, D3Q19). Macroscopic quantities via statistical moments.

| Strengths | Limitations |
|-----------|-------------|
| Exceptional GPU scalability (x20 vs CPU) | Artificial compressibility ($Ma < 0.1$) |
| Massive parallelization | Sub-micron precision difficult |
| Open-source implementations (Palabos, waLBerla) | Delicate rheological calibration |

---

### 3.4 SPH (Smoothed Particle Hydrodynamics)

**Principle:** Meshless method with mobile particles. Navier-Stokes solved via interpolation kernels (cubic spline).

| Strengths | Limitations |
|-----------|-------------|
| Extreme deformations (coalescence, fragmentation) | Numerical noise (pressure, velocity) |
| No mesh → no distortion | Stress tensor instability at high velocity |
| Open-source (DualSPHysics, PySPH) | High memory cost in 3D |

---

## 4. Summary Table

| Criterion | VOF | FEM | LBM | SPH |
|-----------|-----|-----|-----|-----|
| **Interface precision** | 0.1–1 µm | 0.05–0.5 µm | 0.2–2 µm | 0.5–5 µm |
| **Computation time** | 2–10 h | 10–50 h | 1–5 h | 5–20 h |
| **Mass conservation** | Perfect | Adjustment | Approximate | Summation |
| **Carreau rheology** | ✓ | ✓ | ✓ | ✓ |
| **GPU parallelization** | Good | Limited | Excellent | Good |
| **Ease of use** | High | Medium | Medium | Medium |
| **Industrial maturity** | Very high | High | Medium | Low |

**Recommendations:**
- **Standard inkjet** (< 1200 dpi) → **VOF** (robustness + precision)
- **High resolution** (> 2400 dpi) → **Hybrid VOF-LBM** (precision + speed)
- **Viscoelastic inks** → **FEM** (complex rheological laws)
- **Academic R&D** → **SPH** (flexibility, new physics)

---

## 5. Hardware Requirements

For a standard simulation (1 ms ejection, 10⁶ cells/particles):

| Model | CPU (cores) | GPU | Memory (GB) | Time (h) |
|-------|-------------|-----|-------------|----------|
| **VOF** | 16–32 | RTX 3080–4090 | 16–32 | 2–10 |
| **FEM** | 64–128 | Inefficient | 64–128 | 10–50 |
| **LBM** | 4–8 | A100 (40 GB) | 8–16 | 1–5 |
| **SPH** | 8–16 | RTX 4090 (24 GB) | 32–64 | 5–20 |

**Scalability:**
- **LBM**: most efficient on GPU (x20 vs CPU)
- **FEM**: limited by multi-core CPUs and memory
- **VOF / SPH**: good compromise for consumer GPUs

---

## 6. References

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.
