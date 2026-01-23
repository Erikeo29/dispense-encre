---

## 3. Critical Analysis by Model

### 3.1 FEM (Finite Element Method / Phase-Field)

**In brief:** The domain is divided into elements (triangles in 2D, tetrahedra in 3D) and Navier-Stokes equations are solved on each element. The ink/air interface is represented by a "phase field" $\phi$ that varies smoothly from -1 (air) to +1 (ink).

| ✅ Strengths | ⚠️ Limitations |
|-------------|----------------|
| Exceptional precision (down to 0.05 µm) | High computation time in 3D |
| Adaptive mesh (fine where needed) | Requires significant memory resources |
| Easy coupling of multiple physics | Sensitive to stabilization parameters |
| Software: COMSOL (commercial), FEniCS (open-source) | |

---

### 3.2 VOF (Volume of Fluid)

**In brief:** Each mesh cell contains a volume fraction $\alpha$ between 0 (100% air) and 1 (100% ink). The interface is geometrically reconstructed at each time step (PLIC method).

| ✅ Strengths | ⚠️ Limitations |
|-------------|----------------|
| Industry standard for 30 years | Interface sometimes numerically "diffuse" |
| Perfect mass conservation | High memory cost for very fine meshes |
| Very robust and well documented | Droplet coalescence difficult to handle |
| Software: OpenFOAM (open-source), Fluent (commercial) | |

---

### 3.3 LBM (Lattice Boltzmann Method)

**In brief:** Instead of directly solving Navier-Stokes, we simulate "particle packets" that move and collide on a regular grid. Macroscopic properties (velocity, pressure) emerge statistically.

| ✅ Strengths | ⚠️ Limitations |
|-------------|----------------|
| Exceptional GPU parallelization (×20) | Artificial compressibility (limit Ma < 0.1) |
| Simple grid, no complex meshing | Sub-micron precision difficult |
| Local algorithm (each cell independent) | Delicate rheological calibration |
| Software: Palabos (open-source), waLBerla | Less documentation than VOF |

---

### 3.4 SPH (Smoothed Particle Hydrodynamics)

**In brief:** The fluid is represented by particles that move freely. Each particle "feels" its neighbors via an interpolation kernel (like an influence field around it).

| ✅ Strengths | ⚠️ Limitations |
|-------------|----------------|
| No mesh → no deformation issues | Numerical noise in pressure fields |
| Natural coalescence and fragmentation | Instabilities at high velocity |
| Suited for large deformations | Less mature than Eulerian methods |
| Software: PySPH (Python), DualSPHysics | High memory cost in 3D |

---

## 4. Summary Table

This table summarizes key characteristics to help you choose the right method for your case:

| Criterion | FEM | VOF | LBM | SPH |
|-----------|-----|-----|-----|-----|
| **Interface precision** | 0.05–0.5 µm | 0.1–1 µm | 0.2–2 µm | 0.5–5 µm |
| **Typical computation time** | 10–50 h | 2–10 h | 1–5 h | 5–20 h |
| **Mass conservation** | Good (adjustment) | Perfect | Approximate | By summation |
| **Carreau rheology** | ✓ Native | ✓ Native | ✓ Possible | ✓ Possible |
| **GPU acceleration** | Limited | Good | Excellent (×20) | Good |
| **Learning curve** | Medium (GUI with COMSOL) | Steep (C++, CLI) | Steep (specific physics) | Medium (Python) |
| **Industrial maturity** | High | Very high | Medium | Developing |
| **Software cost** | COMSOL ~€10k/year or FEniCS free | OpenFOAM free | Palabos free | PySPH free |

### Which method to choose?

| Your situation | Recommended method | Why |
|----------------|-------------------|-----|
| Industrial production, need robustness | **VOF** (OpenFOAM) | Proven standard, large community |
| Multiphysics coupling (thermal, electrical...) | **FEM** (COMSOL or FEniCS) | Designed for coupling |
| Intensive computing, many simulations | **LBM** (Palabos) | Fastest on GPU |
| Academic research, new physics | **SPH** (PySPH) | Flexible, easy to modify |

---

## 5. Hardware Requirements

### 5.1 Understanding the needs

To simulate 1 millisecond of dispensing with about 1 million cells/particles, here's what to expect:

| Model | Processor (CPU) | Graphics card (GPU) | RAM | Estimated time |
|-------|-----------------|---------------------|-----|----------------|
| **FEM** | Powerful (64-128 cores) | Not very useful | High (64-128 GB) | 10-50 hours |
| **VOF** | Medium (16-32 cores) | Useful for speedup | Medium (16-32 GB) | 2-10 hours |
| **LBM** | Modest (4-8 cores) | Essential (high-end) | Modest (8-16 GB) | 1-5 hours |
| **SPH** | Medium (8-16 cores) | Very useful | High (32-64 GB) | 5-20 hours |

### 5.2 Budget translation

| Range | Configuration examples | Approximate budget | Suited for |
|-------|------------------------|-------------------|------------|
| **Entry level** | Desktop PC with mid-range GPU (e.g., GTX 1660, 8 GB VRAM) | €1,000 – 2,000 | Simple LBM/SPH, coarse VOF mesh |
| **Mid-range** | Workstation with gaming GPU (e.g., RTX 3080/4070, 12-16 GB VRAM) | €3,000 – 6,000 | Standard VOF, LBM, SPH |
| **High-end** | Multi-core server or professional GPU (e.g., RTX 4090, A100) | €10,000 – 30,000 | 3D FEM, parametric studies |
| **Cloud** | Hourly rental (AWS, Google Cloud, Azure) | €1-10/hour | Intensive one-off calculations |

### 5.3 Practical advice

- **LBM** makes the best use of GPUs: with a €500 graphics card, you can achieve performance equivalent to a €5,000 CPU server
- **FEM** remains CPU and RAM hungry: prefer a shared computing server or cloud
- **VOF** and **SPH** are good compromises: they run well on a modern desktop PC

---

## 6. References

> **Note**: For the complete list of scientific references, see the **Bibliography** section in the Appendices menu.
