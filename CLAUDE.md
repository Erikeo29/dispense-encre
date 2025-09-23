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

1. **`app.py`**: Main application file containing all logic
   - `main()`: Entry point that handles page routing through sidebar navigation
   - Three main pages: Simulation, Physics Documentation, Python Code

2. **Simulation System**:
   - Uses a hardcoded GIF mapping in `get_gif_mapping()` function (lines 12-21)
   - Note: There's also CSV-based mapping code that's currently unused (should be refactored)
   - Displays two side-by-side simulations with independent parameter controls
   - Parameters include physical dimensions (diameters, shifts) and material properties (viscosity, contact angles)

3. **Data Flow**:
   - Parameters → GIF selection via tuple matching
   - GIF files loaded from `gif/` directory and converted to base64 for inline display
   - Session state manages simulation parameters between reruns

### Key Architectural Decisions

- **Dual Mapping System**: The code contains both hardcoded GIF mapping (active) and CSV-based mapping (inactive). The CSV system includes `load_gif_mapping_df()` and related functions but isn't used by the simulation page.

- **Documentation Loading**: Physics and code documentation are loaded from markdown files in `documentation/` directory using `load_markdown_file()`.

- **Parameter Storage**: Each simulation stores parameters in two session state variables:
  - Basic parameters tuple for GIF lookup
  - Full parameters dict for display (currently not fully utilized)

### Important Files

- `gif_mapping.csv`: Contains parameter-to-GIF mappings with 10 parameters per simulation (semicolon-separated)
- `documentation/ink_dispensing_physique_v1.md`: Physics documentation
- `documentation/ink_dispensing_code_v8.md`: Python code examples

## Common Tasks

### Adding New Simulations

1. Add GIF file to `gif/` directory
2. Update the hardcoded mapping in `get_gif_mapping()` function (line 17-20)
3. OR implement the CSV-based system by connecting `load_gif_mapping()` to the simulation page

### Modifying Parameter Ranges

Edit the options lists in `simulation_page()` function (lines 62, 68, 74, 80, 86 for Simulation 1, similar lines for Simulation 2)

### Deployment Notes

- Repository: https://github.com/Erikeo29/dispense-encre
- Streamlit automatically redeploys on push to main branch
- Check `requirements.txt` for dependency versions