## Project Objective

This project presents a **comparative study of four numerical methods** for simulating shear-thinning fluid dispensing into micro-wells. The application enables visualization and comparison of two-phase flow simulation results using different approaches:

- **FEM / Phase-Field**: Finite Element Method with phase-field interface tracking
- **VOF (Volume of Fluid)**: Industrial standard Eulerian method (OpenFOAM)
- **LBM (Lattice Boltzmann)**: GPU-optimized mesoscopic approach (Palabos)
- **SPH (Smoothed Particle Hydrodynamics)**: Meshless Lagrangian method (PySPH)

---

## Target Application

The simulations model **Ag/AgCl ink dispensing** into micro-wells for electrochemical sensor fabrication. This process requires precise control of filling, wetting, and final deposit shape.

**Key parameters studied:**
- Geometry: well diameter (800–1500 µm), nozzle diameter (200–350 µm)
- Rheology: variable viscosity (Carreau model)
- Wetting: contact angles on well bottom, vertical walls, and substrate surface.

---

## Navigation

Use the sidebar menu to explore the different chapters:
1. **Introduction**: Scientific context and dimensionless numbers
2. **Model Comparison**: Detailed comparison tables
3. **Model Pages**: Physics, source code, and simulation examples: flow animations during dispensing (GIF files) and final state images (PNG files).
