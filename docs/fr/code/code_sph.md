# Code PySPH - Smoothed Particle Hydrodynamics (SPH)

Cette page présente l'implémentation SPH utilisant la bibliothèque **PySPH**. Le code est écrit en Python et permet de simuler la dispense d'encre avec une gestion précise des angles de contact.

---

## 1. Structure du code

Le projet utilise PySPH pour définir les équations et le solveur. La configuration est gérée par des fichiers YAML.

```
project_directory/
├── templates/
│   └── pysph/
│       └── droplet_spreading.py   # Script de simulation principal
├── config/
│   └── base_parameters.yaml       # Paramètres par défaut
├── scripts/                       # Utilitaires de visualisation
└── results/                       # Fichiers de sortie (.npz)
```

---

## 2. Configuration (`base_parameters.yaml`)

Ce fichier centralise les paramètres physiques et numériques. Il est partagé entre les simulations VOF et SPH pour assurer la cohérence.

```yaml
# config/base_parameters.yaml

sph:
  dx: 1.0e-5              # Espacement particules (10 µm)
  hdx: 1.3                # Ratio lissage/espacement
  c0: 10.0                # Vitesse du son artificielle

surface:
  sigma: 0.040            # Tension de surface (N/m)

rheology:
  eta0: 1.5               # Viscosité zéro-cisaillement
  n: 0.5                  # Indice rhéofluidifiant

contact_angles:
  substrate: 35           # Fond (hydrophile)
  wall_isolant_left: 15   # Mur gauche
```

**Points clés :**
- **dx** : définit la résolution spatiale (taille caractéristique des particules)
- **c0** : vitesse du son numérique pour le schéma WCSPH (faiblement compressible)
- **sigma** : tension de surface physique

---

## 3. Classe principale (`DropletSpreading`)

La simulation est encapsulée dans une classe dérivée de `Application` de PySPH. Elle configure le solveur, les particules et les équations.

```python
# templates/pysph/droplet_spreading.py

class DropletSpreading(Application):
    def initialize(self):
        # Paramètres par défaut
        self.dx = 1e-5
        self.rho_ink = 3000.0
        self.scheme_name = 'morris'  # Schéma de tension de surface

    def create_particles(self):
        # Création des particules fluides et solides
        # ...
        return [fluid, solid]

    def create_equations(self):
        # Définition des forces et interactions
        # ...
        return equations
```

**Points clés :**
- **Application** : gère le cycle de vie de la simulation PySPH
- **Schéma Morris** : utilisé pour la tension de surface (robuste pour les forts ratios de densité)

---

## 4. Gestion des angles de contact (`CavityAdhesionForce`)

Contrairement aux méthodes classiques, nous utilisons une force d'adhésion explicite pour imposer l'angle de contact sur les parois complexes de la cavité.

```python
class CavityAdhesionForce(Equation):
    """Applique une force d'adhésion pour imposer l'angle de contact."""

    def initialize(self, d_idx, d_x, d_y, d_h, d_au, d_av, d_scolor):
        # Application uniquement à l'interface (scolor ~ 0.5)
        if 0.05 <= d_scolor[d_idx] <= 0.95:
            # Calcul de la distance à la paroi
            dist_to_bottom = d_y[d_idx] - self.y_bottom
            
            if dist_to_bottom < self.delta * h:
                # Force proportionnelle au cosinus de l'angle de contact
                F_mag = self.alpha * self.sigma * abs(self.cos_theta) / h
                
                # Direction : étalement ou retrait selon hydrophilie
                if self.cos_theta > 0: # Hydrophile
                    d_au[d_idx] += direction * F_mag
                else: # Hydrophobe
                    d_au[d_idx] -= direction * F_mag
```

**Points clés :**
- **Force d'adhésion** : simule la tension de ligne triple
- **Géométrie complexe** : gère distinctement le fond, les murs verticaux et les plateaux
- **cos_theta** : détermine si la force favorise l'étalement (>0) ou le retrait (<0)

---

## 5. Rhéologie (Modèle Carreau)

Comme pour le LBM, la viscosité de chaque particule est ajustée dynamiquement en fonction du taux de déformation local.

```python
class CarreauViscosity(Equation):
    def loop(self, d_idx, d_nu, d_strain_rate):
        gamma_dot = d_strain_rate[d_idx]

        # Modèle de Carreau
        factor = 1.0 + (self.lam * gamma_dot)**2
        exponent = 0.5 * (self.n - 1.0)
        
        # Viscosité dynamique locale
        eta = self.eta_inf + (self.eta0 - self.eta_inf) * (factor ** exponent)

        # Conversion en viscosité cinématique
        d_nu[d_idx] = eta / self.rho0
```

**Points clés :**
- **Calcul particulaire** : chaque particule transporte sa propre viscosité
- **ComputeStrainRate** : équation préalable qui estime le tenseur de déformation $\dot{\gamma}$ via les gradients SPH

---

## 6. Création des équations (`create_equations`)

La méthode `create_equations` assemble tous les modèles physiques en groupes séquentiels.

```python
def create_equations(self):
    equations = [
        # Groupe 1 : Densité
        Group(equations=[SummationDensity(dest='fluid', sources=['fluid', 'solid'])]),

        # Groupe Rhéologie (optionnel)
        Group(equations=[
            ComputeStrainRate(...),
            CarreauViscosity(...)
        ]) if self.use_carreau else Group(),

        # Groupe Tension de Surface & Adhésion
        Group(equations=[
            MorrisColorGradient(...),
            ShadlooYildizSurfaceTensionForce(...),
            CavityAdhesionForce(...)
        ]),

        # Groupe Quantité de Mouvement
        Group(equations=[
            MomentumEquationPressureGradient(...),
            MomentumEquationViscosity(...),
        ])
    ]
    return equations
```

**Points clés :**
- **Groupes** : définissent l'ordre d'exécution des forces
- **Modularité** : permet d'activer/désactiver la rhéologie ou la géométrie de cavité
