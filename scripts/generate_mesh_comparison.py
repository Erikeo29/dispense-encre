#!/usr/bin/env python3
"""
Generate mesh comparison images for FEM, VOF, LBM, SPH visualization.

This script creates comparable mesh/grid visualizations showing:
- FEM: Triangular adaptive mesh (Eulerian)
- VOF: Hexahedral adaptive mesh (Eulerian)
- LBM: Uniform lattice grid (Eulerian)
- SPH: Particle distribution (Lagrangian)

Usage:
    python generate_mesh_comparison.py

Output:
    assets/comparaison/mesh_fem.png
    assets/comparaison/mesh_vof.png
    assets/comparaison/mesh_lbm.png
    assets/comparaison/mesh_sph.png
"""

import matplotlib
matplotlib.use('Agg')  # Non-GUI backend for headless execution
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PolyCollection, LineCollection
import numpy as np
from pathlib import Path
import sys

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "assets" / "comparaison"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Try to import meshio for FEM mesh
try:
    import meshio
    HAS_MESHIO = True
except ImportError:
    HAS_MESHIO = False
    print("Warning: meshio not installed. FEM mesh visualization will use synthetic data.")

# Common geometry parameters (aligned across all methods)
WELL_WIDTH = 0.8  # mm
WELL_DEPTH = 0.13  # mm
PLATEAU_WIDTH = 0.4  # mm (each side for FEM) or 0.2 mm (for LBM/SPH)
DOMAIN_WIDTH_FEM = 1.6  # mm
DOMAIN_WIDTH_LBM = 1.2  # mm

# Colors
COLOR_INK = '#1f77b4'  # Blue for ink/fluid
COLOR_AIR = '#aec7e8'  # Light blue for air
COLOR_MESH = '#333333'  # Dark gray for mesh lines
COLOR_BOUNDARY = '#d62728'  # Red for boundaries
COLOR_WELL = '#2ca02c'  # Green for well region


def create_well_geometry_patch(x_start, x_end, y_bottom, y_top, plateau_y=0):
    """Create patch representing the well cavity."""
    # Well cavity (below plateau level)
    well_verts = [
        (x_start, plateau_y),
        (x_start, y_bottom),
        (x_end, y_bottom),
        (x_end, plateau_y),
    ]
    return well_verts


