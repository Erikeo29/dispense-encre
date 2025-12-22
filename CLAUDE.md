# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
```bash
# Run the application locally
streamlit run app.py

# Install dependencies
pip install -r requirements.txt

# Deploy to GitHub (after changes)
git add .
git commit -m "Your commit message"
git push origin main
```

## Architecture

### Core Application Structure

The application is a Streamlit-based simulation tool with a multi-page architecture:

1. **`app.py`**: Main application file (417 lines) containing all logic
   - `main()`: Entry point (lines 352-415) that handles page routing through sidebar navigation
   - Three main pages: Simulation, Physics Documentation, Python Code

2. **Simulation System**:
   - Uses CSV-based GIF mapping via `load_gif_mapping()` function (lines 13-36)
   - Reads `gif_mapping.csv` with semicolon separators and converts to Python dictionary
   - Displays two side-by-side simulations with independent parameter controls
   - 6 parameters per simulation: puit diameter, buse diameter, shift X, viscosity, contact angle (wall), contact angle (gold)
   - Central "LANCER LES SIMULATIONS" button triggers both simulations simultaneously
   - 109 pre-computed simulation results available

3. **Data Flow**:
   - User selects 6 parameters per simulation → Stored as tuple in session state
   - Click "LANCER" button → Sets `sim1_running` and `sim2_running` flags → Triggers `st.rerun()`
   - Parameter tuple lookup in `gif_mapping` dictionary → Returns GIF filename
   - GIF loaded from `gif/` directory and converted to base64 for inline display via HTML `<img>` tag
   - Session state preserves parameters between Streamlit reruns

### Key Architectural Decisions

- **CSV-Based Parameter Mapping**: The `load_gif_mapping()` function reads `gif_mapping.csv` and creates a dictionary with tuple keys `(puit_diam, buse_diam, shift_x, viscosity, angle_wall, angle_gold)` → `gif_path`. Enables quick lookup of pre-computed simulations.

- **Tuple-Based Lookup Pattern**: Parameters stored as immutable tuples allow fast dictionary lookups. Requires exact parameter matches (no interpolation).

- **Session State Mechanics**: Streamlit reruns entire script on interaction. Parameters stored in `st.session_state` persist across reruns. Flags like `sim1_running` trigger conditional GIF display.

- **Aggressive Branding Removal**: `hide_streamlit_branding()` function (lines 48-101) injects CSS to hide Streamlit UI elements (hamburger menu, footer, GitHub button, toolbar) for professional appearance.

- **Base64 GIF Encoding**: GIFs converted to base64 strings and embedded in HTML `<img>` tags for inline display without external file serving.

- **Documentation Loading**: Physics and code documentation are loaded from markdown files in `documentation/` directory using `load_markdown_file()` (lines 103-111).

### Important Files

- `gif_mapping.csv`: Contains parameter-to-GIF mappings (7 columns: filename + 6 parameters, semicolon-separated, 109 data rows)
- `documentation/ink_dispensing_physique_v1.md`: Physics documentation
- `documentation/ink_dispensing_code_v8.md`: Python code examples
- `.streamlit/config.toml`: UI theme configuration (color scheme, minimal toolbar)

## Common Tasks

### Adding New Simulations

1. Generate GIF file from FEniCS simulation with desired parameters
2. Save GIF to `gif/` directory (naming convention: `gif_XXX.gif`)
3. Add new row to `gif_mapping.csv` with parameters and filename:
   ```csv
   gif_new01.gif;800;200;0;1,5;90;35
   ```
   Note: Use semicolon separator and comma for decimal point (French locale)
4. Test locally: `streamlit run app.py`
5. Deploy: `git add . && git commit -m "Add simulation XXX" && git push`

### Modifying Parameter Ranges

Parameter dropdowns are defined in `simulation_page()` function around lines 134-220. To add new values:

**Example - Add new nozzle diameter (300 µm)**:
```python
# Simulation 1 (around line 154)
diametre_buse_1 = st.selectbox(
    "Diamètre buse (µm)",
    options=[200, 250, 300, 350],  # Add 350
    key="diam_buse_1"
)

# Simulation 2 (around line 204)
diametre_buse_2 = st.selectbox(
    "Diamètre buse (µm)",
    options=[200, 250, 300, 350],  # Add 350
    key="diam_buse_2"
)
```

Note: Must also generate corresponding GIF files and update CSV for new parameter combinations.

### Troubleshooting Missing GIFs

If simulation shows "Aucune simulation disponible pour cette combinaison":
1. Check parameter tuple matches exactly a row in `gif_mapping.csv`
2. Verify GIF file exists in `gif/` directory
3. Check CSV uses semicolons and comma decimal separator (French format)
4. Validate CSV encoding (UTF-8) and no extra spaces

### Deployment Notes

- Repository: https://github.com/Erikeo29/dispense-encre
- Branch: `main` (single branch deployment)
- Streamlit Cloud auto-redeploys on push to main branch
- Check `requirements.txt` for dependency versions (streamlit==1.40.2, pandas==2.2.3)
- No environment variables currently required