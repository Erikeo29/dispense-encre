import pandas as pd
import os
import re

# Parameters from YAML logic
# Runs 1-36: CA_sub=35, CA_wr=120
# Runs 37-72: CA_sub=15, CA_wr=120
# Runs 73-108: CA_sub=35, CA_wr=15
# Runs 109-144: CA_sub=15, CA_wr=15

# Inner loop (36 runs) structure based on full_factorial_study.yaml
# loops order: y_gap (2) -> x_gap (3) -> eta0 (3) -> ratio (2)
# y_gap: [0.030, 0.120]
# x_gap: [0.0, -0.075, -0.150]
# eta0: [0.5, 1.5, 5.0]
# ratio: [0.8, 1.2]

y_gaps = [30, 120] # um
x_gaps = [0, -75, -150] # um
eta0s = [0.5, 1.5, 5.0] # Pa.s
ratios = [0.8, 1.2]

# Generate the base 36 combinations in order
base_combinations = []
for y in y_gaps:
    for x in x_gaps:
        for e in eta0s:
            for r in ratios:
                base_combinations.append({
                    "gap buse (µm)": y,
                    "shift buse (µm)": x,
                    "Viscosite eta0 (Pa.s)": e,
                    "ratio surface goutte/puit": r
                })

# Blocks
blocks = [
    {"start": 1, "end": 36, "CA_sub": 35, "CA_wr": 120},
    {"start": 37, "end": 72, "CA_sub": 15, "CA_wr": 120},
    {"start": 73, "end": 108, "CA_sub": 35, "CA_wr": 15},
    {"start": 109, "end": 144, "CA_sub": 15, "CA_wr": 15},
]

rows = []
for block in blocks:
    for i, base in enumerate(base_combinations):
        run_id = block["start"] + i
        row = base.copy()
        row["run_id"] = run_id
        row["CA substrat (deg)"] = block["CA_sub"]
        row["CA mur droit (deg)"] = block["CA_wr"]
        row["CA mur gauche (deg)"] = 15 # Constant
        rows.append(row)

df = pd.DataFrame(rows)

# Get list of files to match
assets_gif = "assets/vof/gif"
assets_png = "assets/vof/png"
gif_files = sorted([f for f in os.listdir(assets_gif) if f.endswith(".gif")])
png_files = sorted([f for f in os.listdir(assets_png) if f.endswith(".png")])

# Helper to find filename by run_id
def find_file(run_id, files):
    # Search for "run_001_" or "run_144_" etc.
    # Format is run_{:03d}_...
    prefix = f"run_{run_id:03d}_"
    for f in files:
        if f.startswith(prefix):
            return f
    return None

# Add filenames to DF
df["nom fichier gif"] = df["run_id"].apply(lambda x: find_file(x, gif_files))
df["nom fichier png"] = df["run_id"].apply(lambda x: find_file(x, png_files))

# Filter out missing files (should not happen if copy was successful)
df_gif = df.dropna(subset=["nom fichier gif"]).drop(columns=["nom fichier png"])
df_png = df.dropna(subset=["nom fichier png"]).drop(columns=["nom fichier gif"])

# Save CSVs
df_gif.to_csv("data/vof_gif_mapping.csv", sep=";", index=False, encoding="utf-8")
df_png.to_csv("data/vof_png_mapping.csv", sep=";", index=False, encoding="utf-8")

print(f"Generated mappings: {len(df_gif)} GIFs, {len(df_png)} PNGs")
