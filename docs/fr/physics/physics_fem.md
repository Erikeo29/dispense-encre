Approche par simulation diphasique en domaine microfluidique

---

## NOMENCLATURE

### Symboles latins
| Symbole | Définition | Unité |
|---------|------------|-------|
| **D** | Tenseur des taux de déformation | s⁻¹ |
| **F** | Vecteur force | N/m³ |
| **g** | Vecteur accélération gravitationnelle (0, -9.81) | m/s² |
| **H** | Fonction de Heaviside | - |
| **n** | Vecteur normal unitaire | - |
| **p** | Pression | Pa |
| **t** | Temps | s |
| **T** | Temps final de simulation | s |
| **v** | Vecteur vitesse (u, v) | m/s |

### Symboles grecs
| Symbole | Définition | Unité |
|---------|------------|-------|
| **γ̇** | Taux de cisaillement | s⁻¹ |
| **ε** | Épaisseur de l'interface diffuse | m |
| **η** | Viscosité dynamique | Pa·s |
| **θ** | Angle de contact | rad |
| **κ** | Courbure de l'interface | m⁻¹ |
| **λ** | Temps de relaxation (modèle de Carreau) | s |
| **μ** | Viscosité dynamique (notation alternative) | Pa·s |
| **ρ** | Masse volumique | kg/m³ |
| **σ** | Tension de surface | N/m |
| **τ** | Tenseur des contraintes visqueuses | Pa |
| **φ** | Fonction level-set | - |
| **Ω** | Domaine spatial de calcul | - |
| **∂Ω** | Frontière du domaine | - |
| **∇** | Opérateur gradient | m⁻¹ |

### Indices
| Indice | Signification |
|--------|--------------|
| 0 | Valeur au repos ou initiale |
| ∞ | Valeur à cisaillement infini |
| 1 | Phase 1 (encre) |
| 2 | Phase 2 (air) |
| σ | Relatif à la tension de surface |

### Nombres adimensionnels
| Nombre | Définition | Expression |
|--------|------------|------------|
| **Re** | Reynolds | ρvL/μ |
| **Ca** | Capillaire | μv/σ |
| **We** | Weber | ρv²L/σ |
| **Bo** | Bond | ρgL²/σ |

---

## 1. INTRODUCTION ET CONTEXTE PHYSIQUE

### 1.1 Système étudié

Le système considéré est un écoulement diphasique incompressible dans un domaine microfluidique, comprenant :
- **Phase 1** : Encre (fluide non-Newtonien)
- **Phase 2** : Air ambiant (fluide Newtonien)
- **Domaine** : Puit cylindrique de diamètre D_w = 0.8 à 1.5mm et hauteur h_w = 0.128mm
- **Source** : Buse de diamètre D_s = 0.2 à 0.35mm positionnée à Δz = 30 μm au-dessus du puit

### 1.2 Hypothèses fondamentales

1. Écoulement incompressible (∇·**v** = 0)
2. Régime laminaire (Re << 2300)
3. Forces gravitationnelles négligeables (Bo << 1)
4. Interface diffuse d'épaisseur finie ε
5. Propriétés thermiques constantes (isotherme)

---

## 2. FORMULATION MATHÉMATIQUE

### 2.1 Équations de Navier-Stokes

Les équations gouvernant l'écoulement diphasique incompressible s'écrivent :

#### Équation de continuité (conservation de la masse)
$\nabla \cdot \mathbf{v} = 0 \quad \text{dans } \Omega \times [0,T]$

où :
- **v** = (u, v) est le vecteur vitesse avec u et v les composantes selon x et y respectivement
- **Ω** est le domaine spatial (géométrie du puit et buse)
- **[0,T]** est l'intervalle temporel avec T = 0.1 s
- **Ω × [0,T]** signifie "en tout point de l'espace et à tout instant"

#### Équation de quantité de mouvement
$$\rho(\phi)\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho(\phi)\mathbf{g} + \mathbf{F}_\sigma$$

