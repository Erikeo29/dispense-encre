<div style="font-size: 0.9em; line-height: 1.3; background: #f8f9fa; padding: 8px 12px; border-radius: 4px; margin-bottom: 1em;">

**Sommaire :** 1. Principe Lagrangien Sans Maillage • 2. Noyaux de Lissage • 3. Équations du Mouvement • 4. Viscosité Artificielle • 5. Tension Superficielle • 6. Conditions aux Limites • 7. Fluides Non-Newtoniens • 8. Résultats de Validation • 9. Avantages Uniques • 10. Limitations et Solutions • 11. Coût Computationnel • 12. Bibliothèques Open-Source • 13. Références
</div>

## 1. Principe Lagrangien Sans Maillage

La méthode **SPH (Smoothed Particle Hydrodynamics)** est une approche **lagrangienne** et **sans maillage (meshless)** où le fluide est représenté par un ensemble de particules mobiles transportant les propriétés physiques (masse, vitesse, pression).

### 1.1 Concept Fondamental

Contrairement aux méthodes sur grille (VOF, FEM), il n'y a pas de connexions fixes entre les points de discrétisation. La valeur d'une propriété scalaire $A$ en une position $\mathbf{r}$ est calculée par **interpolation** sur les particules voisines :

$$A(\mathbf{r}) = \sum_b m_b \frac{A_b}{\rho_b} W(|\mathbf{r} - \mathbf{r}_b|, h)$$

où :
- $m_b$ : masse de la particule $b$
- $\rho_b$ : densité de la particule $b$
- $W$ : **noyau de lissage** (smoothing kernel)
- $h$ : **longueur de lissage** (smoothing length)

---

## 2. Noyaux de Lissage

### 2.1 Fonction du Noyau

Le noyau $W(r, h)$ doit satisfaire plusieurs propriétés :
- **Normalisation** : $\int W(r, h) dV = 1$
- **Limite delta** : $\lim_{h \to 0} W(r, h) = \delta(r)$
- **Support compact** : $W(r, h) = 0$ pour $r > \kappa h$ (typiquement $\kappa = 2$)

### 2.2 Noyaux Courants

**Cubic Spline (M₄) :**

| Domaine | Expression |
|---------|------------|
| $0 \leq q < 1$ | $W(q) = \frac{\sigma_d}{h^d} \left(1 - \frac{3}{2}q^2 + \frac{3}{4}q^3\right)$ |
| $1 \leq q < 2$ | $W(q) = \frac{\sigma_d}{h^d} \cdot \frac{1}{4}(2-q)^3$ |
| $q \geq 2$ | $W(q) = 0$ |

avec $q = r/h$ et $\sigma_d$ le facteur de normalisation dimensionnel.

**Quintic Spline (M₆) :**

Plus précis mais plus coûteux, réduit les instabilités tensorielles.

**Wendland C4 :**

$$W(q) = \frac{\sigma_d}{h^d} (1-q/2)^6 (35q^2/12 + 3q + 1) \quad \text{pour } q < 2$$

Très stable pour les écoulements à haute vitesse.

---

## 3. Équations du Mouvement

### 3.1 Équation de Quantité de Mouvement

L'équation de mouvement pour une particule $a$ est :

$$m_a \frac{d\mathbf{v}_a}{dt} = -\sum_b m_b \left(\frac{p_a}{\rho_a^2} + \frac{p_b}{\rho_b^2} + \Pi_{ab}\right) \nabla_a W_{ab} + \mathbf{f}_\sigma$$

où :
- $p_a, p_b$ : pressions des particules $a$ et $b$
- $\Pi_{ab}$ : terme de **viscosité artificielle**
- $\mathbf{f}_\sigma$ : force de tension superficielle

### 3.2 Équation d'État

La pression est calculée par une équation d'état faiblement compressible :

$$p = c_0^2 (\rho - \rho_0) \quad \text{ou} \quad p = B\left[\left(\frac{\rho}{\rho_0}\right)^\gamma - 1\right]$$

avec $c_0$ la vitesse du son numérique (typiquement $c_0 = 10 \cdot v_{max}$) et $\gamma = 7$ pour les liquides.

---

## 4. Viscosité Artificielle

### 4.1 Nécessité

La SPH standard souffre d'instabilités numériques, notamment des **oscillations de pression** et des **instabilités tensorielles**. La viscosité artificielle stabilise le schéma.

### 4.2 Formulation de Monaghan

