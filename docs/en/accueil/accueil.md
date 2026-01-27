**Contents:**
1. Project Objective
2. Target Application
3. Navigation
4. Methodological Note

---

## 1. Project Objective

The purpose of this application is to enable visualization and comparison of the results of **three numerical methods** for simulating shear-thinning fluid dispensing into micro-via. The application allows exploring results from two-phase flow simulations performed with different approaches:

- **VOF (Volume of Fluid)**: Industrial standard Eulerian method (OpenFOAM)
- **LBM (Lattice Boltzmann)**: GPU-optimized mesoscopic approach (Palabos)
- **SPH (Smoothed Particle Hydrodynamics)**: Meshless Lagrangian method (PySPH)

---

## 2. Target Application

The simulations model **shear-thinning ink dispensing** into micro-via.

**Key parameters studied:**
- Geometry: micro-via diameter (800–1500 µm), nozzle diameter (200–350 µm)
- Nozzle position: X and Y offset (vertical and horizontal offset relative to the via)
- Rheology: variable viscosity (Carreau model)
- Wetting: contact angles on micro-via bottom, vertical walls, and substrate surface.

---

## 3. Navigation

The application is structured around several tools to facilitate exploration:

1.  **Sidebar (on the left)**: This is the main navigation tool. It allows you to move between the major sections of the project:
    *   **Introduction**: Scientific context, properties of shear-thinning fluids, and presentation of the studied physical system.
    *   **Model Comparison**: Summary tables to compare the different approaches.
    *   **Model Pages**: Each model's page (VOF, LBM, SPH) contains tabs to explore the underlying physics, the source code used, and the simulation results (GIF animations and PNG images).

2.  **Floating Navigation Buttons (on the right)**: Two arrows allow you to quickly scroll to the top or bottom of long pages.

3.  **AI Assistant (in the sidebar)**: A pop-up opens to answer your questions about the physics, numerical methods, or the project in general.

---

## 4. Methodological Note

The animations and images presented in this application come from **pre-calculated** simulations. The VOF, LBM and SPH codes were developed by the author of this site with the use of AI tools for program development and debugging on a standard laptop (Linux base, 1.5-3.5 GHz, 6 CPU / 12 threads), 32GB RAM, 8GB GPU (when usable: LBM, SPH DualSPHysics). The simulations were performed with various parameter combinations (geometry, viscosity, contact angles, dispensing time...) as a parametric study. The results were then exported as GIF files (animations) and PNG files (final images) to populate this application.

This application is a **results viewer**, not a real-time simulator. Indeed, running these simulations requires substantial Python or OpenFOAM package configurations; the modeling time is also significant, ranging from 10 minutes to 2 hours per unit simulation depending on the numerical model type and parameters studied. The codes are provided in the "Code" tabs of the 3 models to enable users to copy and reproduce these simulations on other machines.

The author certifies that this project was developed from a "blank slate", without copying from any existing sources or websites. The code implementation, application structure, and technical research were conducted exclusively using AI tools and Web-based documentation. This work is released as open-source: it may be freely copied, duplicated, and adapted for learning purposes or for the use of the physical and numerical models presented here.
