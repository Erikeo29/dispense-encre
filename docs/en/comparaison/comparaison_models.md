**Contents:**
1. Overview of the 3 Models
2. Discretization Approaches
3. Critical Analysis by Model
4. Hardware Requirements
5. Summary Table
6. Bibliographical References

---

## 1. Overview of the 3 Models

This section presents the three numerical methods used to simulate shear-thinning ink dispensing into micro-wells.

| Model | Principle | Main characteristic |
|-------|-----------|---------------------|
| **VOF** | Interface tracking via volume fraction $\alpha \in [0,1]$ on Eulerian mesh | Industry standard, rigorous mass conservation |
| **LBM** | Boltzmann equation resolution on regular grid | Optimal GPU parallelization, computational speed |
| **SPH** | Meshless Lagrangian particle method | Natural handling of large deformations |

---

## 2. Discretization Approaches: Eulerian vs Lagrangian

### 2.1 Method classification

Numerical methods for fluid simulation are divided into two families based on spatial treatment:

| Approach | Principle | Advantage | Methods |
|----------|-----------|-----------|---------|
| **Eulerian** | Fixed mesh, fluid flows through cells | Stability, direct implementation | VOF, LBM |
| **Lagrangian** | Mobile particles following the fluid | Natural deformation tracking | SPH |

The Eulerian approach observes the fluid from a fixed reference frame, while the Lagrangian approach follows fluid elements in their motion.

### 2.2 Visualization of the 3 Approaches

The figures below illustrate the discretization structures used **in this study** on the reference geometry (well: 800 µm × 130 µm):

#### VOF - Hexahedral Mesh
- Rectangular cells (resolution ~5 µm in this study)
- Volume fraction $\alpha$ in each cell

#### LBM - Uniform Grid
- Regular Cartesian grid (5 µm/cell in this study)
- Macroscopic properties obtained via statistical moments

#### SPH - Particle Distribution
- Approximately 1000 particles in this study (value depends on desired resolution)
- Interpolation via kernels (cubic spline, Wendland)


