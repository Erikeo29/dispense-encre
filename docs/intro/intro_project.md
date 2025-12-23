# Simulation de la Dispense de Microgouttes d'Encre Rhéofluidifiante

## Contexte Scientifique et Industriel

### Évolution Technologique de l'Impression Jet d'Encre

L'impression jet d'encre (*inkjet*) a connu une évolution remarquable depuis ses débuts dans les années 1960. Les premières technologies, basées sur le **continuous inkjet (CIJ)** (Sweet, 1965), utilisaient un jet continu dévié électrostatiquement pour former des gouttes. L'avènement du **drop-on-demand (DOD)** dans les années 1980, notamment avec les têtes piézo-électriques (Epson, HP), a révolutionné le domaine en permettant un contrôle précis de l'éjection de gouttes de 1–100 pL à des fréquences allant jusqu'à 100 kHz.

**Applications industrielles actuelles :**
- Impression 3D et fabrication additive
- Électronique imprimée (circuits, capteurs)
- Bioprinting et dépôt de cellules
- Dépôt de matériaux fonctionnels (encres conductrices Ag/AgCl)

---

## Propriétés des Encres Rhéofluidifiantes

### Comportement Non-Newtonien

Les encres rhéofluidifiantes sont des fluides **non-newtoniens** dont la viscosité apparente diminue sous l'effet d'un cisaillement. Leur comportement est décrit par des lois empiriques :

**Loi de puissance (Ostwald-de Waele) :**

$$\tau = K\dot{\gamma}^n \quad \text{avec } n < 1$$

où $\tau$ est la contrainte de cisaillement, $K$ l'indice de consistance, $\dot{\gamma}$ le taux de cisaillement, et $n$ l'indice de comportement.

**Modèle de Carreau-Yasuda :**

$$\eta(\dot{\gamma}) = \eta_\infty + \frac{\eta_0 - \eta_\infty}{[1 + (k\dot{\gamma})^a]^{(1-n)/a}}$$

où $\eta_0$ et $\eta_\infty$ sont les viscosités à cisaillement nul et infini, et $k$, $a$ des paramètres d'ajustement.

**Exemple industriel :** Une encre piézo-électrique typique présente $\eta_0 = 15$ mPa·s (au repos) et $\eta = 3$ mPa·s sous $\dot{\gamma} = 10^4$ s⁻¹.

---

## Défis Technologiques Actuels

### Enjeux Majeurs de l'Impression Inkjet

| Défi | Description | Impact |
|------|-------------|--------|
| **Résolution spatiale** | Atteindre > 2400 dpi nécessite des gouttes < 5 µm | Contrôle de la dynamique interfaciale |
| **Stabilité des gouttes** | Les satellites représentent 20–30 % du volume éjecté | Réduction de la qualité d'impression |
| **Compatibilité des encres** | Encres pigmentées vs colorants | Modèles rhéologiques avancés requis |
| **Efficacité énergétique** | Têtes piezo consommant jusqu'à 10 W à > 50 kHz | Limite l'intégration portable |

---

## Problématiques Clés et Nombres Adimensionnels

La modélisation de la dispense de microgouttes implique plusieurs phénomènes physiques interdépendants, caractérisés par les nombres adimensionnels suivants :

### Nombres Adimensionnels Fondamentaux

| Nombre | Expression | Signification | Valeur typique (inkjet) |
|--------|------------|---------------|------------------------|
| **Reynolds** | $Re = \frac{\rho v D}{\eta}$ | Effets inertiels vs visqueux | 10 – 100 |
| **Weber** | $We = \frac{\rho v^2 L}{\sigma}$ | Forces inertielles vs tension superficielle | $We \approx 4$ (satellites) |
| **Ohnesorge** | $Oh = \frac{\eta}{\sqrt{\rho \sigma D}}$ | Viscosité, tension superficielle et taille | $Oh < 0.1$ (gouttes stables) |
| **Deborah** | $De = \lambda \dot{\gamma}$ | Effets viscoélastiques (temps de relaxation $\lambda$) | Variable selon encre |
| **Capillaire** | $Ca = \frac{\eta v}{\sigma}$ | Viscosité vs capillarité | $Ca \ll 1$ (régime capillaire) |
| **Bond** | $Bo = \frac{\rho g L^2}{\sigma}$ | Gravité vs tension superficielle | $Bo \ll 1$ (gravité négligeable) |

**Interprétation physique :**
- $Re$ entre 10 et 100 : régime laminaire avec effets inertiels significatifs
- $We \approx 4$ : valeur critique pour la formation de satellites
- $Oh < 0.1$ : favorise la formation de gouttes stables

---

## Objectifs du Projet

Ce projet vise à **modéliser et comparer** quatre approches numériques pour la simulation de dispense d'encre rhéofluidifiante dans des micro-puits :

### Approche Comparative Multi-Modèles

| Modèle | Méthode | Implémentation | Focus Physique |
|--------|---------|----------------|----------------|
| **FEM** | Phase-Field / Éléments Finis | Python (FEniCS) | Thermodynamique de l'interface, capillarité fine |
| **VOF** | Volume of Fluid | C++ (OpenFOAM) | Standard industriel, robustesse, conservation de masse |
| **LBM** | Lattice Boltzmann (Shan-Chen) | C++ (Palabos) | Calcul HPC/GPU, géométries complexes, mouillage naturel |
| **SPH** | Smoothed Particle Hydrodynamics | Python (PySPH) | Surfaces libres complexes, éclaboussures, dynamique violente |

### Système Physique Étudié

- **Simulation diphasique** : encre Ag/AgCl + air en domaine microfluidique
- **Régime** : laminaire incompressible ($Re \ll 2300$)
- **Interface** : méthodes de suivi adaptées à chaque approche
- **Rhéologie** : modèle de Carreau pour le comportement rhéofluidifiant

**Paramètres géométriques :**
- Diamètre du puit : 800 – 1500 µm
- Diamètre de la buse : 200 – 350 µm
- Décalage horizontal : 0, -75, -150 µm
- Temps de dispense : 40 ms

---

## Structure de la Documentation

Cette documentation technique est organisée comme suit :

1. **Comparaison des modèles** : Analyse technique comparative (précision, coût, hardware)
2. **Physique FEM** : Fondements mathématiques de la méthode Phase-Field
3. **Physique VOF** : Méthode Volume of Fluid et schémas de reconstruction
4. **Physique LBM** : Approche mésoscopique Lattice Boltzmann
5. **Physique SPH** : Méthode lagrangienne sans maillage
6. **Conclusion** : Recommandations et perspectives

---

## Références Clés

- Sweet, R. G. (1965). *High frequency recording with electrostatically deflected ink jets*. Review of Scientific Instruments, 36(2), 131-136.
- Basaran, O. A., Gao, H., & Bhat, P. P. (2013). *Nonstandard inkjets*. Annual Review of Fluid Mechanics, 45, 85-113.
- Derby, B. (2010). *Inkjet printing of functional and structural materials*. Annual Review of Materials Research, 40, 395-414.
