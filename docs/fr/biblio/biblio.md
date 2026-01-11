# Bibliographie

Cette page regroupe toutes les références bibliographiques utilisées dans ce projet de simulation de dispense d'encre rhéofluidifiante.

---

## Méthode des Éléments Finis (FEM) / Phase-Field

1. **Jacqmin, D.** (1999). *Calculation of two-phase Navier-Stokes flows using phase-field modeling*. Journal of Computational Physics, 155(1), 96-127. [DOI:10.1006/jcph.1999.6332](https://doi.org/10.1006/jcph.1999.6332)
   - Article fondateur du modèle de champ de phase pour les écoulements diphasiques.

2. **Yue, P., Feng, J. J., Liu, C., & Shen, J.** (2004). *A diffuse-interface method for simulating two-phase flows of complex fluids*. Journal of Fluid Mechanics, 515, 293-317. [DOI:10.1017/S0022112004000370](https://doi.org/10.1017/S0022112004000370)
   - Extension du modèle de champ de phase aux fluides complexes.

3. **Brooks, A. N., & Hughes, T. J. R.** (1982). *Streamline upwind/Petrov-Galerkin formulations for convection dominated flows*. Computer Methods in Applied Mechanics and Engineering, 32(1-3), 199-259. [DOI:10.1016/0045-7825(82)90071-8](https://doi.org/10.1016/0045-7825(82)90071-8)
   - Formulation SUPG pour la stabilisation des éléments finis.

4. **Tezduyar, T. E.** (1991). *Stabilized finite element formulations for incompressible flow computations*. Advances in Applied Mechanics, 28, 1-44.
   - Méthodes de stabilisation pour les écoulements incompressibles.

5. **Logg, A., Mardal, K.-A., & Wells, G.** (Eds.). (2012). *Automated Solution of Differential Equations by the Finite Element Method: The FEniCS Book*. Springer. ISBN: 978-3-642-23098-1.
   - Documentation complète du framework FEniCS.

6. **Basaran, O. A.** (2002). *Small-scale free surface flows with breakup: Drop formation and emerging applications*. AIChE Journal, 48(9), 1842-1848. [DOI:10.1002/aic.690480902](https://doi.org/10.1002/aic.690480902)
   - Revue sur la formation de gouttes et les surfaces libres.

---

## Volume of Fluid (VOF)

7. **Hirt, C. W., & Nichols, B. D.** (1981). *Volume of fluid (VOF) method for the dynamics of free boundaries*. Journal of Computational Physics, 39(1), 201-225. [DOI:10.1016/0021-9991(81)90145-5](https://doi.org/10.1016/0021-9991(81)90145-5)
   - Article fondateur de la méthode VOF.

8. **Brackbill, J. U., Kothe, D. B., & Zemach, C.** (1992). *A continuum method for modeling surface tension*. Journal of Computational Physics, 100(2), 335-354. [DOI:10.1016/0021-9991(92)90240-Y](https://doi.org/10.1016/0021-9991(92)90240-Y)
   - Modèle CSF (Continuum Surface Force) pour la tension de surface.

9. **Popinet, S.** (2009). *An accurate adaptive solver for surface-tension-driven interfacial flows*. Journal of Computational Physics, 228(16), 5838-5866. [DOI:10.1016/j.jcp.2009.04.042](https://doi.org/10.1016/j.jcp.2009.04.042)
   - Solveur adaptatif de haute précision pour les écoulements interfaciaux.

10. **Jasak, H.** (1996). *Error Analysis and Estimation for the Finite Volume Method with Applications to Fluid Flows*. PhD Thesis, Imperial College London.
    - Fondements théoriques de la méthode des volumes finis dans OpenFOAM.

---

## Lattice Boltzmann Method (LBM)

11. **Chen, S., & Doolen, G. D.** (1998). *Lattice Boltzmann method for fluid flows*. Annual Review of Fluid Mechanics, 30(1), 329-364. [DOI:10.1146/annurev.fluid.30.1.329](https://doi.org/10.1146/annurev.fluid.30.1.329)
    - Revue complète de la méthode LBM.

12. **Shan, X., & Chen, H.** (1993). *Lattice Boltzmann model for simulating flows with multiple phases and components*. Physical Review E, 47(3), 1815. [DOI:10.1103/PhysRevE.47.1815](https://doi.org/10.1103/PhysRevE.47.1815)
    - Modèle Shan-Chen pour les écoulements multiphasiques.

13. **Krüger, T., Kusumaatmaja, H., Kuzmin, A., Shardt, O., Silva, G., & Viggen, E. M.** (2017). *The Lattice Boltzmann Method: Principles and Practice*. Springer. ISBN: 978-3-319-44649-3. [DOI:10.1007/978-3-319-44649-3](https://doi.org/10.1007/978-3-319-44649-3)
    - Ouvrage de référence complet sur la méthode LBM.

14. **Huang, H., Sukop, M., & Lu, X.** (2015). *Multiphase Lattice Boltzmann Methods: Theory and Application*. Wiley-Blackwell. ISBN: 978-1-118-97133-8.
    - Applications multiphasiques de la méthode LBM.

15. **Fakhari, A., & Rahimian, M. H.** (2010). *Phase-field modeling by the method of lattice Boltzmann equations*. Physical Review E, 81(3), 036707. [DOI:10.1103/PhysRevE.81.036707](https://doi.org/10.1103/PhysRevE.81.036707)
    - Couplage LBM et modèle de champ de phase.

---

## Smoothed Particle Hydrodynamics (SPH)

16. **Monaghan, J. J.** (2005). *Smoothed particle hydrodynamics*. Reports on Progress in Physics, 68(8), 1703-1759. [DOI:10.1088/0034-4885/68/8/R01](https://doi.org/10.1088/0034-4885/68/8/R01)
    - Revue fondamentale de la méthode SPH.

17. **Morris, J. P., Fox, P. J., & Zhu, Y.** (1997). *Modeling low Reynolds number incompressible flows using SPH*. Journal of Computational Physics, 136(1), 214-226. [DOI:10.1006/jcph.1997.5776](https://doi.org/10.1006/jcph.1997.5776)
    - SPH pour les écoulements à faible nombre de Reynolds.

18. **Adami, S., Hu, X. Y., & Adams, N. A.** (2012). *A generalized wall boundary condition for smoothed particle hydrodynamics*. Journal of Computational Physics, 231(21), 7057-7075. [DOI:10.1016/j.jcp.2012.05.005](https://doi.org/10.1016/j.jcp.2012.05.005)
    - Conditions aux limites pour SPH.

19. **Liu, M. B., & Liu, G. R.** (2010). *Smoothed Particle Hydrodynamics (SPH): an Overview and Recent Developments*. Archives of Computational Methods in Engineering, 17, 25-76. [DOI:10.1007/s11831-010-9040-7](https://doi.org/10.1007/s11831-010-9040-7)
    - Revue des développements récents en SPH.

20. **Violeau, D.** (2012). *Fluid Mechanics and the SPH Method: Theory and Applications*. Oxford University Press. ISBN: 978-0-19-965552-6.
    - Ouvrage complet sur la méthode SPH.

---

## Rhéologie et Mouillage

21. **Barnes, H. A.** (1997). *Thixotropy—a review*. Journal of Non-Newtonian Fluid Mechanics, 70(1-2), 1-33.
    - Revue sur la thixotropie des fluides complexes.

22. **de Gennes, P. G.** (1985). *Wetting: statics and dynamics*. Reviews of Modern Physics, 57(3), 827.
    - Fondements théoriques du mouillage.

23. **Owens, R. G., & Phillips, T. N.** (2002). *Computational Rheology*. Imperial College Press.
    - Référence pour la modélisation numérique des fluides non-newtoniens.

---

## Ouvrages Généraux

24. **Basaran, O. A., Gao, H., & Bhat, P. P.** (2013). *Nonstandard inkjets*. Annual Review of Fluid Mechanics, 45, 85-113.
    - Revue complète des mécanismes d'éjection de gouttes non standards.

25. **Derby, B.** (2010). *Inkjet printing of functional and structural materials*. Annual Review of Materials Research, 40, 395-414.
    - Introduction aux applications industrielles de l'impression jet d'encre.

---

## Ressources en Ligne

- [OpenFOAM Documentation](https://openfoam.org)
- [FEniCS Project](https://fenicsproject.org)
- [Palabos](https://palabos.unige.ch)
- [PySPH Documentation](https://pysph.readthedocs.io)
- [CFD Online Forums](https://www.cfd-online.com/Forums/)