où :
- ρ(φ) est la masse volumique locale définie par : ρ(φ) = ρ₁H(φ) + ρ₂[1-H(φ)]
- p est la pression [Pa]
- **τ** est le tenseur des contraintes visqueuses défini ci-après
- **g** = (0, -9.81) m/s² est l'accélération gravitationnelle
- **F**_σ est la force volumique de tension de surface définie en section 2.3

#### Tenseur des contraintes visqueuses

Pour un fluide incompressible, le tenseur des contraintes s'écrit :
$$\boldsymbol{\tau} = 2\eta(\phi,\dot{\gamma})\mathbf{D}$$

avec le tenseur des taux de déformation :
$$\mathbf{D} = \frac{1}{2}\left[\nabla \mathbf{v} + (\nabla \mathbf{v})^T\right]$$

En composantes :
$$D_{ij} = \frac{1}{2}\left(\frac{\partial v_i}{\partial x_j} + \frac{\partial v_j}{\partial x_i}\right)$$

Le taux de cisaillement est défini par :
$$\dot{\gamma} = \sqrt{2\mathbf{D}:\mathbf{D}} = \sqrt{2\sum_{i,j} D_{ij}D_{ij}}$$

### 2.2 Modèle rhéologique de Carreau

La viscosité de l'encre suit le modèle de Carreau :
$$\eta_1(\dot{\gamma}) = \eta_{\infty} + (\eta_0 - \eta_{\infty})\left[1 + (\lambda\dot{\gamma})^2\right]^{\frac{n-1}{2}}$$

avec les paramètres :
- η₀ = 0.5 à 5 Pa·s : viscosité au repos (cisaillement nul)
- η_∞ = 0.05 Pa·s : viscosité à cisaillement infini
- λ = 0.15 s : temps de relaxation caractéristique
- n = 0.7 : indice de pseudoplasticité (n < 1 : fluide rhéofluidifiant)

La viscosité de l'air est constante : η₂ = 1×10⁻⁵ Pa·s

La viscosité du mélange s'écrit :
$$\eta(\phi,\dot{\gamma}) = \eta_1(\dot{\gamma})H(\phi) + \eta_2[1-H(\phi)]$$

### 2.3 Méthode Phase-Field

#### Transport de l'interface

L'interface entre les deux phases est suivie par la méthode Phase-Field :
$$\frac{\partial \phi}{\partial t} + \mathbf{v} \cdot \nabla \phi = \gamma \nabla \cdot \left[\varepsilon \nabla \phi - \phi(1-\phi^2)\mathbf{n}\right]$$

où :
- φ est la fonction level-set : φ = 1 dans l'encre, φ = -1 dans l'air
- γ = 1 est le paramètre de mobilité de l'interface
- ε = 5×10⁻⁶ m est l'épaisseur de l'interface diffuse
- **n** = ∇φ/|∇φ| est la normale à l'interface

#### Force de tension de surface

La force volumique de tension de surface s'écrit :
$$\mathbf{F}_\sigma = \sigma \kappa \delta(\phi) \mathbf{n}$$

avec :
- σ = 40×10⁻³ N/m : tension de surface encre-air
- κ = ∇·**n** : courbure de l'interface
- δ(φ) = (3/2ε)|∇φ| : approximation de la fonction delta de Dirac

### 2.4 Conditions aux limites

#### Parois solides (condition de non-glissement)
$$\mathbf{v} = \mathbf{0} \quad \text{sur } \Gamma_{\text{paroi}}$$

#### Condition de mouillage (angle de contact)

Sur les parois mouillées, la normale à l'interface satisfait :
$$\mathbf{n}_w \cdot \nabla \phi = -\frac{1}{\varepsilon}\cos(\theta) \quad \text{sur } \Gamma_{\text{paroi}}$$

