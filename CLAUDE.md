# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run locally
streamlit run app.py

# Install dependencies
pip install -r requirements.txt

# Deploy (auto-deploys on push)
git add . && git commit -m "message" && git push origin main
```

## Architecture

### Overview

Multi-model Streamlit application (V3.0) comparing 4 numerical methods for simulating shear-thinning ink dispensing into micro-wells:

| Model | Method | Implementation |
|-------|--------|----------------|
| FEM | Phase-Field / Finite Elements | Python (FEniCS) |
| VOF | Volume of Fluid | C++ (OpenFOAM) |
| LBM | Lattice Boltzmann (Shan-Chen) | C++ (Palabos) |
| SPH | Smoothed Particle Hydrodynamics | Python (PySPH) |

### File Structure

```
app.py              # Single-file application (207 lines)
assets/             # Visual resources organized by model
  fem/gif/          # FEM simulation GIFs
  fem/png/          # FEM simulation PNGs (stored as .jpg)
  vof/gif/          # VOF simulation GIFs
  lbm/gif/          # LBM simulation GIFs
  sph/gif/          # SPH simulation GIFs
data/               # CSV mappings for parameter lookups
  fem_gif_mapping.csv   # 6-param tuple → GIF path
  fem_png_mapping.csv   # 6-param tuple → PNG path
docs/               # Documentation markdown files
  intro/            # Project introduction
  physics/          # Theory for each model
  code/             # Source code extracts (.cpp, .py, .md)
  comparaison/      # Model comparison
```

### Key Patterns

**CSV-Based Parameter Mapping** (`load_gif_mapping()`, `load_png_mapping()`):
- Semicolon-separated CSV with French locale (comma as decimal separator)
- Creates dict with tuple keys for O(1) lookup: `(param1, param2, ...) → filepath`
- Cached with 10-minute TTL via `@st.cache_data(ttl=600)`

**Documentation Loading** (`load_file_content()`):
- No caching (TTL removed) to enable live documentation updates
- Reads markdown files from `docs/` directory

**Media Display** (`load_media_as_base64()`):
- Converts images to base64 for inline HTML rendering
- Handles GIF, PNG, and JPG formats

**Page Routing**:
- Sidebar radio navigation with 6 pages
- FEM page has 4 tabs: Physics, Code, GIF Viewer, PNG Viewer
- Other model pages have 3 tabs: Physics, Code, Examples

## Common Tasks

### Adding New FEM Simulations

1. Generate GIF/PNG from FEniCS simulation
2. Save to `assets/fem/gif/` or `assets/fem/png/` (PNG saved as .jpg)
3. Add row to `data/fem_gif_mapping.csv` or `data/fem_png_mapping.csv`:
   ```csv
   new_file.gif;800;200;0;1,5;90;35
   ```
   Note: semicolon separator, comma decimal (French locale)

### Modifying FEM Parameter Options

GIF viewer parameters in `app.py:149-150`:
- Tuple order: (puit, buse, shift, viscosity, angle_wall, angle_gold)

PNG viewer parameters in `app.py:165-166`:
- Tuple order: (temps, viscosity, shift_x, shift_z, angle, remplissage)

### Adding Documentation

1. Create/edit markdown in appropriate `docs/` subdirectory
2. No app.py changes needed if using existing paths
3. Changes appear immediately (no cache)

### Troubleshooting

**"Simulation non trouvée"**: Parameter tuple doesn't match any CSV row exactly
- Check CSV uses semicolons and comma decimals
- Verify tuple order matches CSV column order
- Ensure file exists in `assets/` directory

## Deployment

- Repository: https://github.com/Erikeo29/dispense-encre
- Streamlit Cloud auto-redeploys on push to `main`
- Dependencies: streamlit, pandas (see requirements.txt)
