# Modélisation de la dispense d'encre dans un puit
## Approche par simulation diphasique en domaine microfluidique

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