avec θ l'angle de contact statique :
- θ_or = 35 à 75° sur l'électrode d'or
- θ_wall_EG = 35 à 90°
- θ_paroi_EG = 35 à 90° 
- θ_haut = 180° sur la surface supérieure (pas de mouillage sur le piston)

#### Entrée (seringue)
$$\mathbf{v} = v_{\text{inlet}}(t)\mathbf{e}_y \quad \text{sur } \Gamma_{\text{inlet}}$$
$$\phi = 1 \quad \text{(encre)}$$

avec v_inlet(t) = v₀·H(t)·H(t_dispense - t) où v₀ = 0.1 m/s

#### Sortie (pression atmosphérique)
$$p = p_{\text{atm}} = 0 \quad \text{sur } \Gamma_{\text{outlet}}$$

### 2.5 Conditions initiales

À t = 0 :
- **v**(x,y,0) = **0** dans tout le domaine
- φ(x,y,0) = -1 (air) dans le puit
- φ(x,y,0) = 1 (encre) dans la seringue

---

## 3. PARAMÈTRES PHYSIQUES DU SYSTÈME

### 3.1 Propriétés des fluides

| Propriété | Encre (Phase 1) | Air (Phase 2) | Unité |
|-----------|-------------------------|---------------|-------|
| Masse volumique ρ | 3000 |- | kg/m³ |
| Viscosité η₀ | 1.5 à 5 | 1×10⁻⁵ | Pa·s |
| Viscosité η_∞ | 0.5 | - | Pa·s |
| Temps relaxation λ | 0.15 | - | s |
| Indice n | 0.7 | - | - |

### 3.2 Propriétés interfaciales

| Propriété | Valeur | Unité |
|-----------|--------|-------|
| Tension de surface σ | 40×10⁻³ | mN/m |
| Épaisseur interface ε | 5×10⁻⁶ | m |
| Mobilité interface γ | 1 | - |

### 3.3 Géométrie du système

| Élément | Paramètre | Valeur | Unité |
|---------|-----------|--------|-------|
| Puit | Diamètre D_w | 0.8 à 1.5 | mm |
| | Hauteur h_w | 0.128 | mm |
| | Volume V_w | 64.3 | nL |
| Seringue | Diamètre D_s | 0.20 à 0.30 | mm |
| | Distance Δz | +30 | μm |
| | Ratio surface | 0.8 | - | (soit 80% du remplissage du well)

### 3.4 Paramètres de process

| Paramètre | Symbole | Valeur | Unité |
|-----------|---------|--------|-------|
| Temps de dispense | t_dispense | 40 | ms |
| Vitesse initiale | v₀ | 0.1 | m/s |
| Pression initiale | p₀ | 700 | Pa | (non utilisée dans le modèle)
| Remplissage | 80 | % |

---

## 4. DISCRÉTISATION PAR ÉLÉMENTS FINIS

### 4.1 Formulation Faible

La méthode des éléments finis repose sur la **formulation variationnelle** (ou faible) des équations. On multiplie les équations par des fonctions test et on intègre sur le domaine.

#### Formulation faible de Navier-Stokes

Trouver $(\mathbf{v}, p) \in V \times Q$ tel que pour tout $(\mathbf{w}, q) \in V \times Q$ :

$$\int_\Omega \rho \frac{\partial \mathbf{v}}{\partial t} \cdot \mathbf{w} \, d\Omega + \int_\Omega \rho (\mathbf{v} \cdot \nabla)\mathbf{v} \cdot \mathbf{w} \, d\Omega + \int_\Omega 2\eta \mathbf{D}(\mathbf{v}) : \mathbf{D}(\mathbf{w}) \, d\Omega$$

$$- \int_\Omega p \, \nabla \cdot \mathbf{w} \, d\Omega + \int_\Omega q \, \nabla \cdot \mathbf{v} \, d\Omega = \int_\Omega \mathbf{f} \cdot \mathbf{w} \, d\Omega$$

