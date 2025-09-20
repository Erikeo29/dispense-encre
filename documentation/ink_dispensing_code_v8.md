
## 4. MÉTHODE NUMÉRIQUE

### 4.1 Discrétisation spatiale

Le domaine Ω est discrétisé par éléments finis avec :
- Éléments P₂ pour la vitesse (polynômes quadratiques)
- Éléments P₁ pour la pression (polynômes linéaires)
- Éléments P₁ pour la fonction level-set

Cette combinaison (P₂-P₁) satisfait la condition inf-sup pour la stabilité.

### 4.2 Discrétisation temporelle

Schéma de Crank-Nicolson (θ = 0.5) :
$$\frac{\mathbf{v}^{n+1} - \mathbf{v}^n}{\Delta t} = \theta \mathcal{F}(\mathbf{v}^{n+1}) + (1-\theta)\mathcal{F}(\mathbf{v}^n)$$

avec Δt = 10⁻⁴ s choisi pour satisfaire CFL < 0.5 :
$$\text{CFL} = \frac{|\mathbf{v}|_{\max} \Delta t}{h} < 0.5$$

où h est la taille caractéristique de maille.

### 4.3 Algorithme de résolution

```
ALGORITHME : Simulation diphasique Phase-Field
------------------------------------------------
1. INITIALISATION
   - Créer maillage avec raffinement près de l'interface
   - Initialiser v = 0, p = 0, φ = φ₀
   
2. BOUCLE TEMPORELLE : pour t = 0 à T
   
   2.1 TRANSPORT INTERFACE
       - Résoudre équation Phase-Field pour φⁿ⁺¹
       - Réinitialiser distance signée si nécessaire
   
   2.2 MISE À JOUR PROPRIÉTÉS
       - Calculer ρ(φⁿ⁺¹), η(φⁿ⁺¹, γ̇ⁿ)
       - Calculer F_σ depuis φⁿ⁺¹
   
   2.3 RÉSOLUTION NAVIER-STOKES (algorithme SIMPLE)
       a. Prédiction vitesse v*
          Résoudre : ρ(v* - vⁿ)/Δt + ρ(vⁿ·∇)v* = -∇pⁿ + ∇·τⁿ + F
       
       b. Correction pression
          Résoudre : ∇²p' = (ρ/Δt)∇·v*
       
       c. Correction vitesse
          vⁿ⁺¹ = v* - (Δt/ρ)∇p'
          pⁿ⁺¹ = pⁿ + p'
   
   2.4 VÉRIFICATION CONVERGENCE
       - ||vⁿ⁺¹ - vⁿ||/||vⁿ|| < 10⁻⁶
       - ||∇·vⁿ⁺¹|| < 10⁻⁸
   
   2.5 CALCUL MÉTRIQUES
       - Taux de remplissage : α = ∫_Ω H(φ)dΩ / V_puit
       - Si α ≥ 0.8 : STOP
   
3. POST-TRAITEMENT
   - Export résultats (VTK/XDMF)
   - Analyse statistique
```

---

## 5. IMPLÉMENTATION PYTHON

### 5.1 Structure modulaire du code

