**Contents:**
1. Overview of the 4 Models
2. Discretization Approaches
3. Critical Analysis by Model
4. Summary Table
5. Hardware Requirements
6. References

---

## 1. Overview of the 4 Models

This section presents the four numerical methods used to simulate shear-thinning ink dispensing into micro-wells.

| Model | Principle | Main characteristic |
|-------|-----------|---------------------|
| **FEM** | Finite element discretization with phase field $\phi$ for interface tracking | High local precision, native multiphysics coupling |
| **VOF** | Interface tracking via volume fraction $\alpha \in [0,1]$ on Eulerian mesh | Industry standard, rigorous mass conservation |
| **LBM** | Boltzmann equation resolution on regular grid | Optimal GPU parallelization, computational speed |
| **SPH** | Meshless Lagrangian particle method | Natural handling of large deformations |

---

## 2. Discretization Approaches: Eulerian vs Lagrangian

### 2.1 Method classification

Numerical methods for fluid simulation are divided into two families based on spatial treatment:

| Approach | Principle | Advantage | Methods |
|----------|-----------|-----------|---------|
| **Eulerian** | Fixed mesh, fluid flows through cells | Stability, direct implementation | FEM, VOF, LBM |
| **Lagrangian** | Mobile particles following the fluid | Natural deformation tracking | SPH |

The Eulerian approach observes the fluid from a fixed reference frame, while the Lagrangian approach follows fluid elements in their motion.

### 2.2 Visualization of the 4 Approaches

The figures below illustrate the discretization structures on a reference geometry (well: 800 µm × 130 µm):

#### FEM - Adaptive Triangular Mesh
- Triangular elements of variable size (1-10 µm)
- Local refinement at critical zones (interface, walls)

#### VOF - Hexahedral Mesh
- Uniform rectangular cells or with adaptive mesh refinement (AMR)
- Volume fraction $\alpha$ in each cell

#### LBM - Uniform Grid
- Regular Cartesian grid (resolution: 5 µm/cell)
- Macroscopic properties obtained via statistical moments

#### SPH - Particle Distribution
- Particle ensemble (~1000) with influence radius h
- Interpolation via kernels (cubic spline, Wendland)


