**Contents:**
1. Project Objective
2. Target Application
3. Navigation
4. Methodological Note

---

## 1. Project Objective

This project presents a **comparative study of four numerical methods** for simulating shear-thinning fluid dispensing into micro-via. The application enables visualization and comparison of two-phase flow simulation results using different approaches:

- **FEM / Phase-Field**: Finite Element Method with phase-field interface tracking
- **VOF (Volume of Fluid)**: Industrial standard Eulerian method (OpenFOAM)
- **LBM (Lattice Boltzmann)**: GPU-optimized mesoscopic approach (Palabos)
- **SPH (Smoothed Particle Hydrodynamics)**: Meshless Lagrangian method (PySPH)

---

## 2. Target Application

The simulations model **shear-thinning ink dispensing** into micro-via.

**Key parameters studied:**
- Geometry: micro-via diameter (800–1500 µm), nozzle diameter (200–350 µm)
- Rheology: variable viscosity (Carreau model)
- Wetting: contact angles on micro-via bottom, vertical walls, and substrate surface.

---

## 3. Navigation

Use the sidebar menu to explore the different chapters:
1. **Introduction**: Scientific context and dimensionless numbers
2. **Model Comparison**: Detailed comparison tables
3. **Model Pages**: Physics, source code, and simulation examples: flow animations during dispensing (GIF files) and final state images (PNG files).

---

## 4. Methodological Note

The animations and images presented in this application come from **pre-calculated** simulations. The FEM, VOF, LBM and SPH codes were developed and executed on a standard PC with various parameter combinations (geometry, viscosity, contact angles), then the results were exported as GIF files (animations) and PNG files (final images).

This application is a **results viewer**, not a real-time simulator.
