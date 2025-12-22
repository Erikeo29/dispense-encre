# Méthode Lattice Boltzmann (LBM)

La méthode LBM ne résout pas directement les équations de Navier-Stokes (macro-échelle), mais l'équation de Boltzmann discrète sur un réseau (Lattice).

On suit l'évolution de fonctions de distribution de particules $f_i(\mathbf{x}, t)$ qui se déplacent selon des directions discrètes $c_i$ et entrent en collision.

$$
f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = \Omega_i(f)
$$

Les grandeurs macroscopiques (densité $\rho$, vitesse $\mathbf{u}$) sont retrouvées par des moments statistiques de $f_i$.

### Bibliothèque Utilisée : Palabos

**Palabos** (Parallel Lattice Boltzmann Solver) est une bibliothèque open-source de référence, écrite en C++.
*   **Architecture :** Orientée objet, conçue dès le départ pour le calcul parallèle massif (MPI).
*   **Performance :** Excellente scalabilité sur clusters CPU.
*   **Alternatives :** **OpenLB** (plus ingénierie), **Walberla** (HPC extrême), **Sailfish** (GPU Python).

### Modèle Multiphasique : Shan-Chen (Pseudopotentiel)

Pour simuler l'encre et l'air, nous utilisons le modèle de **Shan-Chen**.

*   **Principe :** Les fluides interagissent via une force interparticulaire à courte portée, calculée à partir d'un "pseudopotentiel" $\psi(\mathbf{x})$ qui dépend de la densité locale.
    $$
    \mathbf{F}_{int}(\mathbf{x}) = -G \psi(\mathbf{x}) \sum_{i} w_i \psi(\mathbf{x} + \mathbf{c}_i \Delta t) \mathbf{c}_i
    $$
*   **Séparation de Phase :** Cette force d'interaction provoque une séparation spontanée des phases (comme l'eau et l'huile) sans avoir besoin de suivre explicitement l'interface.
*   **Mouillage :** Les angles de contact sur les parois solides sont gérés en assignant une densité fictive (ou un potentiel) aux nœuds solides, ce qui attire ou repousse le fluide naturellement. C'est un énorme avantage pour les géométries complexes comme les micro-puits.