| Condition | Expression de $\Pi_{ab}$ |
|-----------|--------------------------|
| $\mathbf{v}_{ab} \cdot \mathbf{r}_{ab} < 0$ | $\Pi_{ab} = \frac{-\alpha \bar{c}_{ab} \mu_{ab} + \beta \mu_{ab}^2}{\bar{\rho}_{ab}}$ |
| sinon | $\Pi_{ab} = 0$ |

avec :

$$\mu_{ab} = \frac{h \mathbf{v}_{ab} \cdot \mathbf{r}_{ab}}{|\mathbf{r}_{ab}|^2 + \epsilon h^2}$$

**Paramètres typiques :** $\alpha = 0.1$, $\beta = 0$, $\epsilon = 0.01$

---

## 5. Tension Superficielle

### 5.1 Modèle de Morris (CSF)

La méthode **Continuum Surface Force (CSF)** adaptée à SPH ajoute une force volumique basée sur la courbure de l'interface :

$$\mathbf{F}_{st} = -\sigma \kappa \mathbf{n}$$

où :
- $\mathbf{n} = \nabla c$ : normale calculée par le gradient du **champ de couleur** $c$ (1 dans l'encre, 0 ailleurs)
- $\kappa = -\nabla \cdot \mathbf{n}$ : courbure de l'interface

### 5.2 Calcul de la Courbure en SPH

$$\kappa_a = -\frac{1}{|\mathbf{n}_a|} \sum_b \frac{m_b}{\rho_b} (\mathbf{n}_b - \mathbf{n}_a) \cdot \nabla_a W_{ab}$$

**Limitation :** La méthode CSF introduit du bruit numérique, surtout aux interfaces fines.

### 5.3 Modèle de Pairwise Force

Alternative plus stable basée sur les forces interparticulaires :

$$\mathbf{F}_{st,a} = -\sigma \sum_b s_{ab} \frac{\mathbf{r}_{ab}}{|\mathbf{r}_{ab}|} W_{ab}$$

avec $s_{ab}$ un coefficient de tension dépendant des types de particules.

---

## 6. Conditions aux Limites

### 6.1 Problématique

Gérer des parois solides étanches est **difficile** en SPH car les particules n'ont pas de connexions fixes. Plusieurs approches existent :

### 6.2 Particules Fantômes (Adami et al., 2012)

Les parois sont constituées de plusieurs couches de **particules fantômes (dummy particles)** fixes :

1. Ces particules exercent une **pression répulsive** calculée dynamiquement
2. Elles imposent la condition de **non-glissement** (no-slip)
3. Les propriétés (pression, vitesse) sont extrapolées depuis le fluide

**Extrapolation de la pression :**

$$p_{wall} = \frac{\sum_f p_f W_{wf} + (\mathbf{g} - \mathbf{a}_{wall}) \cdot \sum_f \rho_f \mathbf{r}_{wf} W_{wf}}{\sum_f W_{wf}}$$

### 6.3 Particules Répulsives (Lennard-Jones)

Force répulsive de type Lennard-Jones pour empêcher la pénétration :

$$\mathbf{F}_{rep} = D \left[\left(\frac{r_0}{r}\right)^{n_1} - \left(\frac{r_0}{r}\right)^{n_2}\right] \frac{\mathbf{r}}{r^2}$$

avec $n_1 = 12$, $n_2 = 4$ typiquement.

---

## 7. Adaptation aux Fluides Non-Newtoniens

### 7.1 Fluides Rhéofluidifiants

Le tenseur des contraintes est calculé avec une viscosité dépendant du taux de cisaillement :

$$\boldsymbol{\tau}_a = K|\dot{\gamma}_a|^{n-1} \dot{\gamma}_a$$

où $\dot{\gamma}_a$ est le taux de cisaillement de la particule $a$, calculé par :

$$\dot{\gamma}_a = \sqrt{2\mathbf{D}_a : \mathbf{D}_a}$$

### 7.2 Fluides Thixotropes (Modèle de Moore)

**Avantage unique de SPH :** Grâce à son approche lagrangienne, SPH peut naturellement gérer la **thixotropie** (dépendance temporelle de la viscosité).

Le paramètre de structure $\lambda$ évolue selon :

$$\lambda(t) = \lambda_0 + (1 - \lambda_0) e^{-t/\tau_{thix}}$$

où $\tau_{thix}$ est le temps de restructuration.

La viscosité devient :

$$\eta(\dot{\gamma}, \lambda) = \eta_\infty + (\eta_0 - \eta_\infty) \lambda^m \cdot f(\dot{\gamma})$$

**Étude Pourquie et al. (2024) :** Première étude SPH systématique pour les encres thixotropes, montrant une augmentation de 25 % du temps de pincement pour $\tau_{thix} = 1$ ms.

### 7.3 Fluides Viscoélastiques (Intégrale Temporelle)

Le tenseur des contraintes est calculé via une intégrale de mémoire :

$$\boldsymbol{\tau}_a = \int_0^t G(t - t') \dot{\gamma}_a(t') dt'$$

où $G(t)$ est le module de relaxation.

---

## 8. Résultats de Validation

### 8.1 Étude Pourquie et al. (2024) - Encre Thixotrope

**Configuration :**
- Solveur : PySPH (Python/GPU)
- Noyau : Cubic spline, $h = 1.2\Delta x$
- Rhéologie : Loi de puissance ($n = 0.6$, $K = 0.08$ Pa·sⁿ) + thixotropie

**Conditions :**
- $D = 25$ µm
- $v_{max} = 15$ m/s
- $We = 4.2$

**Résultats :**
- Erreur sur la forme de la goutte : < 3 % vs expérimental
- Temps de calcul : 4 h sur RTX 4090

### 8.2 Étude Markesteijn et al. (2023) - Multi-Gouttes et Coalescence

**Configuration :**
- Solveur : DualSPHysics
- Nombre de particules : 10⁶
- Fréquence d'éjection : 10–50 kHz

**Résultats :**

| Fréquence (kHz) | Coalescence en vol | Satellites (%) | Stabilité du jet |
|-----------------|-------------------|----------------|------------------|
| 10 | Non | 8 | Bonne |
| 30 | Partielle | 15 | Moyenne |
| 50 | Oui | 30 | Mauvaise |

**Mécanisme :** À haute fréquence, les gouttes n'ont pas le temps de se détacher complètement avant l'éjection suivante. La coalescence réduit la résolution spatiale.

---

## 9. Avantages Uniques pour la Dispense

### 9.1 Surface Libre

La SPH est **imbattable** pour gérer les surfaces libres complexes :
- Ruptures de jet
- Formation de satellites
- Éclaboussures violentes

**Raison :** Pas de maillage à déformer ou à raffiner.

### 9.2 Advection Exacte

Le terme convectif non-linéaire $(\mathbf{u} \cdot \nabla)\mathbf{u}$ est traité **exactement** par le mouvement des particules, éliminant la diffusion numérique des méthodes eulériennes.

### 9.3 Coalescence Naturelle

La fusion de gouttes est gérée **naturellement** : les particules de deux gouttes proches interagissent simplement via les noyaux SPH.

---

## 10. Limitations et Solutions

| Limitation | Description | Solution |
|------------|-------------|----------|
| **Bruit numérique** | Oscillations dans les champs de pression/vitesse | Noyaux d'ordre supérieur (quintic spline) |
| **Instabilité tenseur** | Instabilité pour $v > 20$ m/s | Viscosité artificielle + termes de correction |
| **Conditions aux limites** | Parois difficiles à gérer | Particules fantômes (Adami) |
| **Coût mémoire** | 10⁶ particules = 32–64 GB RAM | GPU avec mémoire élevée (A100, RTX 4090) |

---

## 11. Coût Computationnel

### 11.1 Configuration Typique

Pour une simulation 3D (1 ms d'éjection, 10⁶ particules) :

| Configuration | Particules | Temps (h) | Hardware |
|---------------|------------|-----------|----------|
| Standard | 100k | 2–4 | 8 cœurs CPU |
| Haute résolution | 1M | 5–10 | RTX 4090 (24 GB) |
| Multi-GPU | 5M | 4–8 | 4× A100 (40 GB) |

**Scaling GPU :** Accélération x10–x15 vs CPU pour les simulations > 500k particules.

---

## 12. Bibliothèques Open-Source

| Bibliothèque | Langage | GPU | Focus |
|--------------|---------|-----|-------|
| **PySPH** | Python/Cython | CUDA (OpenCL) | Flexibilité, prototypage rapide |
| **DualSPHysics** | C++/CUDA | CUDA native | Performance, applications côtières |
| **GPUSPH** | C++/CUDA | CUDA | Écoulements géophysiques |
| **SPHinXsys** | C++ | OpenMP | Couplages multiphysiques |

---

## 13. Références

> **Note** : Pour la liste complète des références, consultez la section **Bibliographie** dans le menu Annexes.
