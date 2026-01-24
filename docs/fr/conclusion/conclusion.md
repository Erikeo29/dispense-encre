**Sommaire :**
1. Conclusion
2. Perspectives
   - 2.1 Intelligence artificielle et modélisation hybride
   - 2.2 Calcul quantique
   - 2.3 Impression 4D et encres intelligentes
   - 2.4 Opportunités de recherche

---

## 1. Conclusion

Cette étude a permis de modéliser la dispense d'une encre rhéofluidifiante dans des micro-via en utilisant quatre méthodes numériques distinctes : FEM/Phase-Field, VOF, LBM et SPH.

Les résultats obtenus montrent des tendances comparables à ce qui est observé expérimentalement. Notamment, l'impact de la position de la buse en X sur le phénomène d'overflow et sur l'uniformité du remplissage a pu être mis en évidence. De même, les phénomènes physicochimiques attendus ont été reproduits : l'influence de la viscosité et des angles de contact (énergie de surface) sur l'étalement de l'encre correspond aux comportements physiques anticipés.

Des différences de résultats apparaissent selon les modèles utilisés, ce qui est cohérent compte tenu de leurs formulations numériques très différentes (eulérien vs lagrangien, maillé vs sans maillage, macroscopique vs mésoscopique). Cependant, les tendances globales restent comparables entre les quatre approches, ce qui renforce la confiance dans la validité des simulations.

Pour aller plus loin, il serait nécessaire de poursuivre l'amélioration des codes, d'affiner les modèles physicochimiques (notamment la rhéologie et le mouillage dynamique), et d'optimiser les paramètres numériques pour améliorer la justesse des résultats par rapport aux observations expérimentales.

---

## 2. Perspectives

### 2.1 Intelligence artificielle et modélisation hybride

### PINN (Physics-Informed Neural Networks)

Les **PINN** combinent les équations physiques avec des réseaux de neurones pour accélérer les simulations :

- **Principe :** Le réseau apprend à résoudre les équations de Navier-Stokes en minimisant à la fois l'erreur de données et la violation des équations physiques.
- **Application inkjet :** Raissi et al. (2020) ont utilisé des PINN pour résoudre Navier-Stokes avec une précision comparable à FEM mais 100× plus rapidement.
- **Limitation actuelle :** Généralisation limitée hors du domaine d'entraînement.

### Surrogate Models

Les **modèles de substitution** remplacent les simulations coûteuses par des réseaux de neurones entraînés :

- **Exemple :** Un réseau peut prédire le volume des satellites en fonction de $We$, $Oh$, et $n$ sans résoudre Navier-Stokes.
- **Avantage :** Optimisation en temps réel des paramètres d'éjection.

### Apprentissage par renforcement

- **Application :** Un agent RL peut apprendre à ajuster $v_{max}$ et $\tau$ pour minimiser les satellites.
- **Potentiel :** Contrôle adaptatif des têtes d'impression en temps réel.

---

### 2.2 Calcul quantique

Le calcul quantique pourrait révolutionner la modélisation des écoulements complexes :

### Algorithmes quantiques pour SPH

- Les ordinateurs quantiques pourraient simuler 10⁹ particules SPH en temps réel.
- **Exemple :** IBM a démontré (2023) un algorithme quantique pour la dynamique moléculaire, applicable à SPH.

### Optimisation des maillages FEM

- Les algorithmes quantiques de partitionnement de graphes pourraient réduire le coût des maillages 3D adaptatifs.

---

### 2.3 Impression 4D et encres intelligentes

Les encres rhéofluidifiantes sont de plus en plus utilisées pour l'**impression 4D** (matériaux qui changent de forme après impression) :

### Encres à mémoire de forme

- Polymères qui se déforment sous l'effet de la température ou de la lumière.
- **Modélisation :** Couplage FEM avec des modèles thermomécaniques.

### Encres conductrices (rhéofluidifiantes)

- Nanoparticules d'argent ou de graphène pour l'électronique imprimée.
- **Défis :** Rhéologie complexe (thixotropie, viscoélasticité) + sédimentation.

---

### 2.4 Opportunités de recherche

### Couplage rhéologie-interface

**Problématique :** Aucun modèle ne gère simultanément la rhéologie non-newtonienne complexe (thixotropie) et les interfaces libres avec une précision sub-micronique.

**Pistes de recherche :**
- **Hybridation VOF-SPH** : VOF pour le suivi d'interface, SPH pour la rhéologie.
- **LBM avec rhéologie avancée** : Implémenter des modèles de thixotropie et de viscoélasticité dans LBM.
- **FEM adaptatif** : Maillages dynamiques qui s'adaptent aux zones de fort cisaillement.

### Échelles sub-microniques

**Problématique :** Les gouttes < 5 µm sont difficiles à modéliser en raison des effets de tension superficielle dominants et des temps de calcul prohibitifs.

**Pistes de recherche :**
- **Modèles multi-échelles** : Coupler un modèle macroscopique (VOF, FEM) avec un modèle mésoscopique (LBM, DPD).
- **Simulations atomistiques** : Utiliser la dynamique moléculaire (MD) pour les gouttes < 1 µm.
- **Approches asymptotiques** : Développer des modèles réduits pour les gouttes sub-microniques (théorie des films minces).

### Validation expérimentale avancée

**Problématique :** Seulement 30 % des études incluent une validation expérimentale rigoureuse.

**Pistes de recherche :**
- **Micro-PIV** : Mesure des champs de vitesse dans les gouttes < 10 µm.
- **Tomographie par cohérence optique (OCT)** : Imagerie 3D des interfaces avec une résolution de 1 µm.
- **Rhéométrie in situ** : Mesure de la viscosité dans le filament pendant l'éjection.

---

## Références

> **Note** : Pour la liste complète des références, consultez la section **Bibliographie** dans le menu Annexes.
