**Contents:**
1. Overview of the 4 Models
2. Discretization Approaches
3. Critical Analysis by Model
4. Summary Table
5. Hardware Requirements
6. References

---

## 1. Overview of the 4 Models

This section presents the four numerical methods used to simulate shear-thinning ink dispensing into micro-wells. Each method has its strengths and weaknesses depending on the use case.

| Model | Principle in one sentence | What sets it apart |
|-------|---------------------------|-------------------|
| **FEM** | Divides the domain into small triangles/tetrahedra and solves equations on each element | Very precise locally, ideal for coupling multiple physics (thermal, electrical...) |
| **VOF** | Tracks ink/air interface via volume fraction $\alpha$ (0 = air, 1 = ink) | Industry reference, perfect mass conservation, very robust |
| **LBM** | Simulates fluid as "particle packets" on a regular grid | Extremely fast on GPU, natural parallelization |
| **SPH** | Represents fluid by freely moving particles | Naturally handles large deformations and fragmentation |

---

## 2. Discretization Approaches: Eulerian vs Lagrangian

### 2.1 Two main families

In numerical simulation, we distinguish two fundamental philosophies:

| Approach | How does it work? | Main advantage | Methods |
|----------|-------------------|----------------|---------|
| **Eulerian** | Mesh remains **fixed**, fluid "flows through" cells | Simple to implement, stable | FEM, VOF, LBM |
| **Lagrangian** | Particles **move with** the fluid, no fixed mesh | Naturally follows deformations | SPH |

**Analogy:** Imagine observing a river. The Eulerian approach is like placing fixed sensors on the banks. The Lagrangian approach is like following corks floating on the water.

### 2.2 Visualization of the 4 Approaches

The images below show how each method "sees" the same geometry (well: 800 µm × 130 µm):

#### FEM - Adaptive Triangular Mesh
- Small triangles where important (interface, walls), larger triangles elsewhere
- Element size: 1 to 10 µm depending on zone

#### VOF - Rectangular Mesh
- Square/rectangular cells, uniform or with local refinement (AMR)
- Each cell contains an ink fraction between 0 and 1

#### LBM - Uniform Grid
- Very simple regular grid (here: 1 cell = 5 µm)
- Physics emerges from collisions between "particle packets"

#### SPH - Particle Cloud
- About 1000 mobile particles
- Each particle "influences" its neighbors within radius h


