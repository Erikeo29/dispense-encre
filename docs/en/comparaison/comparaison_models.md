**Contents:**
1. Performance Summary
2. Global Comparison Table
3. Discretization Approaches
4. Adaptability to Shear-Thinning Inks
5. Critical Analysis by Model
6. Common Challenges and Solutions
7. Recommendations by Application
8. Detailed Hardware Requirements
9. References

---

## 1. Performance Summary

This section presents a comprehensive comparison of the four numerical methods for simulating shear-thinning ink microdroplet dispensing, based on a meta-analysis of 62 studies published between 2010 and 2025.

---

## 2. Global Comparison Table

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

## 3. Discretization Approaches: Eulerian vs Lagrangian

### 3.1 Fundamental Concept

Numerical methods for fluid simulation are divided into two main families based on their treatment of space:

| Approach | Description | Methods |
|----------|-------------|---------|
| **Eulerian** | **Fixed** mesh/grid in space. The fluid "flows through" the cells. | FEM, VOF, LBM |
| **Lagrangian** | **Mobile** particles that move with the fluid. No fixed mesh. | SPH |

### 3.2 Visualization of the 4 Approaches

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

### 3.3 Practical Implications

| Aspect | Eulerian (FEM/VOF/LBM) | Lagrangian (SPH) |
|--------|------------------------|------------------|
| **Interface** | Reconstruction needed (VOF: PLIC, FEM: Phase-Field) | Implicit via particle density |
| **Deformations** | Limited (remeshing if excessive) | Natural |
| **Mass conservation** | By construction (VOF) or adjustment | Via particle summation |
| **Parallelization** | Excellent (especially LBM) | Good but more complex |