def generate_fem_mesh_image(mesh_path=None, output_path=None):
    """
    Generate FEM triangular mesh visualization.

    Shows adaptive triangular mesh with refinement near boundaries.
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    if mesh_path and HAS_MESHIO and Path(mesh_path).exists():
        # Read actual mesh from GMSH file
        mesh = meshio.read(mesh_path)
        points = mesh.points[:, :2] * 1000  # Convert m to mm

        # Get triangular cells
        triangles = None
        for cell_block in mesh.cells:
            if cell_block.type == 'triangle':
                triangles = cell_block.data
                break

        if triangles is not None:
            # Plot triangular mesh
            ax.triplot(points[:, 0], points[:, 1], triangles,
                      color=COLOR_MESH, linewidth=0.3, alpha=0.7)

            # Highlight well region
            ax.axhline(y=0, color=COLOR_BOUNDARY, linewidth=1.5, linestyle='--',
                      label='Niveau plateau')
            ax.axvline(x=0.4, ymin=0, ymax=0.5, color=COLOR_WELL, linewidth=1.5)
            ax.axvline(x=1.2, ymin=0, ymax=0.5, color=COLOR_WELL, linewidth=1.5)

            n_nodes = len(points)
            n_elements = len(triangles)
    else:
        # Generate synthetic triangular mesh for visualization
        # Create points for a simple mesh
        n_x, n_y = 32, 20
        x = np.linspace(0, DOMAIN_WIDTH_FEM, n_x)
        y = np.linspace(-WELL_DEPTH, 0.45, n_y)
        X, Y = np.meshgrid(x, y)

        # Add some refinement near the well edges
        X_flat = X.flatten()
        Y_flat = Y.flatten()

        # Perturb points slightly for natural mesh look
        np.random.seed(42)
        X_flat += np.random.uniform(-0.02, 0.02, len(X_flat))
        Y_flat += np.random.uniform(-0.01, 0.01, len(Y_flat))

        # Create triangulation
        from matplotlib.tri import Triangulation
        tri = Triangulation(X_flat, Y_flat)

        # Plot
        ax.triplot(tri, color=COLOR_MESH, linewidth=0.4, alpha=0.8)

        n_nodes = len(X_flat)
        n_elements = len(tri.triangles)

        # Draw well boundaries
        well_x_left = PLATEAU_WIDTH
        well_x_right = PLATEAU_WIDTH + WELL_WIDTH
        ax.plot([well_x_left, well_x_left], [-WELL_DEPTH, 0],
               color=COLOR_BOUNDARY, linewidth=2, label='Parois puit')
        ax.plot([well_x_right, well_x_right], [-WELL_DEPTH, 0],
               color=COLOR_BOUNDARY, linewidth=2)
        ax.plot([well_x_left, well_x_right], [-WELL_DEPTH, -WELL_DEPTH],
               color=COLOR_BOUNDARY, linewidth=2)
        ax.axhline(y=0, color='gray', linewidth=1, linestyle='--', alpha=0.5)

    # Labels and title
    ax.set_xlabel('x [mm]', fontsize=12)
    ax.set_ylabel('y [mm]', fontsize=12)
    ax.set_title(f'FEM - Maillage Triangulaire Adaptatif\n'
                f'(Eulérien: maillage fixe, fluide traverse)', fontsize=14)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')

    # Add info box
    info_text = (f"Maillage adaptatif\n"
                f"~5000 noeuds\n"
                f"~10000 triangles\n"
                f"h: 1-10 µm")
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {output_path}")

    plt.close()
    return fig


def generate_lbm_grid_image(output_path=None):
    """
    Generate LBM uniform lattice grid visualization.

    Shows uniform Cartesian grid typical of Lattice Boltzmann methods.
    """
    fig, (ax, axins) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [2, 1]})

    # LBM domain parameters
    domain_width = 1.2  # mm
    domain_height = 0.63  # mm
    y_min = -0.13  # mm (well bottom)
    dx = 0.005  # mm = 5 µm resolution

    # Grid parameters
    nx = int(domain_width / dx)  # 240
    ny = int(domain_height / dx)  # 126

    # Draw uniform grid (subset for visibility)
    skip = 4  # Draw every 4th line

    # Vertical lines
    for i in range(0, nx + 1, skip):
        x = i * dx
        ax.axvline(x=x, color=COLOR_MESH, linewidth=0.3, alpha=0.5)

    # Horizontal lines
    for j in range(0, ny + 1, skip):
        y = y_min + j * dx
        ax.axhline(y=y, color=COLOR_MESH, linewidth=0.3, alpha=0.5)

    # Highlight well region
    well_x_left = 0.2
    well_x_right = 1.0
    well_bottom = y_min

    # Draw well boundaries (thicker)
    ax.plot([well_x_left, well_x_left], [well_bottom, 0],
           color=COLOR_BOUNDARY, linewidth=2, label='Parois puit')
    ax.plot([well_x_right, well_x_right], [well_bottom, 0],
           color=COLOR_BOUNDARY, linewidth=2)
    ax.plot([well_x_left, well_x_right], [well_bottom, well_bottom],
           color=COLOR_BOUNDARY, linewidth=2)

    # Draw plateau lines
    ax.plot([0, well_x_left], [0, 0], color='gray', linewidth=1.5)
    ax.plot([well_x_right, domain_width], [0, 0], color='gray', linewidth=1.5)

    # Draw actual 1x1 l.u. grid in zoom panel
    zoom_x_min, zoom_x_max = 0.55, 0.65  # mm
    zoom_y_min, zoom_y_max = 0.0, 0.08  # mm

    for i in range(int(zoom_x_min / dx), int(zoom_x_max / dx) + 1):
        x = i * dx
        axins.axvline(x=x, color=COLOR_MESH, linewidth=0.8, alpha=0.7)

    for j in range(int((zoom_y_min - y_min) / dx), int((zoom_y_max - y_min) / dx) + 1):
        y = y_min + j * dx
        axins.axhline(y=y, color=COLOR_MESH, linewidth=0.8, alpha=0.7)

    # Add lattice nodes
    for i in range(int(zoom_x_min / dx), int(zoom_x_max / dx) + 1):
        for j in range(int((zoom_y_min - y_min) / dx), int((zoom_y_max - y_min) / dx) + 1):
            x = i * dx
            y = y_min + j * dx
            axins.plot(x, y, 'o', color=COLOR_INK, markersize=4)

    axins.set_xlim(zoom_x_min, zoom_x_max)
    axins.set_ylim(zoom_y_min, zoom_y_max)
    axins.set_title('ZOOM: 1 cellule = 5 µm', fontsize=11, fontweight='bold')
    axins.set_xlabel('x [mm]', fontsize=10)
    axins.set_ylabel('y [mm]', fontsize=10)
    axins.set_aspect('equal')

    # Main plot settings
    ax.set_xlim(-0.02, domain_width + 0.02)
    ax.set_ylim(y_min - 0.02, 0.5)
    ax.set_xlabel('x [mm]', fontsize=12)
    ax.set_ylabel('y [mm]', fontsize=12)
    ax.set_title(f'LBM Shan-Chen - Grille Uniforme\n'
                f'(Eulérien: grille fixe, fluide traverse)', fontsize=14)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')

    # Add info box
    info_text = (f"Grille uniforme\n"
                f"{nx}×{ny} = {nx*ny} cellules\n"
                f"dx = 5 µm\n"
                f"1 cellule = 1 l.u.")
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', horizontalalignment='left',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {output_path}")

    plt.close()
    return fig


def generate_sph_particles_image(output_path=None):
    """
    Generate SPH particle distribution visualization.

    Shows discrete particles representing the fluid - Lagrangian approach.
    """
    fig, (ax, axins) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [2, 1]})

    # Domain parameters (same as LBM/SPH)
    domain_width = 1.6  # mm
    y_min = -0.13  # mm

    # Particle parameters
    dp = 0.01  # mm = 10 µm particle spacing
    droplet_center = (0.8, 0.25)  # mm
    droplet_radius = 0.175  # mm

    # Generate particles in a circular droplet
    n_particles = 0
    particles_x = []
    particles_y = []

    # Create particles within circle
    for i in range(-20, 21):
        for j in range(-20, 21):
            x = droplet_center[0] + i * dp
            y = droplet_center[1] + j * dp
            r = np.sqrt((x - droplet_center[0])**2 + (y - droplet_center[1])**2)
            if r <= droplet_radius:
                particles_x.append(x)
                particles_y.append(y)
                n_particles += 1

    # Plot particles
    ax.scatter(particles_x, particles_y, s=8, c=COLOR_INK, alpha=0.8,
              label=f'Particules fluide (n={n_particles})')

    # Draw well geometry
    well_x_left = 0.4
    well_x_right = 1.2
    well_bottom = y_min

    # Well boundaries
    ax.plot([0, well_x_left], [0, 0], color='black', linewidth=2)
    ax.plot([well_x_right, domain_width], [0, 0], color='black', linewidth=2)
    ax.plot([well_x_left, well_x_left], [0, well_bottom], color='black', linewidth=2)
    ax.plot([well_x_right, well_x_right], [0, well_bottom], color='black', linewidth=2)
    ax.plot([well_x_left, well_x_right], [well_bottom, well_bottom], color='black', linewidth=2)

    # Zoom on edge of droplet
    zoom_x_min, zoom_x_max = 0.55, 0.75
    zoom_y_min, zoom_y_max = 0.1, 0.25

    zoom_particles_x = []
    zoom_particles_y = []
    for x, y in zip(particles_x, particles_y):
        if zoom_x_min <= x <= zoom_x_max and zoom_y_min <= y <= zoom_y_max:
            zoom_particles_x.append(x)
            zoom_particles_y.append(y)

    axins.scatter(zoom_particles_x, zoom_particles_y, s=50, c=COLOR_INK, alpha=0.8, edgecolors='black', linewidths=0.5)
    axins.set_xlim(zoom_x_min, zoom_x_max)
    axins.set_ylim(zoom_y_min, zoom_y_max)
    axins.set_title('ZOOM: particules SPH', fontsize=11, fontweight='bold')
    axins.set_xlabel('x [mm]', fontsize=10)
    axins.set_ylabel('y [mm]', fontsize=10)
    axins.set_aspect('equal')

    # Add smoothing length annotation
    h = 0.015  # smoothing length ~1.5*dp
    circle = plt.Circle((0.65, 0.18), h, fill=False, color='red', linestyle='--', linewidth=2)
    axins.add_patch(circle)
    axins.annotate('h = 15 µm\n(rayon\nd\'influence)', xy=(0.65, 0.18+h), xytext=(0.70, 0.22),
                  fontsize=9, arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

    # Main plot settings
    ax.set_xlim(-0.02, domain_width + 0.02)
    ax.set_ylim(y_min - 0.02, 0.5)
    ax.set_xlabel('x [mm]', fontsize=12)
    ax.set_ylabel('y [mm]', fontsize=12)
    ax.set_title(f'SPH - Particules Discrètes\n'
                f'(Lagrangien: particules se déplacent avec le fluide)', fontsize=14)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    # Add info box
    info_text = (f"Méthode sans maillage\n"
                f"~{n_particles} particules\n"
                f"dp = 10 µm\n"
                f"h = 15 µm")
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', horizontalalignment='left',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {output_path}")

    plt.close()
    return fig


def generate_vof_mesh_image(output_path=None):
    """
    Generate VOF hexahedral mesh visualization.

    Shows adaptive mesh with refinement near interface (OpenFOAM style).
    """
    fig, (ax, axins) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [2, 1]})

    # Domain parameters
    domain_width = 1.6  # mm
    domain_height = 0.7  # mm
    y_min = -0.13  # mm

    # Base mesh parameters
    dx_base = 0.02  # mm = 20 µm base resolution
    dx_fine = 0.005  # mm = 5 µm refined resolution

    # Draw base mesh
    n_x_base = int(domain_width / dx_base)
    n_y_base = int(domain_height / dx_base)

    # Create cells with different refinement levels
    cells = []

    # Well region (refined)
    well_x_left = 0.4
    well_x_right = 1.2
    well_bottom = y_min

    # Base mesh (coarse)
    for i in range(n_x_base):
        for j in range(n_y_base):
            x0 = i * dx_base
            y0 = y_min + j * dx_base
            x1 = x0 + dx_base
            y1 = y0 + dx_base

            # Check if near interface region (refine there)
            near_interface = (well_x_left - 0.1 <= x0 <= well_x_right + 0.1 and
                            y0 <= 0.15)

            if near_interface:
                # Subdivide into 4 smaller cells
                dx = dx_base / 2
                for di in range(2):
                    for dj in range(2):
                        cells.append([
                            [x0 + di * dx, y0 + dj * dx],
                            [x0 + (di+1) * dx, y0 + dj * dx],
                            [x0 + (di+1) * dx, y0 + (dj+1) * dx],
                            [x0 + di * dx, y0 + (dj+1) * dx],
                        ])
            else:
                cells.append([
                    [x0, y0], [x1, y0], [x1, y1], [x0, y1]
                ])

    # Draw cells
    for cell in cells:
        verts = cell + [cell[0]]  # Close the polygon
        xs, ys = zip(*verts)
        ax.plot(xs, ys, color=COLOR_MESH, linewidth=0.3, alpha=0.6)

    # Draw well boundaries
    ax.plot([0, well_x_left], [0, 0], color='black', linewidth=2)
    ax.plot([well_x_right, domain_width], [0, 0], color='black', linewidth=2)
    ax.plot([well_x_left, well_x_left], [0, well_bottom], color=COLOR_BOUNDARY, linewidth=2, label='Parois puit')
    ax.plot([well_x_right, well_x_right], [0, well_bottom], color=COLOR_BOUNDARY, linewidth=2)
    ax.plot([well_x_left, well_x_right], [well_bottom, well_bottom], color=COLOR_BOUNDARY, linewidth=2)

    # Draw refined cells in zoom panel
    zoom_x_min, zoom_x_max = 0.32, 0.55
    zoom_y_min, zoom_y_max = -0.08, 0.12

    for cell in cells:
        x_coords = [p[0] for p in cell]
        y_coords = [p[1] for p in cell]
        if (zoom_x_min <= min(x_coords) and max(x_coords) <= zoom_x_max and
            zoom_y_min <= min(y_coords) and max(y_coords) <= zoom_y_max):
            verts = cell + [cell[0]]
            xs, ys = zip(*verts)
            axins.plot(xs, ys, color=COLOR_MESH, linewidth=0.8, alpha=0.8)

    # Draw well edge in zoom panel
    axins.axvline(x=well_x_left, color=COLOR_BOUNDARY, linewidth=2)
    axins.axhline(y=0, color='gray', linewidth=1.5, linestyle='--')

    axins.set_xlim(zoom_x_min, zoom_x_max)
    axins.set_ylim(zoom_y_min, zoom_y_max)
    axins.set_title('ZOOM: raffinement adaptatif (AMR)', fontsize=11, fontweight='bold')
    axins.set_xlabel('x [mm]', fontsize=10)
    axins.set_ylabel('y [mm]', fontsize=10)
    axins.set_aspect('equal')

    # Main plot settings
    ax.set_xlim(-0.02, domain_width + 0.02)
    ax.set_ylim(y_min - 0.02, 0.55)
    ax.set_xlabel('x [mm]', fontsize=12)
    ax.set_ylabel('y [mm]', fontsize=12)
    ax.set_title(f'VOF (OpenFOAM) - Maillage Hexaédrique Adaptatif\n'
                f'(Eulérien: maillage fixe, fluide traverse)', fontsize=14)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')

    # Add info box
    info_text = (f"Maillage adaptatif (AMR)\n"
                f"~{len(cells)} cellules\n"
                f"dx: 10-20 µm\n"
                f"Raffiné près interface")
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', horizontalalignment='left',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {output_path}")

    plt.close()
    return fig


def generate_fem_with_droplet(output_path=None):
    """Generate FEM mesh with droplet at final state (Phase-Field phi)."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    # Domain parameters
    domain_width = 1.6  # mm
    y_min = -0.13  # mm

    # Create mesh grid for phase field visualization
    n_x, n_y = 160, 70
    x = np.linspace(0, domain_width, n_x)
    y = np.linspace(y_min, 0.55, n_y)
    X, Y = np.meshgrid(x, y)

    # Create phase field phi: +1 = ink, -1 = air
    phi = -np.ones_like(X)

    # Droplet in well (final state - spread at bottom)
    well_left, well_right = 0.4, 1.2
    well_bottom = y_min

    # Fill the well with ink (phi = +1)
    for i in range(n_y):
        for j in range(n_x):
            xi, yi = X[i, j], Y[i, j]
            # Inside well cavity
            if well_left <= xi <= well_right and well_bottom <= yi <= 0.02:
                phi[i, j] = 1.0
            # Meniscus shape (curved top surface)
            elif well_left <= xi <= well_right and 0.02 < yi <= 0.08:
                # Parabolic meniscus
                x_center = (well_left + well_right) / 2
                dist_from_center = abs(xi - x_center) / ((well_right - well_left) / 2)
                meniscus_height = 0.08 - 0.06 * dist_from_center**2
                if yi <= meniscus_height:
                    phi[i, j] = 1.0

    # Plot phase field with colormap
    im = ax.pcolormesh(X, Y, phi, cmap='RdBu_r', vmin=-1, vmax=1, shading='auto', alpha=0.8)

    # Draw triangular mesh overlay (sparse for visibility)
    from matplotlib.tri import Triangulation
    skip = 8
    X_sparse = X[::skip, ::skip].flatten()
    Y_sparse = Y[::skip, ::skip].flatten()
    tri = Triangulation(X_sparse, Y_sparse)
    ax.triplot(tri, color='black', linewidth=0.3, alpha=0.4)

    # Draw interface contour (phi = 0)
    ax.contour(X, Y, phi, levels=[0], colors='white', linewidths=2)

    # Draw well boundaries
    ax.plot([well_left, well_left], [well_bottom, 0], color='black', linewidth=2)
    ax.plot([well_right, well_right], [well_bottom, 0], color='black', linewidth=2)
    ax.plot([well_left, well_right], [well_bottom, well_bottom], color='black', linewidth=2)
    ax.plot([0, well_left], [0, 0], color='black', linewidth=2)
    ax.plot([well_right, domain_width], [0, 0], color='black', linewidth=2)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, label='Phase field φ', shrink=0.8)
    cbar.set_ticks([-1, 0, 1])
    cbar.set_ticklabels(['Air (-1)', 'Interface', 'Encre (+1)'])

    ax.set_xlim(-0.02, domain_width + 0.02)
    ax.set_ylim(y_min - 0.02, 0.35)
    ax.set_xlabel('x [mm]', fontsize=12)
    ax.set_ylabel('y [mm]', fontsize=12)
    ax.set_title('FEM Phase-Field - Goutte étalée (état final)\nMaillage triangulaire + champ de phase φ', fontsize=13)
    ax.set_aspect('equal')

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {output_path}")
    plt.close()