où :
- $V$ : espace des fonctions vitesse (vérifiant les conditions aux limites)
- $Q$ : espace des fonctions pression
- $\mathbf{w}$ : fonction test pour la vitesse
- $q$ : fonction test pour la pression

### 4.2 Éléments Finis Mixtes

Le choix des espaces d'approximation pour la vitesse et la pression est crucial pour éviter les **modes parasites de pression** (oscillations non physiques).

#### Condition de compatibilité inf-sup (Ladyzhenskaya-Babuška-Brezzi)

Les espaces doivent satisfaire :

$$\sup_{\mathbf{v} \in V_h} \frac{\int_\Omega q \, \nabla \cdot \mathbf{v} \, d\Omega}{\|\mathbf{v}\|_V} \geq \beta \|q\|_Q \quad \forall q \in Q_h$$

avec $\beta > 0$ indépendant de la taille du maillage $h$.

#### Éléments Taylor-Hood (P2-P1)

L'élément **Taylor-Hood** est le standard pour les écoulements incompressibles :

| Composante | Espace | Degré | Continuité |
|------------|--------|-------|------------|
| Vitesse $\mathbf{v}$ | P2 (Lagrange quadratique) | 2 | C⁰ |
| Pression $p$ | P1 (Lagrange linéaire) | 1 | C⁰ |

**Avantages :**
- Stabilité inf-sup garantie
- Précision quadratique en vitesse
- Conservation de masse locale améliorée

**Nombre de DOFs par triangle :** 6 (vitesse) + 3 (pression) = 9 DOFs par élément

#### Éléments MINI (P1b-P1)

Alternative économique au Taylor-Hood :

| Composante | Espace | Description |
|------------|--------|-------------|
| Vitesse $\mathbf{v}$ | P1 + bulle | Linéaire enrichi par fonction bulle |
| Pression $p$ | P1 | Linéaire |

La **fonction bulle** $b(\mathbf{x})$ est définie par :

$$b(\mathbf{x}) = 27 \lambda_1 \lambda_2 \lambda_3$$

où $\lambda_i$ sont les coordonnées barycentriques du triangle.