```python
#!/usr/bin/env python3
"""
Simulation diphasique de dispense d'encre Ag/AgCl
Méthode Phase-Field avec FEniCSx
"""

import numpy as np
from mpi4py import MPI
from petsc4py import PETSc
from dolfinx import fem, mesh, io
from dolfinx.fem import Function, FunctionSpace
from ufl import (
    grad, div, inner, dx, ds, 
    TestFunction, TrialFunction, split
)

class InkDispenseSimulation:
    """
    Classe principale pour la simulation de dispense d'encre Ag/AgCl.
    
    Attributes:
        rho_ink (float): Masse volumique de l'encre [kg/m³]
        rho_air (float): Masse volumique de l'air [kg/m³]
        mu_0 (float): Viscosité au repos [Pa·s]
        mu_inf (float): Viscosité à cisaillement infini [Pa·s]
        lambda_c (float): Temps de relaxation de Carreau [s]
        n_carreau (float): Indice de pseudoplasticité [-]
        sigma (float): Tension de surface [N/m]
        epsilon (float): Épaisseur interface [m]
    """
    
    def __init__(self, config_file=None):
        """Initialisation avec paramètres physiques."""
        
        # Propriétés Phase 1 : Encre Ag/AgCl
        self.rho_ink = 2200.0      # kg/m³
        self.mu_0 = 1.5            # Pa·s
        self.mu_inf = 0.05         # Pa·s  
        self.lambda_c = 0.15       # s
        self.n_carreau = 0.7       # -
        
        # Propriétés Phase 2 : Air
        self.rho_air = 1.2         # kg/m³
        self.mu_air = 1e-5         # Pa·s
        
        # Propriétés interfaciales
        self.sigma = 0.04          # N/m
        self.epsilon = 5e-6        # m
        self.gamma_mob = 1.0       # mobilité
        
        # Géométrie [m]
        self.D_well = 0.8e-3       # diamètre puit
        self.h_well = 0.128e-3     # hauteur puit
        self.D_needle = 0.2e-3     # diamètre seringue
        self.gap = 30e-6           # distance seringue-puit
        
        # Angles de contact [rad]
        self.theta_gold = np.radians(145)
        self.theta_left = np.radians(145)  
        self.theta_right = np.radians(90)
        self.theta_top = np.radians(0)
        
        # Paramètres numériques
        self.dt = 1e-4             # pas de temps [s]
        self.T_final = 0.1         # temps final [s]
        self.tol = 1e-6            # tolérance convergence
        
    def carreau_viscosity(self, shear_rate):
        """
        Modèle de viscosité de Carreau.
        
        Args:
            shear_rate: Taux de cisaillement [s⁻¹]
            
        Returns:
            eta: Viscosité dynamique [Pa·s]
        """
        eta = (self.mu_inf + 
               (self.mu_0 - self.mu_inf) * 
               (1 + (self.lambda_c * shear_rate)**2)**((self.n_carreau - 1)/2))
        return eta
    
    def create_mesh(self, nx=80, ny=20):
        """
        Création du maillage 2D axisymétrique.
        
        Args:
            nx: Nombre d'éléments selon x
            ny: Nombre d'éléments selon y
            
        Returns:
            domain: Objet maillage Dolfinx
        """
        domain = mesh.create_rectangle(
            MPI.COMM_WORLD,
            [np.array([0, 0]), 
             np.array([self.D_well/2, self.h_well])],
            [nx, ny],
            cell_type=mesh.CellType.triangle
        )
        return domain
    
    def setup_function_spaces(self, domain):
        """
        Définition des espaces fonctionnels P2-P1.
        
        Args:
            domain: Maillage
            
        Returns:
            W: Espace mixte [vitesse, pression, level-set]
        """
        from basix.ufl import element, mixed_element
        
        # Éléments P2 pour vitesse
        P2 = element("Lagrange", domain.topology.cell_name(), 2, 
                     shape=(domain.geometry.dim,))
        # Éléments P1 pour pression et level-set
        P1 = element("Lagrange", domain.topology.cell_name(), 1)
        
        # Espace mixte
        ME = mixed_element([P2, P1, P1])
        W = FunctionSpace(domain, ME)
        
        return W
    
    def weak_form(self, u, v, p, q, phi, psi, u_n, p_n, phi_n):
        """
        Formulation variationnelle faible du système couplé.
        
        Args:
            u, v: Vitesse et fonction test
            p, q: Pression et fonction test
            phi, psi: Level-set et fonction test
            u_n, p_n, phi_n: Solutions au pas de temps précédent
            
        Returns:
            F: Forme variationnelle complète
        """
        # Tenseur des déformations
        def epsilon(u):
            return 0.5 * (grad(u) + grad(u).T)
        
        # Taux de cisaillement
        def shear_rate(u):
            return (2 * inner(epsilon(u), epsilon(u)))**0.5
        
        # Fonction Heaviside régularisée
        def H(phi):
            return 0.5 * (1 + phi)
        
        # Propriétés du mélange
        rho = self.rho_ink * H(phi) + self.rho_air * (1 - H(phi))
        eta = self.carreau_viscosity(shear_rate(u)) * H(phi) + \
              self.mu_air * (1 - H(phi))
        
        # Normale et courbure
        n = grad(phi) / (inner(grad(phi), grad(phi))**0.5 + 1e-10)
        kappa = div(n)
        
        # Force de tension de surface
        F_sigma = self.sigma * kappa * abs(grad(phi)) * n
        
        # Forme variationnelle Navier-Stokes
        F_ns = (
            # Terme instationnaire
            rho * inner((u - u_n)/self.dt, v) * dx +
            # Terme convectif
            rho * inner(grad(u) * u_n, v) * dx +
            # Terme de pression
            inner(grad(p), v) * dx - 
            # Terme visqueux
            2 * eta * inner(epsilon(u), epsilon(v)) * dx +
            # Contrainte d'incompressibilité
            div(u) * q * dx +
            # Force de tension de surface
            inner(F_sigma, v) * dx
        )
        
        # Forme variationnelle Phase-Field
        F_pf = (
            # Transport
            inner((phi - phi_n)/self.dt + grad(phi) * u_n, psi) * dx +
            # Diffusion
            self.gamma_mob * self.epsilon * inner(grad(phi), grad(psi)) * dx
        )
        
        return F_ns + F_pf
    
    def apply_boundary_conditions(self, W, t):
        """
        Application des conditions aux limites.
        
        Args:
            W: Espace fonctionnel
            t: Temps actuel [s]
            
        Returns:
            bcs: Liste des conditions de Dirichlet
        """
        from dolfinx.fem import dirichletbc, locate_dofs_topological
        
        bcs = []
        
        # Non-glissement sur les parois
        # ... (implémentation détaillée)
        
        # Vitesse d'entrée (seringue)
        # ... (implémentation détaillée)
        
        # Angle de contact
        # ... (implémentation détaillée)
        
        return bcs
    
    def solve(self):
        """
        Boucle de résolution temporelle principale.
        """
        # Création du maillage
        domain = self.create_mesh()
        W = self.setup_function_spaces(domain)
        
        # Initialisation
        w = Function(W)
        w_n = Function(W)
        
        # Extraction des composantes
        u, p, phi = split(w)
        u_n, p_n, phi_n = split(w_n)
        
        # Fonctions test
        v, q, psi = TestFunctions(W)
        
        # Formulation variationnelle
        F = self.weak_form(u, v, p, q, phi, psi, u_n, p_n, phi_n)
        
        # Boucle temporelle
        t = 0.0
        step = 0
        
        while t < self.T_final:
            t += self.dt
            step += 1
            
            # Conditions aux limites
            bcs = self.apply_boundary_conditions(W, t)
            
            # Résolution non-linéaire (Newton)
            problem = fem.NonlinearProblem(F, w, bcs)
            solver = fem.NewtonSolver(MPI.COMM_WORLD, problem)
            solver.convergence_criterion = "incremental"
            solver.rtol = self.tol
            
            # Résolution
            n_iter, converged = solver.solve(w)
            
            if not converged:
                print(f"Pas de convergence à t = {t:.6f} s")
                break
            
            # Mise à jour solution
            w_n.x.array[:] = w.x.array
            
            # Calcul du taux de remplissage
            fill_ratio = self.compute_fill_ratio(phi)
            
            # Affichage
            if step % 10 == 0:
                print(f"t = {t:.4f} s | "
                      f"Itérations: {n_iter} | "
                      f"Remplissage: {fill_ratio:.1%}")
            
            # Critère d'arrêt
            if fill_ratio >= 0.8:
                print(f"\nObjectif atteint!")
                print(f"Temps de remplissage: {t:.3f} s")
                print(f"Taux de remplissage: {fill_ratio:.1%}")
                break
        
        return w
    
    def compute_fill_ratio(self, phi):
        """
        Calcul du taux de remplissage du puit.
        
        Args:
            phi: Fonction level-set
            
        Returns:
            ratio: Fraction volumique d'encre [-]
        """
        from dolfinx.fem import assemble_scalar
        
        # Intégration de H(phi) sur le domaine
        H_phi = 0.5 * (1 + phi)
        volume_ink = assemble_scalar(H_phi * dx)
        volume_total = self.D_well**2 * np.pi/4 * self.h_well
        
        return volume_ink / volume_total
    
    def post_process(self, w, filename="results"):
        """
        Post-traitement et export des résultats.
        
        Args:
            w: Solution finale
            filename: Nom de base des fichiers de sortie
        """
        u, p, phi = w.split()
        
        # Export VTK/XDMF pour Paraview
        with io.XDMFFile(MPI.COMM_WORLD, f"{filename}.xdmf", "w") as file:
            file.write_mesh(u.function_space.mesh)
            file.write_function(u, "velocity")
            file.write_function(p, "pressure")
            file.write_function(phi, "level_set")
        
        print(f"Résultats exportés : {filename}.xdmf")

# Point d'entrée principal
if __name__ == "__main__":
    print("=" * 60)
    print("SIMULATION DISPENSE ENCRE Ag/AgCl")
    print("Méthode Phase-Field - FEniCSx")
    print("=" * 60)
    
    # Lancement simulation
    sim = InkDispenseSimulation()
    solution = sim.solve()
    sim.post_process(solution)
    
    print("\nSimulation terminée avec succès!")
```