def generate_vof_with_droplet(output_path=None):
    """Generate VOF mesh with droplet at final state (alpha field)."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    # Domain parameters
    domain_width = 1.6  # mm
    y_min = -0.13  # mm

    # Create mesh grid for alpha visualization
    n_x, n_y = 80, 35
    dx = domain_width / n_x
    dy = (0.55 - y_min) / n_y

    well_left, well_right = 0.4, 1.2
    well_bottom = y_min

    # Draw cells with alpha coloring
    for i in range(n_x):
        for j in range(n_y):
            x0 = i * dx
            y0 = y_min + j * dy
            x1 = x0 + dx
            y1 = y0 + dy
            x_center = (x0 + x1) / 2
            y_center = (y0 + y1) / 2

            # Determine alpha (0 = air, 1 = ink)
            alpha = 0
            if well_left <= x_center <= well_right and well_bottom <= y_center <= 0.05:
                alpha = 1.0
            elif well_left <= x_center <= well_right and 0.05 < y_center <= 0.12:
                # Curved meniscus
                x_rel = (x_center - well_left) / (well_right - well_left)
                meniscus = 0.12 - 0.07 * (2*x_rel - 1)**2
                if y_center <= meniscus:
                    alpha = 1.0

            # Color based on alpha
            if alpha > 0.5:
                color = plt.cm.Blues(0.7)
            else:
                color = 'white'

            rect = plt.Rectangle((x0, y0), dx, dy, linewidth=0.3,
                                 edgecolor='gray', facecolor=color, alpha=0.8)
            ax.add_patch(rect)

    # Draw well boundaries
    ax.plot([well_left, well_left], [well_bottom, 0], color='red', linewidth=2.5, label='Parois puit')
    ax.plot([well_right, well_right], [well_bottom, 0], color='red', linewidth=2.5)
    ax.plot([well_left, well_right], [well_bottom, well_bottom], color='red', linewidth=2.5)
    ax.plot([0, well_left], [0, 0], color='black', linewidth=2)
    ax.plot([well_right, domain_width], [0, 0], color='black', linewidth=2)

    ax.set_xlim(-0.02, domain_width + 0.02)
    ax.set_ylim(y_min - 0.02, 0.35)
    ax.set_xlabel('x [mm]', fontsize=12)
    ax.set_ylabel('y [mm]', fontsize=12)
    ax.set_title('VOF (OpenFOAM) - Goutte étalée (état final)\nMaillage hexaédrique + fraction volumique α', fontsize=13)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')

    # Add legend for alpha
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=plt.cm.Blues(0.7), edgecolor='gray', label='Encre (α=1)'),
                      Patch(facecolor='white', edgecolor='gray', label='Air (α=0)')]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {output_path}")
    plt.close()


def generate_lbm_with_droplet(output_path=None):
    """Generate LBM grid with droplet at final state (density field)."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    # Domain parameters
    domain_width = 1.2  # mm
    domain_height = 0.63  # mm
    y_min = -0.13  # mm
    dx = 0.005  # mm = 5 µm

    nx = int(domain_width / dx)
    ny = int(domain_height / dx)

    # Create density field
    X, Y = np.meshgrid(np.linspace(0, domain_width, nx),
                       np.linspace(y_min, y_min + domain_height, ny))
    rho = 90 * np.ones_like(X)  # Air density

    well_left, well_right = 0.2, 1.0
    well_bottom = y_min

    # Fill well with liquid density
    for i in range(ny):
        for j in range(nx):
            xi, yi = X[i, j], Y[i, j]
            if well_left <= xi <= well_right and well_bottom <= yi <= 0.03:
                rho[i, j] = 458  # Liquid density
            elif well_left + 0.05 <= xi <= well_right - 0.05 and 0.03 < yi <= 0.08:
                # Curved top
                x_rel = (xi - well_left) / (well_right - well_left)
                meniscus = 0.08 - 0.05 * (2*x_rel - 1)**2
                if yi <= meniscus:
                    rho[i, j] = 458

    # Plot density field
    im = ax.pcolormesh(X, Y, rho, cmap='Blues', vmin=90, vmax=458, shading='auto')

    # Draw grid lines (sparse)
    skip = 8
    for i in range(0, nx + 1, skip):
        x = i * dx
        ax.axvline(x=x, color='gray', linewidth=0.2, alpha=0.5)
    for j in range(0, ny + 1, skip):
        y = y_min + j * dx
        ax.axhline(y=y, color='gray', linewidth=0.2, alpha=0.5)

    # Draw well boundaries
    ax.plot([well_left, well_left], [well_bottom, 0], color='red', linewidth=2.5)
    ax.plot([well_right, well_right], [well_bottom, 0], color='red', linewidth=2.5)
    ax.plot([well_left, well_right], [well_bottom, well_bottom], color='red', linewidth=2.5)
    ax.plot([0, well_left], [0, 0], color='black', linewidth=2)
    ax.plot([well_right, domain_width], [0, 0], color='black', linewidth=2)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, label='Densité ρ [l.u.]', shrink=0.8)

    ax.set_xlim(-0.02, domain_width + 0.02)
    ax.set_ylim(y_min - 0.02, 0.35)
    ax.set_xlabel('x [mm]', fontsize=12)
    ax.set_ylabel('y [mm]', fontsize=12)
    ax.set_title('LBM Shan-Chen - Goutte étalée (état final)\nGrille uniforme + champ de densité ρ', fontsize=13)
    ax.set_aspect('equal')

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {output_path}")
    plt.close()


