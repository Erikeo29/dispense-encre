## Numerical Method Acronyms

| Acronym | Full Name | Description |
|---------|-----------|-------------|
| **FEM** | Finite Element Method | Finite element method |
| **VOF** | Volume of Fluid | Eulerian interface tracking method |
| **LBM** | Lattice Boltzmann Method | Lattice Boltzmann method |
| **SPH** | Smoothed Particle Hydrodynamics | Smoothed particle hydrodynamics |
| **CFD** | Computational Fluid Dynamics | Computational fluid mechanics |
| **DNS** | Direct Numerical Simulation | Direct numerical simulation |

---

## Numerical Scheme Acronyms

| Acronym | Full Name | Context |
|---------|-----------|---------|
| **PLIC** | Piecewise Linear Interface Calculation | VOF interface reconstruction |
| **CSF** | Continuum Surface Force | Surface tension model |
| **BGK** | Bhatnagar-Gross-Krook | LBM collision operator |
| **MRT** | Multiple Relaxation Time | Multi-relaxation LBM scheme |
| **SUPG** | Streamline Upwind Petrov-Galerkin | FEM convection stabilization |
| **PSPG** | Pressure Stabilizing Petrov-Galerkin | FEM pressure stabilization |
| **GLS** | Galerkin Least-Squares | Combined FEM stabilization |
| **ALE** | Arbitrary Lagrangian-Eulerian | Moving mesh |
| **AMR** | Adaptive Mesh Refinement | Adaptive meshing |
| **MULES** | Multidimensional Universal Limiter | OpenFOAM limiter for VOF |

---

## Dimensionless Numbers

| Symbol | Name | Expression | Physical Meaning |
|--------|------|------------|------------------|
| $Re$ | Reynolds | $\frac{\rho v L}{\eta}$ | Inertia / Viscosity |
| $We$ | Weber | $\frac{\rho v^2 L}{\sigma}$ | Inertia / Surface tension |
| $Oh$ | Ohnesorge | $\frac{\eta}{\sqrt{\rho \sigma L}}$ | Viscosity / (Inertia × Capillarity)$^{1/2}$ |
| $Ca$ | Capillary | $\frac{\eta v}{\sigma}$ | Viscosity / Capillarity |
| $Bo$ | Bond | $\frac{\rho g L^2}{\sigma}$ | Gravity / Capillarity |
| $De$ | Deborah | $\lambda \dot{\gamma}$ | Relaxation time × Shear rate |
| $Ma$ | Mach | $\frac{v}{c_s}$ | Velocity / Speed of sound |

---

## Physical Symbols

### Fluid Properties

| Symbol | Name | SI Unit |
|--------|------|---------|
| $\rho$ | Density | kg/m³ |
| $\eta$, $\mu$ | Dynamic viscosity | Pa·s |
| $\nu$ | Kinematic viscosity | m²/s |
| $\sigma$ | Surface tension | N/m |
| $\theta$ | Contact angle | ° or rad |

### Rheological Parameters

| Symbol | Name | Model | Unit |
|--------|------|-------|------|
| $\eta_0$ | Zero-shear viscosity | Carreau | Pa·s |
| $\eta_\infty$ | Infinite-shear viscosity | Carreau | Pa·s |
| $\lambda$ | Relaxation time | Carreau, Oldroyd-B | s |
| $n$ | Flow behavior index | Power law | - |
| $K$ | Consistency | Power law | Pa·s$^n$ |
| $\tau_0$ | Yield stress | Herschel-Bulkley | Pa |
| $\dot{\gamma}$ | Shear rate | All | s$^{-1}$ |

### Flow Variables

| Symbol | Name | Unit |
|--------|------|------|
| $\mathbf{v}$, $\mathbf{u}$ | Velocity vector | m/s |
| $p$ | Pressure | Pa |
| $\mathbf{D}$ | Rate of deformation tensor | s$^{-1}$ |
| $\boldsymbol{\tau}$ | Stress tensor | Pa |
| $\kappa$ | Interface curvature | m$^{-1}$ |

---

## Technical Terms

### Rheology