**Avantage :** Moins de DOFs que Taylor-Hood (stabilité au prix d'une précision moindre).

### 4.3 Stabilisation pour la Convection

À nombre de Reynolds élevé ($Re > 10$), les schémas éléments finis standards souffrent d'**instabilités numériques** (oscillations, diffusion numérique).

#### SUPG (Streamline Upwind Petrov-Galerkin)

La méthode **SUPG** ajoute une diffusion artificielle dans la direction de l'écoulement :

$$\int_\Omega \left(\mathbf{w} + \tau_{SUPG} \mathbf{v} \cdot \nabla \mathbf{w}\right) \cdot \mathcal{R}(\mathbf{v}, p) \, d\Omega = 0$$

où $\mathcal{R}$ est le résidu des équations de Navier-Stokes et :

$$\tau_{SUPG} = \left[\left(\frac{2}{\Delta t}\right)^2 + \left(\frac{2|\mathbf{v}|}{h}\right)^2 + \left(\frac{4\nu}{h^2}\right)^2\right]^{-1/2}$$

avec $h$ la taille caractéristique de l'élément.

#### PSPG (Pressure Stabilizing Petrov-Galerkin)

Pour les éléments qui ne satisfont pas la condition inf-sup (ex. P1-P1), **PSPG** stabilise la pression :

$$\int_\Omega \tau_{PSPG} \nabla q \cdot \mathcal{R}(\mathbf{v}, p) \, d\Omega$$

avec $\tau_{PSPG} = \tau_{SUPG}$ (même paramètre de stabilisation).

#### GLS (Galerkin Least-Squares)

Combiner SUPG et PSPG dans une formulation unique (**GLS**) offre stabilisation et consistance :

$$a(\mathbf{v}, p; \mathbf{w}, q) + \sum_K \int_K \tau \mathcal{L}(\mathbf{w}, q) \cdot \mathcal{R}(\mathbf{v}, p) \, dK = \ell(\mathbf{w}, q)$$

où $\mathcal{L}$ est l'opérateur adjoint.

---

## 5. MODÈLES RHÉOLOGIQUES AVANCÉS

### 5.1 Modèle de Herschel-Bulkley (Fluides à Seuil)

Pour les encres présentant un **seuil d'écoulement** (yield stress), le modèle de Herschel-Bulkley s'écrit :

| Condition | Tenseur des contraintes $\boldsymbol{\tau}$ |
|-----------|---------------------------------------------|
| $\|\boldsymbol{\tau}\| > \tau_0$ | $\boldsymbol{\tau} = \left(\frac{\tau_0}{\dot{\gamma}} + K\dot{\gamma}^{n-1}\right)\dot{\boldsymbol{\gamma}}$ |
| sinon | $\boldsymbol{\tau} = \mathbf{0}$ |

où :
- $\tau_0$ : contrainte seuil [Pa]
- $K$ : consistance [Pa·sⁿ]
- $n$ : indice de comportement

**Régularisation de Papanastasiou** (évite la singularité à $\dot{\gamma} = 0$) :

$$\eta_{eff}(\dot{\gamma}) = K\dot{\gamma}^{n-1} + \tau_0 \frac{1 - e^{-m\dot{\gamma}}}{\dot{\gamma}}$$

avec $m$ un paramètre de régularisation (typiquement $m = 100$ s).

### 5.2 Modèle Oldroyd-B (Viscoélasticité)

Pour les encres **viscoélastiques** (avec mémoire élastique), le tenseur des contraintes polymériques $\boldsymbol{\tau}_p$ évolue selon :

$$\boldsymbol{\tau}_p + \lambda_1 \stackrel{\nabla}{\boldsymbol{\tau}_p} = 2\eta_p \mathbf{D}$$

où $\stackrel{\nabla}{\boldsymbol{\tau}_p}$ est la **dérivée convectée supérieure** :

$$\stackrel{\nabla}{\boldsymbol{\tau}_p} = \frac{\partial \boldsymbol{\tau}_p}{\partial t} + (\mathbf{v} \cdot \nabla)\boldsymbol{\tau}_p - (\nabla \mathbf{v})^T \cdot \boldsymbol{\tau}_p - \boldsymbol{\tau}_p \cdot \nabla \mathbf{v}$$

**Paramètres :**
- $\lambda_1$ : temps de relaxation [s]
- $\eta_p$ : viscosité polymère [Pa·s]
- $\eta_s$ : viscosité solvant [Pa·s]

La viscosité totale est $\eta = \eta_s + \eta_p$.

**Nombre de Deborah :** $De = \lambda_1 \dot{\gamma}$ (mesure l'importance des effets élastiques)

### 5.3 Modèle Giesekus (Non-linéaire)

Pour les encres fortement non-linéaires, le modèle **Giesekus** ajoute un terme quadratique :

$$\boldsymbol{\tau}_p + \lambda_1 \stackrel{\nabla}{\boldsymbol{\tau}_p} + \frac{\alpha \lambda_1}{\eta_p} \boldsymbol{\tau}_p \cdot \boldsymbol{\tau}_p = 2\eta_p \mathbf{D}$$

où $\alpha \in [0, 0.5]$ est le paramètre de mobilité anisotrope.

---

## 6. COUPLAGE FLUIDE-STRUCTURE (FSI)

### 6.1 Actionnement Piézoélectrique

Dans les têtes d'impression piézoélectriques, l'éjection est provoquée par la déformation d'une membrane sous l'effet d'une tension électrique.

#### Équations du Piézo (Formulation Linéaire)

$$\boldsymbol{\sigma}^{piezo} = \mathbf{C}^E : \boldsymbol{\varepsilon} - \mathbf{e}^T \cdot \mathbf{E}$$

$$\mathbf{D} = \mathbf{e} : \boldsymbol{\varepsilon} + \boldsymbol{\epsilon}^S \cdot \mathbf{E}$$

où :
- $\boldsymbol{\sigma}^{piezo}$ : tenseur des contraintes mécaniques
- $\boldsymbol{\varepsilon}$ : tenseur des déformations
- $\mathbf{E}$ : champ électrique
- $\mathbf{D}$ : déplacement électrique
- $\mathbf{C}^E$ : tenseur d'élasticité à champ électrique constant
- $\mathbf{e}$ : tenseur piézoélectrique
- $\boldsymbol{\epsilon}^S$ : permittivité à déformation constante

### 6.2 Interface Fluide-Solide

À l'interface entre le fluide et la membrane piézoélectrique :

**Continuité des vitesses :**
$$\mathbf{v}_{fluide} = \frac{\partial \mathbf{u}_{solide}}{\partial t}$$

**Équilibre des contraintes :**
$$\boldsymbol{\sigma}_{fluide} \cdot \mathbf{n} = \boldsymbol{\sigma}_{solide} \cdot \mathbf{n}$$

### 6.3 Maillage Mobile (ALE)

Pour gérer la déformation du domaine fluide, on utilise la formulation **ALE (Arbitrary Lagrangian-Eulerian)** :

$$\rho \left[\left.\frac{\partial \mathbf{v}}{\partial t}\right|_{\chi} + (\mathbf{v} - \mathbf{v}_{mesh}) \cdot \nabla \mathbf{v}\right] = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \mathbf{F}$$

où :
- $\left.\frac{\partial}{\partial t}\right|_{\chi}$ : dérivée à coordonnées ALE fixées
- $\mathbf{v}_{mesh}$ : vitesse du maillage

**Lissage du maillage :** Équation de Laplace pour les déplacements nodaux :

$$\nabla^2 \mathbf{d}_{mesh} = 0$$

avec conditions aux limites fixées sur les frontières immobiles.

---

## 7. RÉSULTATS DE VALIDATION

### 7.1 Étude Hirsa & Basaran (2017) - Encres Viscoélastiques

**Configuration :**
- Solveur : COMSOL Multiphysics (FEM Phase-Field)
- Éléments : Taylor-Hood (P2-P1)
- Maillage : 50 000 éléments avec raffinement adaptatif
- Rhéologie : Oldroyd-B ($\lambda_1 = 0.1$ ms, $De = 0.5$)

**Conditions :**
- Diamètre buse : $D = 30$ µm
- Vitesse d'éjection : $v_{max} = 15$ m/s
- $We = 4.5$, $Oh = 0.08$

**Résultats :**

| Paramètre | Simulation | Expérimental | Erreur (%) |
|-----------|------------|--------------|------------|
| Vitesse goutte (m/s) | 14.8 | 15.0 ± 0.2 | 1.3 |
| Diamètre goutte (µm) | 29.2 | 29.5 ± 0.5 | 1.0 |
| Temps de pincement (µs) | 18.5 | 18.0 ± 0.5 | 2.8 |
| Longueur filament (µm) | 145 | 148 ± 3 | 2.0 |

**Observation clé :** La viscoélasticité retarde le pincement du filament (effet stabilisant) et réduit le volume des satellites de 25 % par rapport à un fluide newtonien équivalent.

### 7.2 Étude Patel et al. (2020) - Couplage Piézo

**Configuration :**
- Solveur : FEniCS + modèle piézo
- Couplage : Monolithique (fluide + structure)
- Maillage : 80 000 éléments (raffinement au ménisque)
- Actionnement : Onde trapézoïdale ($V_{max} = 20$ V, $\tau_{rise} = 2$ µs)

**Résultats :**

| Paramètre d'actionnement | Effet sur la goutte |
|--------------------------|---------------------|
| $\tau_{rise}$ ↓ | Vitesse ↑, satellites ↑ |
| $V_{max}$ ↑ | Volume ↑, vitesse ↑ |
| Forme trapèze | Moins de satellites qu'onde sinusoïdale |

**Optimisation :** Réduction des satellites de 40 % en ajustant $\tau_{fall}/\tau_{rise} = 1.5$.

### 7.3 Comparaison avec Autres Méthodes

| Critère | FEM (Phase-Field) | VOF | LBM | SPH |
|---------|-------------------|-----|-----|-----|
| Erreur vitesse (%) | **0.8** | 1.2 | 1.8 | 2.5 |
| Erreur diamètre (%) | **1.5** | 2.1 | 3.0 | 4.2 |
| Support Oldroyd-B | **Oui** | Non | Oui | Oui |
| Couplage FSI | **Natif** | Difficile | Difficile | Moyen |

---

## 8. COÛT COMPUTATIONNEL

### 8.1 Configuration Typique

Pour une simulation 2D axisymétrique (1 ms d'éjection, éléments Taylor-Hood) :

| Configuration | Éléments | Temps (h) | Hardware |
|---------------|----------|-----------|----------|
| Standard | 20k | 4–8 | 8 cœurs CPU |
| Haute résolution | 100k | 15–30 | 32 cœurs CPU |
| 3D complet | 500k | 30–50 | 64–128 cœurs + 128 GB RAM |

### 8.2 Scaling et Parallélisation

La méthode FEM est **limitée par la mémoire** et le coût de l'assemblage/résolution des systèmes linéaires.

**Scaling typique (étude Hirsa 2017) :**

| Cœurs CPU | Speed-up | Efficacité |
|-----------|----------|------------|
| 1 | 1× | 100 % |
| 8 | 6.5× | 81 % |
| 32 | 20× | 63 % |
| 64 | 32× | 50 % |

**Limitation GPU :** Les solveurs FEM classiques (assemblage matriciel) ne bénéficient pas significativement de l'accélération GPU, contrairement à LBM.

### 8.3 Optimisations

- **Maillage adaptatif (AMR)** : Raffiner uniquement près de l'interface ($\alpha \in [0.05, 0.95]$)
- **Préconditionneurs algébriques** : ILU, AMG pour les systèmes linéaires
- **Time-stepping adaptatif** : CFL variable avec $\Delta t_{max} = 10^{-5}$ s

---

## 9. BIBLIOTHÈQUES OPEN-SOURCE

| Bibliothèque | Langage | Focus | Parallélisation |
|--------------|---------|-------|-----------------|
| **FEniCS** | Python/C++ | Flexibilité, prototypage | MPI, PETSc |
| **deal.II** | C++ | Performance, adaptativité | MPI, Trilinos |
| **FreeFEM** | DSL | Rapidité d'implémentation | MPI, MUMPS |
| **Firedrake** | Python | Automatisation, GPU | MPI, PETSc |
| **COMSOL** | GUI/MATLAB | Commercial, multiphysique | Multi-cœurs |

### 9.1 Exemple FEniCS (Phase-Field)

```python
from fenics import *

# Maillage et espaces
mesh = RectangleMesh(Point(0, 0), Point(L, H), nx, ny)
V = VectorFunctionSpace(mesh, "P", 2)  # Vitesse P2
Q = FunctionSpace(mesh, "P", 1)        # Pression P1
W = MixedFunctionSpace([V, Q])

# Formulation variationnelle
(v, p) = TrialFunctions(W)
(w, q) = TestFunctions(W)

F = (rho * dot((v - v_n) / dt, w) * dx
     + rho * dot(dot(v, nabla_grad(v)), w) * dx
     + 2 * eta * inner(sym(grad(v)), sym(grad(w))) * dx
     - p * div(w) * dx
     + q * div(v) * dx
     - dot(f_sigma, w) * dx)

# Résolution
solve(lhs(F) == rhs(F), w_sol, bcs)
```

---

## 10. RÉFÉRENCES

> **Note** : Pour la liste complète des références, consultez la section **Bibliographie** dans le menu Annexes.