def generate_sph_with_droplet(output_path=None):
    """Generate SPH particles at final state (spread in well)."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    # Domain parameters
    domain_width = 1.6  # mm
    y_min = -0.13  # mm
    dp = 0.008  # mm = 8 µm particle spacing

    well_left, well_right = 0.4, 1.2
    well_bottom = y_min

    # Generate particles in the well (final spread state)
    particles_x = []
    particles_y = []

    # Fill bottom of well
    for xi in np.arange(well_left + dp, well_right - dp, dp):
        for yi in np.arange(well_bottom + dp, 0.02, dp):
            particles_x.append(xi)
            particles_y.append(yi)

    # Add meniscus particles
    for xi in np.arange(well_left + dp*2, well_right - dp*2, dp):
        x_rel = (xi - well_left) / (well_right - well_left)
        max_y = 0.06 - 0.04 * (2*x_rel - 1)**2
        for yi in np.arange(0.02, max_y, dp):
            particles_x.append(xi)
            particles_y.append(yi)

    # Plot particles
    ax.scatter(particles_x, particles_y, s=3, c='#1f77b4', alpha=0.8, label=f'Particules (n={len(particles_x)})')

    # Draw well boundaries
    ax.plot([0, well_left], [0, 0], color='black', linewidth=2)
    ax.plot([well_right, domain_width], [0, 0], color='black', linewidth=2)
    ax.plot([well_left, well_left], [0, well_bottom], color='black', linewidth=2)
    ax.plot([well_right, well_right], [0, well_bottom], color='black', linewidth=2)
    ax.plot([well_left, well_right], [well_bottom, well_bottom], color='black', linewidth=2)

    ax.set_xlim(-0.02, domain_width + 0.02)
    ax.set_ylim(y_min - 0.02, 0.25)
    ax.set_xlabel('x [mm]', fontsize=12)
    ax.set_ylabel('y [mm]', fontsize=12)
    ax.set_title('SPH - Goutte étalée (état final)\nParticules lagrangiennes dans le puit', fontsize=13)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {output_path}")
    plt.close()


def main():
    """Generate all mesh comparison images."""
    print("=" * 60)
    print("Generating mesh comparison images for Streamlit app")
    print("=" * 60)

    # FEM mesh (empty)
    print("\n[1/8] Generating FEM triangular mesh (empty)...")
    fem_mesh_path = Path("/home/erikeo29/17_RD_Ag_AgCl/12_AgCl Fenicsx/02_AgCl_FEniCSx_CC2/mesh/agcl_v3_medium.msh")
    generate_fem_mesh_image(
        mesh_path=fem_mesh_path if fem_mesh_path.exists() else None,
        output_path=OUTPUT_DIR / "mesh_fem.png"
    )

    # VOF mesh (empty)
    print("\n[2/8] Generating VOF hexahedral mesh (empty)...")
    generate_vof_mesh_image(
        output_path=OUTPUT_DIR / "mesh_vof.png"
    )

    # LBM grid (empty)
    print("\n[3/8] Generating LBM uniform grid (empty)...")
    generate_lbm_grid_image(
        output_path=OUTPUT_DIR / "mesh_lbm.png"
    )

    # SPH particles (initial)
    print("\n[4/8] Generating SPH particle distribution (initial)...")
    generate_sph_particles_image(
        output_path=OUTPUT_DIR / "mesh_sph.png"
    )

    # FEM with droplet
    print("\n[5/8] Generating FEM with droplet (final state)...")
    generate_fem_with_droplet(
        output_path=OUTPUT_DIR / "droplet_fem.png"
    )

    # VOF with droplet
    print("\n[6/8] Generating VOF with droplet (final state)...")
    generate_vof_with_droplet(
        output_path=OUTPUT_DIR / "droplet_vof.png"
    )

    # LBM with droplet
    print("\n[7/8] Generating LBM with droplet (final state)...")
    generate_lbm_with_droplet(
        output_path=OUTPUT_DIR / "droplet_lbm.png"
    )

    # SPH with droplet
    print("\n[8/8] Generating SPH with droplet (final state)...")
    generate_sph_with_droplet(
        output_path=OUTPUT_DIR / "droplet_sph.png"
    )

    print("\n" + "=" * 60)
    print("All images generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
