**Sommaire :**
1. Méthode des Éléments Finis (FEM) / Phase-Field
2. Volume of Fluid (VOF)
3. Lattice Boltzmann Method (LBM)
4. Smoothed Particle Hydrodynamics (SPH)
5. Rhéologie et Mouillage
6. Ouvrages Généraux
7. Ressources en Ligne

Cette page regroupe les références bibliographiques utilisées dans ce projet. **Tous les liens pointent vers des ressources en accès libre.**

---

## 1. Méthode des Éléments Finis (FEM) / Phase-Field

1. **Yue, P., Feng, J. J., Liu, C., & Shen, J.** (2004). *A diffuse-interface method for simulating two-phase flows of complex fluids*. Journal of Fluid Mechanics, 515, 293-317. [PDF gratuit (ResearchGate)](https://www.researchgate.net/publication/231965731_A_diffuse-interface_method_of_simulating_two-phase_flows_of_complex_fluids)
   - Extension du modèle de champ de phase aux fluides complexes.

2. **Tezduyar, T. E.** (1992). *Stabilized finite element formulations for incompressible flow computations*. Advances in Applied Mechanics, 28, 1-44. [PDF gratuit (TAFSM)](https://tafsm.org/PUB_PRE/jALL/j32-AAM-Stab92.pdf)
   - Méthodes de stabilisation SUPG/PSPG pour les écoulements incompressibles.

3. **Logg, A., Mardal, K.-A., & Wells, G.** (Eds.). (2012). *Automated Solution of Differential Equations by the Finite Element Method: The FEniCS Book*. Springer. [PDF gratuit (FEniCS Project)](http://launchpad.net/fenics-book/trunk/final/+download/fenics-book-2011-10-27-final.pdf)
   - Documentation complète du framework FEniCS.

---

## 2. Volume of Fluid (VOF)

4. **Hirt, C. W., & Nichols, B. D.** (1981). *Volume of fluid (VOF) method for the dynamics of free boundaries*. Journal of Computational Physics, 39(1), 201-225. [PDF gratuit (SJTU)](https://dcwan.sjtu.edu.cn/PlugIns/ckfinder/userfiles/files/Hirt%20%E5%92%8C%20Nichols%20-%201981%20-%20Volume%20of%20fluid%20(VOF)%20method%20for%20the%20dynamics%20of%20f(1).pdf)
   - Article fondateur de la méthode VOF.

5. **Brackbill, J. U., Kothe, D. B., & Zemach, C.** (1992). *A continuum method for modeling surface tension*. Journal of Computational Physics, 100(2), 335-354. [PDF gratuit (Sorbonne/LJLL)](https://www.ljll.fr/~frey/papers/Navier-Stokes/Brackbill%20J.U.,%20A%20continuum%20method%20for%20modeling%20surface%20tension.pdf)
   - Modèle CSF (Continuum Surface Force) pour la tension de surface.

6. **Popinet, S.** (2009). *An accurate adaptive solver for surface-tension-driven interfacial flows*. Journal of Computational Physics, 228(16), 5838-5866. [PDF gratuit (HAL Science)](https://hal.science/hal-01445445)
   - Solveur adaptatif de haute précision pour les écoulements interfaciaux (Basilisk/Gerris).

7. **Jasak, H.** (1996). *Error Analysis and Estimation for the Finite Volume Method with Applications to Fluid Flows*. PhD Thesis, Imperial College London. [PDF gratuit (Imperial College)](https://spiral.imperial.ac.uk/handle/10044/1/8335)
   - Fondements théoriques de la méthode des volumes finis dans OpenFOAM.

---

## 3. Lattice Boltzmann Method (LBM)

8. **Chen, S., & Doolen, G. D.** (1998). *Lattice Boltzmann method for fluid flows*. Annual Review of Fluid Mechanics, 30(1), 329-364. [PDF gratuit (UC eScholarship)](https://escholarship.org/content/qt8vf0g3zk/qt8vf0g3zk_noSplash_d3843a251a7f7e13bb8782f13ecc40a0.pdf)
   - Revue complète de la méthode LBM.

9. **Shan, X., & Chen, H.** (1993). *Lattice Boltzmann model for simulating flows with multiple phases and components*. Physical Review E, 47(3), 1815. [ResearchGate](https://www.researchgate.net/publication/13329506_Lattice_Boltzmann_Model_for_Simulating_Flows_with_Multiple_Phases_and_Components)
   - Modèle Shan-Chen pour les écoulements multiphasiques (article milestone PRE).

10. **Krüger, T., et al.** (2017). *The Lattice Boltzmann Method: Principles and Practice*. Springer. [PDF gratuit (Academia.edu)](https://www.academia.edu/40196538/Graduate_Texts_in_Physics_The_Lattice_Boltzmann_Method_Principles_and_Practice)
    - Ouvrage de référence complet sur la méthode LBM.

11. **Fakhari, A., & Rahimian, M. H.** (2010). *Phase-field modeling by the method of lattice Boltzmann equations*. Physical Review E, 81(3), 036707. [ResearchGate](https://www.researchgate.net/publication/43020969_Phase-field_modeling_by_the_method_of_lattice_Boltzmann_equations)
    - Couplage LBM et modèle de champ de phase.

---

## 4. Smoothed Particle Hydrodynamics (SPH)

12. **Monaghan, J. J.** (2005). *Smoothed particle hydrodynamics*. Reports on Progress in Physics, 68(8), 1703-1759. [PDF gratuit (U Toronto)](https://planets.utsc.utoronto.ca/~pawel/PHYD57/monaghan-sph2005.pdf)
    - Revue fondamentale de la méthode SPH par son créateur.

13. **Adami, S., Hu, X. Y., & Adams, N. A.** (2012). *A generalized wall boundary condition for smoothed particle hydrodynamics*. Journal of Computational Physics, 231(21), 7057-7075. [PDF gratuit (Academia.edu)](https://www.academia.edu/4728278/A_generalized_wall_boundary_condition_for_smoothed_particle_hydrodynamics)
    - Conditions aux limites généralisées pour SPH.

14. **Liu, M. B., & Liu, G. R.** (2010). *Smoothed Particle Hydrodynamics (SPH): an Overview and Recent Developments*. Archives of Computational Methods in Engineering, 17, 25-76. [PDF gratuit (Semantic Scholar)](https://www.semanticscholar.org/paper/Smoothed-Particle-Hydrodynamics-(SPH):-an-Overview-Liu-Liu/6ae2960b7cbeab3e1969033b343dbe3594c99cb3)
    - Revue des développements récents en SPH.

---

## 5. Rhéologie et Mouillage

15. **de Gennes, P. G.** (1985). *Wetting: statics and dynamics*. Reviews of Modern Physics, 57(3), 827-863. [PDF gratuit (UC Irvine)](https://www.physics.uci.edu/~taborek/publications/other/deGennesWettingReview.pdf)
    - Article fondateur sur la physique du mouillage (Prix Nobel 1991).

---

## 6. Ouvrages Généraux

16. **Derby, B.** (2010). *Inkjet printing of functional and structural materials*. Annual Review of Materials Research, 40, 395-414. [PDF gratuit (U Manchester)](https://pure.manchester.ac.uk/ws/files/174918681/DERBYwithfigures_2017_02_22_19_00_59_UTC_.pdf)
    - Introduction aux applications industrielles de l'impression jet d'encre.

---

## 7. Ressources en Ligne

- [OpenFOAM Documentation](https://openfoam.org) — Solveurs VOF (interFoam, isoAdvector)
- [FEniCS Project](https://fenicsproject.org) — Éléments finis Python/C++
- [Palabos](https://palabos.unige.ch) — LBM open-source (C++)
- [PySPH Documentation](https://pysph.readthedocs.io) — SPH en Python
- [CFD Online Forums](https://www.cfd-online.com/Forums/) — Communauté CFD
- [Basilisk](http://basilisk.fr) — VOF adaptatif (Popinet)
