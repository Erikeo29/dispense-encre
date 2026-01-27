**Contents:**
1. Conclusion
2. Perspectives
   - 2.1 Open Source Python Alternatives
   - 2.2 Artificial Intelligence and Hybrid Modeling
   - 2.3 4D Printing and Smart Inks
   - 2.4 Research Opportunities
   - 2.5 Quantum Computing

---

## 1. Conclusion

This study enabled the modeling of shear-thinning ink dispensing into micro-via using three distinct numerical methods: VOF, LBM, and SPH.

The results obtained show trends comparable to experimental observations. Notably, the impact of nozzle position along the X-axis on overflow phenomena and filling uniformity was demonstrated. Similarly, expected physicochemical phenomena were reproduced: the influence of viscosity and contact angles (surface energy) on ink spreading corresponds to anticipated physical behaviors.

Differences in results appear depending on the models used, which is consistent given their very different numerical formulations (Eulerian vs Lagrangian, mesh-based vs meshless, macroscopic vs mesoscopic). However, overall trends remain comparable across all three approaches, reinforcing confidence in the validity of the simulations.

To go further, it would be necessary to continue improving the codes, refine the physicochemical models (particularly rheology and dynamic wetting), and optimize numerical parameters to improve result accuracy compared to experimental observations.

---

## 2. Perspectives

### 2.1 Open Source Python Alternatives

The failure of the initial FEM/Phase-Field implementation (based on an attempt to reproduce commercial models) highlighted the need for robust, truly open-source Python tools for advanced fluid mechanics:

- **Firedrake**: An automated system for solving partial differential equations using the finite element method. High performance for computational fluid dynamics (CFD), it offers a syntax close to mathematics (UFL) while generating optimized C code.
- **SfePy (Simple Finite Elements in Python)**: A flexible library for solving coupled partial differential equation systems (mechanical, thermal, fluids) using finite elements. Ideal for complex multiphysics problems.
- **Hybrid FEM/SPH Systems**: A promising approach consists of coupling the precision of finite elements (FEM) near solid walls with the flexibility of SPH (Smoothed Particle Hydrodynamics) for free surfaces and large deformations, leveraging the best of both worlds.

### 2.2 Artificial Intelligence and Hybrid Modeling

### PINN (Physics-Informed Neural Networks)

**PINNs** combine physical equations with neural networks to accelerate simulations:

- **Principle:** The network learns to solve Navier-Stokes equations by minimizing both data error and physical equation violation.
- **Inkjet application:** Raissi et al. (2020) used PINNs to solve Navier-Stokes with precision comparable to FEM but 100× faster.
- **Current limitation:** Limited generalization outside the training domain.

### Surrogate Models

**Surrogate models** involve training a "simplified AI" (like a neural network) to instantly predict the outcome of a complex simulation:

- **Principle:** A few hundred real simulations (VOF, LBM...) are performed to "show" the model how the fluid reacts.
- **Advantage:** Once trained, the model can predict if a dispensing operation will overflow in milliseconds, without having to run a multi-hour OpenFOAM calculation.
- **Potential:** Real-time optimization of parameters on a production line.

### Reinforcement Learning

- **Application:** An RL agent can learn to adjust $v_{max}$ and $\tau$ to minimize satellites.
- **Potential:** Real-time adaptive control of print heads.

---

### 2.3 4D Printing and Smart Inks

Shear-thinning inks are increasingly used for **4D printing** (materials that change shape after printing):

### Shape-Memory Inks

- Polymers that deform under temperature or light.
- **Modeling:** FEM coupling with thermomechanical models.

### Conductive Inks (Shear-Thinning)

- Silver or graphene nanoparticles for printed electronics.
- **Challenges:** Complex rheology (thixotropy, viscoelasticity) + sedimentation.

---

### 2.4 Research Opportunities

### Rheology-Interface Coupling

**Problem:** No model simultaneously handles complex non-Newtonian rheology (thixotropy) and free interfaces with sub-micron precision.

**Research directions:**
- **VOF-SPH hybridization:** VOF for interface tracking, SPH for rheology.
- **LBM with advanced rheology:** Implement thixotropy and viscoelasticity models in LBM.
- **Adaptive FEM:** Dynamic meshes that adapt to high-shear zones.

### Sub-Micron Scales

**Problem:** Droplets < 5 µm are difficult to model due to dominant surface tension effects and prohibitive computation times.

**Research directions:**
- **Multi-scale models:** Couple a macroscopic model (VOF, FEM) with a mesoscopic model (LBM, DPD).
- **Atomistic simulations:** Use molecular dynamics (MD) for droplets < 1 µm.
- **Asymptotic approaches:** Develop reduced models for sub-micron droplets (thin film theory).

---

### 2.5 Quantum Computing

Quantum computing could revolutionize complex flow modeling:

### Quantum Algorithms for SPH

- Quantum computers could simulate 10⁹ SPH particles in real-time.
- **Example:** IBM demonstrated (2023) a quantum algorithm for molecular dynamics, applicable to SPH.

### Mesh Optimization

- Quantum graph partitioning algorithms could reduce the cost of 3D adaptive meshes.

---

## References

> **Note**: For references discussing the resources used in this project, see the **Bibliography** section in the Appendices menu.
