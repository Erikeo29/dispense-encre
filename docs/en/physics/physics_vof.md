**Contents:**
1. Method Principle
2. Fundamental Equations
3. Mathematical Formulation
4. Advantages and Limitations
5. Computational Cost
6. Open-Source Libraries
7. References

---

## 1. Method Principle

The **VOF (Volume of Fluid)** method is an Eulerian approach for interface tracking in two-phase flows. It represents the **industrial standard** for free surface simulations, particularly with OpenFOAM's `interFoam` solver.

### Main Variable: Volume Fraction α

| Value | Meaning |
|-------|---------|
| α = 1 | Ink (fluid 1) |
| α = 0 | Air (fluid 2) |
| 0 < α < 1 | Interface zone |

**Key Advantage:** Perfect mass conservation, intrinsic property of the formulation.

---

## 2. Fundamental Equations

### 2.1 Navier-Stokes Equations

**Mass conservation:**
$$\nabla \cdot \mathbf{v} = 0$$

**Momentum conservation:**
$$\rho\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho\mathbf{g} + \mathbf{f}_\sigma$$

### 2.2 α Transport Equation

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

**With artificial compression (MULES - OpenFOAM):**
$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\mathbf{v} \alpha) + \nabla \cdot [\mathbf{v}_r \alpha (1-\alpha)] = 0$$

where **v**_r = c_α |**v**| **n** is a compression velocity acting only at the interface to counter numerical diffusion.

### 2.3 Surface Tension Force (CSF)

The **Continuum Surface Force** model by Brackbill:

$$\mathbf{f}_\sigma = \sigma \kappa \nabla \alpha$$

where κ = -∇·(∇α/|∇α|) is the interface curvature.

---

## 3. Mathematical Formulation

### 3.1 Mixture Properties

Physical properties are linearly interpolated:

$$\rho = \alpha \rho_1 + (1-\alpha) \rho_2$$
$$\eta = \alpha \eta_1 + (1-\alpha) \eta_2$$

### 3.2 Carreau Model (Non-Newtonian Fluids)

$$\eta_{eff}(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) [1 + (\lambda \dot{\gamma})^2]^{(n-1)/2}$$

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Density | ρ | 3000 | kg/m³ |
| Zero-shear viscosity | η₀ | 0.5 – 5 | Pa·s |
| Infinite-shear viscosity | η∞ | 0.05 – 0.167 | Pa·s |
| Relaxation time | λ | 0.15 | s |
| Power-law index | n | 0.7 | - |
| Surface tension | σ | 0.04 | N/m |

### 3.3 OpenFOAM Configuration (`transportProperties`)

```cpp
transportModel Carreau;

CarreauCoeffs {
    nu0   nu0 [0 2 -1 0 0 0 0] 1.667e-4;  // η₀/ρ
    nuInf nuInf [0 2 -1 0 0 0 0] 5.56e-5; // η∞/ρ
    k     k [0 0 1 0 0 0 0] 0.15;          // λ
    n     n [0 0 0 0 0 0 0] 0.7;           // n
}

sigma sigma [1 0 -2 0 0 0 0] 0.04;
```

---

## 4. Advantages and Limitations

| Advantages | Limitations |
|------------|-------------|
| Proven robustness (>25 years) | Numerical interface diffusion |
| Perfect mass conservation | Fine meshes required near interface |
| Industrial standard (OpenFOAM) | Multiple coalescences difficult |
| Interface precision 0.1–1 µm (with PLIC) | Complex rheology (thixotropy) difficult |
| GPU support since OpenFOAM 10 | Memory cost for AMR |

---

## 5. Computational Cost

**Reference domain:** 1.2 mm × 0.5 mm (micro-via dispensing)

| Configuration | Cells | Resolution | Time | Hardware |
|---------------|-------|------------|------|----------|
| **This project** | ~50k | ~5 µm | **30–60 min** | 8 cores |
| High resolution | ~500k | ~1.5 µm | 4–8 h | 16 cores |
| With AMR | 50k–500k | 1–10 µm (adaptive) | 2–4 h | 16 cores |

> **Interpretation:** 50k hexahedral cells on 1.2×0.5 mm correspond to ~5 µm resolution, compatible with PLIC interface reconstruction.

**GPU Acceleration:** x5–x10 for matrix operations (OpenFOAM ≥ v10 with CUDA).

---

## 6. Open-Source Libraries

| Library | Language | Focus | Parallelization |
|---------|----------|-------|-----------------|
| **OpenFOAM** | C++ | Industrial standard, VOF/interFoam | MPI, CUDA |
| **Basilisk** | C | Research, native AMR | MPI |
| **Gerris** | C | Basilisk precursor | MPI |

---

## 7. References

> **Note**: For the complete list of references, see the **Bibliography** section in the Appendices menu.
