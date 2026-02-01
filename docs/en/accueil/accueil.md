

**Author's note** — *This project was designed entirely by the author, from a blank slate through to publication. Content creation was carried out with the support of artificial intelligence tools, particularly for writing and debugging code, internet research, and content formatting.
All results shown in this project are derived from analytical and deterministic physical models solved by validated numerical solvers.
This work is released as open-source: it may be freely copied, duplicated, and adapted for learning purposes or for the use of the physical and numerical models presented here.*

&nbsp;

**Contents:**
1. Project Objective
2. Target Application
3. Navigation
4. Methodological Note

---

## 1. Project Objective

The purpose of this application is to model, visualize and compare the results of **three numerical methods** for simulating shear-thinning fluid dispensing into micro-via. The application allows exploring results from two-phase flow simulations performed with different approaches:

- **VOF (Volume of Fluid)**: Eulerian method (OpenFOAM)
- **LBM (Lattice Boltzmann)**: GPU-optimized mesoscopic approach (Palabos)
- **SPH (Smoothed Particle Hydrodynamics)**: Meshless Lagrangian method (PySPH)

---

## 2. Target Application

The simulations model **shear-thinning ink dispensing** into micro-via.

**Key parameters studied:**
- Geometry: micro-via diameter, nozzle diameter,
- Nozzle position: X and Y offset (vertical and horizontal offset relative to the via)
- Rheology: viscosity (Carreau model)
- Wetting: contact angles on the micro-via bottom, on the vertical walls of the well, on the horizontal substrate surface.

---

## 3. Navigation

The application is structured with the following tools:

1.  **Sidebar (on the left)**: navigation tool between the different sections of the project:
    *   **Introduction**: Scientific context, properties of shear-thinning fluids, and presentation of the studied physical system.
    *   **Model Comparison**: synthetic analyses for comparison of the different approaches.
    *   **Modeling Results**: Each model's page (VOF, LBM, SPH) contains tabs to explore the underlying physics, the source code used, and the simulation results (GIF animations and PNG images).
    *   **Appendices**: Conclusion, perspectives, technical glossary, key equations, and thematic bibliography.


2.  **Floating Navigation Buttons (on the right)**: Two arrows allow you to quickly scroll to the top or bottom of pages.

3.  **AI Assistant (in the sidebar)**: A pop-up opens to answer your questions about the physics, numerical methods, or the project in general.

---

## 4. Methodological Note

The animations and images presented in this application come from **pre-calculated** simulations. The project was carried out on a standard laptop: Linux environment via WSL2, 1.5-3.5 GHz processor, 6 CPU / 12 threads, 32 GB RAM, 8 GB GPU (when usable: LBM, SPH DualSPHysics). The 2D simulations were performed with various combinations of factors (geometry, viscosity, contact angles, dispensing time...) as a parametric study. The results were then exported as GIF files (animations) and PNG files (final state images) to populate this application.

This application is therefore a **results viewer**, not a real-time simulator. Indeed, running these simulations requires specific environment configurations and Python or OpenFOAM packages; the modeling time is also significant, ranging from 10 minutes to 2 hours per unit simulation depending on the numerical model type and parameters studied. The codes are provided in the "Code" tabs of the 3 models so they can be copied and used to reproduce these simulations on other machines.