| Term | Definition |
|------|------------|
| **Shear-thinning** | Fluid whose viscosity decreases with shear |
| **Shear-thickening** | Fluid whose viscosity increases with shear |
| **Thixotropy** | Time-dependent viscosity (restructuring) |
| **Viscoelasticity** | Behavior combining viscosity and elasticity |
| **Newtonian fluid** | Constant viscosity independent of shear |
| **Non-Newtonian fluid** | Shear-dependent viscosity |
| **Yield stress** | Flow threshold stress |

### Fluid Mechanics

| Term | Definition |
|------|------------|
| **Two-phase flow** | Flow involving two phases (e.g., liquid/gas) |
| **Interface** | Separation surface between two phases |
| **Capillarity** | Phenomenon related to surface tension |
| **Wetting** | Fluid-solid interaction characterized by contact angle |
| **Meniscus** | Interface curvature at wall contact |
| **Pinch-off** | Filament necking before breakup |
| **Satellite** | Secondary droplet formed during breakup |
| **Coalescence** | Merging of two droplets |

### Numerical Methods

| Term | Definition |
|------|------------|
| **Eulerian** | Fixed reference frame (fixed grid) |
| **Lagrangian** | Moving reference frame (follows particles) |
| **Mesh** | Spatial discretization of the domain |
| **Meshless** | Method without fixed connectivity (e.g., SPH) |
| **Weak formulation** | Integral form of equations (finite elements) |
| **Test function** | Weighting function in weak formulation |
| **DOF** | Degrees of Freedom |
| **Inf-sup condition** | LBB stability criterion for mixed elements |

---

## Software and Libraries

| Name | Type | Language | Method |
|------|------|----------|--------|
| **FEniCS** | Open-source | Python/C++ | FEM |
| **OpenFOAM** | Open-source | C++ | VOF, FVM |
| **Palabos** | Open-source | C++ | LBM |
| **PySPH** | Open-source | Python | SPH |
| **COMSOL** | Commercial | GUI/MATLAB | Multiphysics FEM |
| **Ansys Fluent** | Commercial | GUI | VOF, FVM |
| **DualSPHysics** | Open-source | C++/CUDA | SPH GPU |
| **waLBerla** | Open-source | C++ | LBM HPC |

---

## Hardware Acronyms

| Acronym | Full Name | Description |
|---------|-----------|-------------|
| **CPU** | Central Processing Unit | Central processor |
| **GPU** | Graphics Processing Unit | Graphics processor |
| **HPC** | High Performance Computing | High performance computing |
| **CUDA** | Compute Unified Device Architecture | NVIDIA GPU API |
| **MPI** | Message Passing Interface | Distributed parallelization |
| **OpenMP** | Open Multi-Processing | Shared memory parallelization |
| **TFLOPS** | Tera Floating-Point Operations Per Second | Computing power unit |
| **RAM** | Random Access Memory | Main memory |

---

## Common Abbreviations

| Abbreviation | Meaning |
|--------------|---------|
| **DOD** | Drop-on-Demand |
| **CIJ** | Continuous Inkjet |
| **PIV** | Particle Image Velocimetry |
| **OCT** | Optical Coherence Tomography |
| **PINN** | Physics-Informed Neural Networks |
| **AI** | Artificial Intelligence |
| **FSI** | Fluid-Structure Interaction |

---

## SI Units

| Quantity | Unit | Symbol |
|----------|------|--------|
| Length | meter | m |
| Mass | kilogram | kg |
| Time | second | s |
| Force | newton | N |
| Pressure | pascal | Pa |
| Dynamic viscosity | pascal-second | Pa·s |
| Surface tension | newton per meter | N/m |
| Energy | joule | J |
| Power | watt | W |

### Prefixes

| Prefix | Symbol | Factor |
|--------|--------|--------|
| micro | µ | 10$^{-6}$ |
| milli | m | 10$^{-3}$ |
| kilo | k | 10$^{3}$ |
| mega | M | 10$^{6}$ |
| giga | G | 10$^{9}$ |
| tera | T | 10$^{12}$ |
