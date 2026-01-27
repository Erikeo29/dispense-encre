**Sommaire :**
1. Objectif du projet
2. Application cible
3. Navigation
4. Note méthodologique

---

## 1. Objectif du projet

Le but de cette application est de permettre de visualiser et comparer les résultats de **trois méthodes numériques** pour la simulation de la dispense de fluides rhéofluidifiants dans des micro-via. L'application permet d'explorer les résultats de simulations diphasiques réalisées avec différentes approches :

- **VOF (Volume of Fluid)** : Méthode eulérienne standard industriel (OpenFOAM)
- **LBM (Lattice Boltzmann)** : Approche mésoscopique optimisée GPU (Palabos)
- **SPH (Smoothed Particle Hydrodynamics)** : Méthode lagrangienne sans maillage (PySPH)

---

## 2. Application cible

Les simulations modélisent la **dispense d'une encre rhéofluidifiante** dans des micro-via.

**Paramètres clés étudiés :**
- Géométrie : diamètre micro-via (800–1500 µm), diamètre buse (200–350 µm)
- Position de la buse : décalage en X et Y (décalage vertical et horizontal par rapport au via)
- Rhéologie : viscosité variable (modèle de Carreau)
- Mouillage : angles de contact sur le fond du micro-via, sur les parois verticales du micro-via, sur la surface horizontale du substrat.

---

## 3. Navigation

Utilisez le menu latéral pour explorer les différents chapitres du projet:
1. **Introduction** : Contexte scientifique et nombres adimensionnels
2. **Comparaison des modèles** : Tableaux comparatifs détaillés
3. **Pages par modèle** : Physique, code source et exemples de simulation: animation de l'écoulement pendant la dispense(fichiers GIF) et images de l'état final (fichiers PNG).

---

## 4. Note méthodologique

Les animations et images présentées dans cette application proviennent de simulations **pré-calculées**. Les codes VOF, LBM et SPH ont été développés par l'auteur de ce site avec l'utilisation d'outils d'IA pour la réalisation et la correction des programmes sur un PC portable standard (base Linux, 1.5-3.5 GHz, 6 CPU / 12 threads), 32 Go de RAM, 8 Go de GPU (quand utilisable : LBM, SPH DualSPHysics). Les modélisations ont été réalisées avec différentes combinaisons de paramètres (géométrie, viscosité, angles de contact, temps de dispense...) sous forme d'étude paramétrique. Les résultats ont ensuite été exportés sous forme de fichiers GIF (animations) et PNG (images finales) pour alimenter cette application.

Cette application est un **visualiseur de résultats**, non un simulateur en temps réel. En effet, la réalisation de ces simulations nécessite des configurations conséquentes de packages Python ou OpenFOAM ; le temps de modélisation est également conséquent, de 10 minutes à 2 heures par simulation unitaire suivant le type de modèle numérique et des paramètres étudiés. Les codes sont fournis dans les onglets "Code" des 3 modèles afin de pouvoir les copier et reproduire ces modélisations sur d'autres machines.

L'auteur certifie que ce projet a été conçu « à partir d'une feuille blanche », sans aucune copie de sources ou de sites existants. La réalisation des codes, la structuration de l'application et la recherche d'informations techniques ont été effectuées exclusivement à l'aide d'outils d'IA et de recherches documentaires sur le Web. Ce travail est mis à disposition en open-source : il peut être librement copié, dupliqué et adapté à des fins d'apprentissage ou d'exploitation des modèles physiques et numériques présentés.
