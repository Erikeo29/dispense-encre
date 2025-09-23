# 💧 Simulation de Dispensing

Application Streamlit pour simuler et visualiser la dispense.

## 🎯 Fonctionnalités

- **Comparaison de 2 simulations** simultanées côte à côte
- **Paramètres configurables** :
  - Dimensions (diamètres puit/buse, shifts X/Z)
  - Propriétés physiques (viscosité, angles de contact)
- **Documentation intégrée** : physique et code source
- **Mapping flexible** via fichier CSV

## 🚀 Installation

```bash
# Cloner le repository
git clone https://github.com/[votre-username]/dispensing.git
cd dispensing

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## 📁 Structure

```
├── app.py                  # Application principale
├── gif/                    # Dossier des animations GIF
├── documentation/          # Documentation markdown
├── gif_mapping.csv         # Correspondance paramètres-GIF
└── requirements.txt        # Dépendances Python
```

## 🔧 Configuration

Modifiez `gif_mapping.csv` pour ajouter de nouvelles simulations :
- Format CSV avec séparateur point-virgule (;)
- 10 paramètres par simulation
- Placez les GIFs dans le dossier `gif/`

## 📊 Paramètres de simulation

- **Diamètre du puit** : 800-1200 µm
- **Diamètre de la buse** : 100-200 µm
- **Shifts X/Z** : Positionnement de la buse
- **Viscosité** : 0.5-10 Pa.s
- **Angles de contact** : 30-90°

## 📝 License

MIT

## 👥 Auteur

EQU - Septembre 2025
