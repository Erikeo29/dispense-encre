# Modeling of Shear-Thinning Fluid Dispensing

## Scientific and Industrial Context

### Microfluidic Dispensing Technologies

Microfluidic dispensing encompasses a set of techniques for controlled deposition of volumes ranging from nanoliters to microliters. These processes find applications in numerous fields:

**Industrial applications:**
- Electrochemical sensor fabrication (Ag/AgCl ink deposition)
- Printed electronics (conductive circuits, RFID antennas)
- Bioprinting and biomaterial deposition
- Functional coatings and thin films
- Precision pharmaceutical dosing

### Physical Mechanisms

Fluid dispensing involves several coupled physical phenomena:
- **Two-phase flow**: fluid/air interaction at the interface
- **Capillarity**: surface tension and wall wetting
- **Rheology**: non-Newtonian behavior of complex fluids
- **Interface dynamics**: deformation, pinch-off, and stability

---

## Properties of Shear-Thinning Fluids

### Non-Newtonian Behavior

Shear-thinning fluids are **non-Newtonian fluids** whose apparent viscosity decreases under shear stress. This behavior is essential for dispensing: the fluid flows easily under pressure but maintains its shape at rest.

**Power law (Ostwald-de Waele):**

$$\tau = K\dot{\gamma}^n \quad \text{with } n < 1$$

where $\tau$ is the shear stress, $K$ the consistency index, $\dot{\gamma}$ the shear rate, and $n$ the behavior index.

**Carreau-Yasuda model:**

$$\eta(\dot{\gamma}) = \eta_\infty + \frac{\eta_0 - \eta_\infty}{[1 + (k\dot{\gamma})^a]^{(1-n)/a}}$$

where $\eta_0$ and $\eta_\infty$ are the zero-shear and infinite-shear viscosities, and $k$, $a$ are fitting parameters.

**Example:** A typical Ag/AgCl ink exhibits $\eta_0 = 0.5$–$5$ Pa·s (at rest) and $\eta_\infty = 0.05$ Pa·s under high shear.

---

## Fundamental Dimensionless Numbers

Fluid dispensing modeling involves several interdependent physical phenomena, characterized by the following dimensionless numbers:

| Number | Expression | Meaning | Typical Value |
|--------|------------|---------|---------------|
| **Reynolds** | $Re = \frac{\rho v D}{\eta}$ | Inertial vs viscous effects | 10 – 100 |
| **Weber** | $We = \frac{\rho v^2 L}{\sigma}$ | Inertial forces vs surface tension | $We < 10$ |
| **Ohnesorge** | $Oh = \frac{\eta}{\sqrt{\rho \sigma D}}$ | Viscosity, surface tension, and size | $Oh < 0.5$ |
| **Deborah** | $De = \lambda \dot{\gamma}$ | Viscoelastic effects (relaxation time $\lambda$) | Variable |
| **Capillary** | $Ca = \frac{\eta v}{\sigma}$ | Viscosity vs capillarity | $Ca \ll 1$ |
| **Bond** | $Bo = \frac{\rho g L^2}{\sigma}$ | Gravity vs surface tension | $Bo \ll 1$ |

**Physical interpretation:**
- $Re$ between 10 and 100: laminar regime with inertial effects
- $Oh < 0.5$: stable droplet/filament formation
- $Bo \ll 1$: gravity negligible (dominant capillary regime)

---

## Numerical Modeling Challenges

### Technical Issues

| Challenge | Description | Approach |
|-----------|-------------|----------|
| **Interface tracking** | Capture fluid/air interface deformation | VOF, Phase-Field, Level-Set |
| **Complex rheology** | Model non-Newtonian behavior | Constitutive laws (Carreau, Herschel-Bulkley) |
| **Wetting** | Handle dynamic contact angles | Specific boundary conditions |
| **Multi-scale** | From micron (interface) to millimeter (well) | Adaptive meshes, meshless methods |
| **Computational cost** | Expensive 3D transient simulations | GPU, parallelization, hybrid methods |

---

## Physical System Studied

### Geometric Configuration

The modeled system consists of:
- **Dispensing nozzle**: diameter 200–350 µm, positioned above the well
- **Micro-well**: diameter 800–1500 µm, depth ~130 µm
- **Fluid**: shear-thinning Ag/AgCl ink ($\rho$ = 3000 kg/m³)
- **Environment**: ambient air

### Simulation Parameters

| Parameter | Range | Unit |
|-----------|-------|------|
| Well diameter | 800 – 1500 | µm |
| Nozzle diameter | 200 – 350 | µm |
| Horizontal offset | 0, -75, -150 | µm |
| Viscosity $\eta_0$ | 0.5 – 5 | Pa·s |
| Wall contact angle | 35 – 90 | ° |
| Electrode contact angle | 35 – 75 | ° |
| Dispensing time | 20 – 40 | ms |

---

## Multi-Model Approach

This project compares four complementary numerical methods:

| Model | Approach | Main Advantage |
|-------|----------|----------------|
| **FEM / Phase-Field** | Eulerian, finite elements | Thermodynamic accuracy, multiphysics coupling |
| **VOF** | Eulerian, finite volumes | Robustness, industrial standard |
| **LBM** | Mesoscopic, lattice | GPU performance, complex geometries |
| **SPH** | Lagrangian, meshless | Free surfaces, large deformations |

---

## References

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.
