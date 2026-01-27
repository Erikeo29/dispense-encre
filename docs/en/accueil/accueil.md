**Contents:**
1. Project Objective
2. Target Application
3. Navigation
4. Methodological Note

---

## 1. Project Objective

This project presents a **comparative study of three numerical methods** for simulating shear-thinning fluid dispensing into micro-via. The application enables visualization and comparison of two-phase flow simulation results using different approaches:

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

The animations and images presented in this application come from **pre-calculated** simulations. The VOF, LBM and SPH codes were developed by the author of this site with the use of AI tools for program development and debugging on a standard PC. The simulations were performed with various parameter combinations (geometry, viscosity, contact angles, dispensing time...) as a parametric study. The results were then exported as GIF files (animations) and PNG files (final images) to populate this application.

This application is a **results viewer**, not a real-time simulator. Indeed, running these simulations requires substantial Python or OpenFOAM package configurations; the modeling time is also significant, ranging from 10 minutes to 2 hours per unit simulation depending on the numerical model type and parameters studied. The codes are provided in the "Code" tabs of the 3 models to enable reproduction of these simulations on other machines.
