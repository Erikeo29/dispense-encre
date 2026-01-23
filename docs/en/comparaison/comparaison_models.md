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

| Model | Principle | Highlights |
|-------|-----------|------------|
| **FEM** | Finite elements with phase field $\phi$ for interface tracking | Exceptional local precision (0.05 µm), native multiphysics coupling |
| **VOF** | Volume fraction $\alpha \in [0,1]$ on fixed Eulerian mesh | Industry standard, perfect mass conservation, robust |
| **LBM** | Discretized Boltzmann equation on regular grid | x20 GPU scalability, massive parallelization, very fast |
| **SPH** | Meshless mobile particles with interpolation kernels | Natural large deformations, easy coalescence/fragmentation |

---

## 2. Discretization Approaches: Eulerian vs Lagrangian

### 2.1 Fundamental Concept

| Approach | Description | Methods |
|----------|-------------|---------|
| **Eulerian** | **Fixed** mesh in space. Fluid flows through cells. | FEM, VOF, LBM |
| **Lagrangian** | **Mobile** particles following the fluid. No fixed mesh. | SPH |

### 2.2 Visualization of the 4 Approaches

The images below illustrate the discretization structures on a comparable geometry (well 0.8 mm × 0.13 mm):

#### FEM - Adaptive Triangular Mesh
- Triangles of variable size (1-10 µm), refinement near walls and interface

#### VOF - Hexahedral Mesh
- Rectangular cells with adaptive mesh refinement (AMR)

#### LBM - Uniform Grid
- Regular Cartesian grid (1 cell = 5 µm = 1 l.u.)

#### SPH - Discrete Particles
- ~1000 particles with influence radius h
