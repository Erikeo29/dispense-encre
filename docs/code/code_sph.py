#!/usr/bin/env python3
"""
AgCl Droplet Spreading Simulation using SPH with Solid Substrate
=================================================================

Simulates the spreading of an AgCl ink droplet on a solid substrate using
Smoothed Particle Hydrodynamics (SPH) with surface tension and contact angle.

Features:
- Two-phase flow (droplet + air)
- Surface tension (Morris/Adami formulations)
- Solid substrate with contact angle boundary condition
- Configurable via YAML or command line

References:
- Morris (2000): Surface tension with SPH, IJNMF 33, pp 333-353
- Adami et al. (2012): Wall boundary condition, JCP 231, pp 7057-7075
- Breinlinger et al. (2013): Contact angle in SPH

Usage:
    python3 droplet_spreading.py --tf 0.1 --sigma 0.04 --contact-angle 45
    python3 droplet_spreading.py --help

"""
import os
import sys
import numpy as np
import yaml

from pysph.base.utils import get_particle_array
from pysph.base.kernels import QuinticSpline, CubicSpline
from pysph.solver.application import Application
from pysph.solver.solver import Solver
from pysph.sph.integrator import PECIntegrator
from pysph.sph.integrator_step import TransportVelocityStep
from pysph.sph.equation import Group, Equation

# Surface tension equations
from pysph.sph.surface_tension import (
    SmoothedColor, MorrisColorGradient, InterfaceCurvatureFromNumberDensity,
    ShadlooYildizSurfaceTensionForce, ColorGradientUsingNumberDensity
)
from pysph.sph.gas_dynamics.basic import ScaleSmoothingLength

# Transport velocity formulation
from pysph.sph.wc.transport_velocity import (
    SummationDensity, StateEquation,
    MomentumEquationPressureGradient, MomentumEquationViscosity,
    MomentumEquationArtificialStress, SolidWallPressureBC, SolidWallNoSlipBC
)


class WallAdhesionForce(Equation):
    """
    Apply wall adhesion force to impose contact angle.
    For flat substrate at y=0 (legacy mode).
    """

    def __init__(self, dest, sources, theta, sigma, delta=1.5, alpha=25.0):
        self.theta_rad = np.radians(theta)
        self.cos_theta = np.cos(self.theta_rad)
        self.sigma = sigma
        self.delta = delta
        self.alpha = alpha
        super().__init__(dest, sources)
        print(f"[WallAdhesionForce] theta={theta}°, cos_theta={self.cos_theta:.3f}, sigma={sigma}, alpha={alpha}")

    def initialize(self, d_idx, d_x, d_y, d_h, d_au, d_av):
        dist = d_y[d_idx]
        h = d_h[d_idx]
        if dist < self.delta * h and dist > 0:
            wall_factor = (1.0 - dist / (self.delta * h))
            F_mag = self.alpha * self.sigma * abs(self.cos_theta) * wall_factor / h
            x_center = 0.8e-3
            dx_from_center = d_x[d_idx] - x_center
            if abs(dx_from_center) > 1e-10:
                direction = 1.0 if dx_from_center > 0 else -1.0
                if self.cos_theta > 0:
                    d_au[d_idx] += direction * F_mag
                else:
                    d_au[d_idx] -= direction * F_mag


class CavityAdhesionForce(Equation):
    """
    Apply wall adhesion force for cavity geometry with multiple contact angles.

    Cavity geometry:
    - Left ledge/platform: x in [x_left, x_wall_left], y=0, theta=theta_left_ledge
    - Right ledge/platform: x in [x_wall_right, x_right], y=0, theta=theta_right_ledge
    - Left wall: x=x_wall_left, y in [y_bottom, 0], theta=theta_left
    - Right wall: x=x_wall_right, y in [y_bottom, 0], theta=theta_right
    - Bottom: x in [x_wall_left, x_wall_right], y=y_bottom, theta=theta_bottom
    """

    def __init__(self, dest, sources, sigma,
                 x_wall_left=0.4e-3, x_wall_right=1.2e-3, y_bottom=-0.13e-3,
                 theta_bottom=30.0, theta_left=45.0, theta_right=90.0,
                 theta_left_ledge=41.0, theta_right_ledge=90.0,
                 delta=1.5, alpha=25.0):
        self.sigma = sigma
        self.x_wall_left = x_wall_left
        self.x_wall_right = x_wall_right
        self.y_bottom = y_bottom
        # Store cos(theta) for each surface
        self.cos_bottom = np.cos(np.radians(theta_bottom))
        self.cos_left = np.cos(np.radians(theta_left))
        self.cos_right = np.cos(np.radians(theta_right))
        self.cos_left_ledge = np.cos(np.radians(theta_left_ledge))
        self.cos_right_ledge = np.cos(np.radians(theta_right_ledge))
        self.delta = delta
        self.alpha = alpha
        super().__init__(dest, sources)
        print(f"[CavityAdhesionForce] alpha={alpha}, bottom={theta_bottom}°, left_wall={theta_left}°, right_wall={theta_right}°")
        print(f"[CavityAdhesionForce] left_platform={theta_left_ledge}°, right_platform={theta_right_ledge}°")

    def initialize(self, d_idx, d_x, d_y, d_h, d_au, d_av, d_scolor):
        """
        Apply adhesion force only to INTERFACE particles (not bulk).
        scolor ~ 0.5 = interface, scolor ~ 0 or 1 = bulk
        """
        # CRITICAL FIX: Only apply to interface particles (scolor between 0.05 and 0.95)
        scolor = d_scolor[d_idx]

        # Only process interface particles (skip bulk air and droplet)
        if scolor >= 0.05 and scolor <= 0.95:
            x = d_x[d_idx]
            y = d_y[d_idx]
            h = d_h[d_idx]

            # Determine which wall the particle is near and apply appropriate force
            delta_h = self.delta * h

            # Check proximity to each wall
            dist_to_bottom = y - self.y_bottom
            dist_to_left_wall = x - self.x_wall_left
            dist_to_right_wall = self.x_wall_right - x

            # Inside cavity region?
            in_cavity_x = (x > self.x_wall_left) and (x < self.x_wall_right)
            in_cavity_y = (y > self.y_bottom) and (y < 0)

            # Bottom wall (inside cavity, near bottom)
            if in_cavity_x and dist_to_bottom < delta_h and dist_to_bottom > 0:
                wall_factor = 1.0 - dist_to_bottom / delta_h
                F_mag = self.alpha * self.sigma * abs(self.cos_bottom) * wall_factor / h
                # Direction based on x position relative to cavity center
                x_center = (self.x_wall_left + self.x_wall_right) / 2
                dx = x - x_center
                if abs(dx) > 1e-10:
                    direction = 1.0 if dx > 0 else -1.0
                    if self.cos_bottom > 0:  # Hydrophilic: spread outward
                        d_au[d_idx] += direction * F_mag
                    else:  # Hydrophobic: contract inward
                        d_au[d_idx] -= direction * F_mag

            # Left vertical wall (inside cavity, near left wall)
            if in_cavity_y and dist_to_left_wall < delta_h and dist_to_left_wall > 0:
                wall_factor = 1.0 - dist_to_left_wall / delta_h
                F_mag = self.alpha * self.sigma * abs(self.cos_left) * wall_factor / h
                # Vertical force based on y position
                y_center = self.y_bottom / 2
                dy = y - y_center
                if abs(dy) > 1e-10:
                    direction = 1.0 if dy > 0 else -1.0
                    if self.cos_left > 0:  # Hydrophilic: spread along wall
                        d_av[d_idx] += direction * F_mag
                    else:
                        d_av[d_idx] -= direction * F_mag

            # Right vertical wall (inside cavity, near right wall)
            if in_cavity_y and dist_to_right_wall < delta_h and dist_to_right_wall > 0:
                wall_factor = 1.0 - dist_to_right_wall / delta_h
                F_mag = self.alpha * self.sigma * abs(self.cos_right) * wall_factor / h
                y_center = self.y_bottom / 2
                dy = y - y_center
                if abs(dy) > 1e-10:
                    direction = 1.0 if dy > 0 else -1.0
                    if self.cos_right > 0:
                        d_av[d_idx] += direction * F_mag
                    else:
                        d_av[d_idx] -= direction * F_mag

            # Left ledge/platform (x < x_wall_left, near y=0)
            if x < self.x_wall_left and y > 0 and y < delta_h:
                wall_factor = 1.0 - y / delta_h
                F_mag = self.alpha * self.sigma * abs(self.cos_left_ledge) * wall_factor / h
                # Direction: spread toward left edge of domain
                if self.cos_left_ledge > 0:  # Hydrophilic: spread left
                    d_au[d_idx] -= F_mag
                else:  # Hydrophobic: contract right
                    d_au[d_idx] += F_mag

            # Right ledge/platform (x > x_wall_right, near y=0)
            if x > self.x_wall_right and y > 0 and y < delta_h:
                wall_factor = 1.0 - y / delta_h
                F_mag = self.alpha * self.sigma * abs(self.cos_right_ledge) * wall_factor / h
                # Direction: spread toward right edge of domain
                if self.cos_right_ledge > 0:  # Hydrophilic: spread right
                    d_au[d_idx] += F_mag
                else:  # Hydrophobic: contract left
                    d_au[d_idx] -= F_mag


class WallRepulsionForce(Equation):
    """
    Apply soft repulsion to prevent wall penetration (flat substrate at y=0).
    """

    def __init__(self, dest, sources, r0=None, k=5000.0, n=2.0):
        # Use sentinel value -1.0 for None (computed at runtime from h)
        self.r0_value = r0 if r0 is not None else -1.0
        self.k = k
        self.n = n
        super().__init__(dest, sources)
        print(f"[WallRepulsionForce] k={k:.1e}, n={n}, r0={r0}")

    def initialize(self, d_idx, d_y, d_h, d_av):
        y = d_y[d_idx]
        h = d_h[d_idx]
        # Use precomputed r0_value or compute from h if sentinel
        r0 = self.r0_value if self.r0_value > 0 else 0.5 * h
        if y < r0:
            if y <= 0:
                F_repulsion = self.k * 10.0
            else:
                ratio = 1.0 - y / r0
                F_repulsion = self.k * (ratio ** self.n)
            d_av[d_idx] += F_repulsion


class CavityRepulsionForce(Equation):
    """
    Apply soft repulsion for cavity geometry - prevents penetration of all walls.

    Cavity walls:
    - Bottom: y = y_bottom
    - Left wall: x = x_wall_left (for y < 0)
    - Right wall: x = x_wall_right (for y < 0)
    - Left ledge: y = 0 (for x < x_wall_left)
    - Right ledge: y = 0 (for x > x_wall_right)
    """

    def __init__(self, dest, sources,
                 x_wall_left=0.4e-3, x_wall_right=1.2e-3, y_bottom=-0.13e-3,
                 r0=None, k=5000.0, n=2.0):
        self.x_wall_left = x_wall_left
        self.x_wall_right = x_wall_right
        self.y_bottom = y_bottom
        # Use sentinel value -1.0 for None (computed at runtime from h)
        self.r0_value = r0 if r0 is not None else -1.0
        self.k = k
        self.n = n
        super().__init__(dest, sources)
        print(f"[CavityRepulsionForce] cavity x=[{x_wall_left*1e3:.2f}, {x_wall_right*1e3:.2f}]mm, y_bottom={y_bottom*1e3:.2f}mm")

    def initialize(self, d_idx, d_x, d_y, d_h, d_au, d_av):
        x = d_x[d_idx]
        y = d_y[d_idx]
        h = d_h[d_idx]
        # Use precomputed r0_value or compute from h if sentinel
        r0 = self.r0_value if self.r0_value > 0 else 0.5 * h

        # Determine region and apply appropriate repulsion
        in_cavity_x = (x > self.x_wall_left) and (x < self.x_wall_right)

        # Bottom wall repulsion (only inside cavity x-range)
        if in_cavity_x:
            dist_to_bottom = y - self.y_bottom
            if dist_to_bottom < r0:
                if dist_to_bottom <= 0:
                    F_repulsion = self.k * 10.0
                else:
                    ratio = 1.0 - dist_to_bottom / r0
                    F_repulsion = self.k * (ratio ** self.n)
                d_av[d_idx] += F_repulsion  # Push up

        # Left wall repulsion (only inside cavity y-range)
        if y < 0 and y > self.y_bottom:
            dist_to_left = x - self.x_wall_left
            if dist_to_left < r0:
                if dist_to_left <= 0:
                    F_repulsion = self.k * 10.0
                else:
                    ratio = 1.0 - dist_to_left / r0
                    F_repulsion = self.k * (ratio ** self.n)
                d_au[d_idx] += F_repulsion  # Push right

        # Right wall repulsion (only inside cavity y-range)
        if y < 0 and y > self.y_bottom:
            dist_to_right = self.x_wall_right - x
            if dist_to_right < r0:
                if dist_to_right <= 0:
                    F_repulsion = self.k * 10.0
                else:
                    ratio = 1.0 - dist_to_right / r0
                    F_repulsion = self.k * (ratio ** self.n)
                d_au[d_idx] -= F_repulsion  # Push left

        # Left ledge repulsion (x < x_wall_left, near y=0)
        if x < self.x_wall_left:
            if y < r0:
                if y <= 0:
                    F_repulsion = self.k * 10.0
                else:
                    ratio = 1.0 - y / r0
                    F_repulsion = self.k * (ratio ** self.n)
                d_av[d_idx] += F_repulsion

        # Right ledge repulsion (x > x_wall_right, near y=0)
        if x > self.x_wall_right:
            if y < r0:
                if y <= 0:
                    F_repulsion = self.k * 10.0
                else:
                    ratio = 1.0 - y / r0
                    F_repulsion = self.k * (ratio ** self.n)
                d_av[d_idx] += F_repulsion


class ContactAngleCorrection(Equation):
    """
    Legacy normal correction (disabled - use WallAdhesionForce).

    Based on Breinlinger et al. (2013) approach:
    Near the wall, the interface normal is rotated to match the desired
    contact angle theta measured from the solid surface.

    The corrected normal n' is computed as:
    n' = n_wall * cos(theta) + n_tangent * sin(theta)

    where n_wall is the wall normal (pointing into fluid) and n_tangent
    is perpendicular to it in the interface plane.
    """

    def __init__(self, dest, sources, theta, wall_normal_y=1.0, delta=2.0):
        """
        Parameters:
        -----------
        theta : float
            Contact angle in degrees (measured from solid surface)
        wall_normal_y : float
            Y-component of wall normal (1.0 for bottom wall)
        delta : float
            Distance (in smoothing lengths) within which correction applies
        """
        self.theta_rad = np.radians(theta)
        self.cos_theta = np.cos(self.theta_rad)
        self.sin_theta = np.sin(self.theta_rad)
        self.wall_ny = wall_normal_y
        self.wall_nx = 0.0
        self.delta = delta
        super().__init__(dest, sources)

    def loop(self, d_idx, d_x, d_y, d_h, d_nx, d_ny, d_color):
        # Only apply to interface particles (color between 0.1 and 0.9)
        if 0.05 < d_color[d_idx] < 0.95:
            # Distance from wall (assuming bottom wall at y=0)
            dist_to_wall = d_y[d_idx]

            # Apply correction only within delta*h of wall
            if dist_to_wall < self.delta * d_h[d_idx]:
                # Current interface normal
                nx = d_nx[d_idx]
                ny = d_ny[d_idx]
                n_mag = (nx*nx + ny*ny)**0.5

                if n_mag > 1e-10:
                    # Normalize
                    nx = nx / n_mag
                    ny = ny / n_mag

                    # Wall normal (pointing into fluid, i.e., upward for bottom wall)
                    wnx = self.wall_nx
                    wny = self.wall_ny

                    # Tangent to wall (perpendicular to wall normal, in interface direction)
                    # Choose direction based on current normal
                    if nx >= 0:
                        tnx = 1.0
                    else:
                        tnx = -1.0
                    tny = 0.0

                    # Corrected normal: n' = wall_normal * cos(theta) + tangent * sin(theta)
                    # For contact angle measured from wall into liquid
                    new_nx = wnx * self.cos_theta + tnx * self.sin_theta
                    new_ny = wny * self.cos_theta + tny * self.sin_theta

                    # Smooth blending based on distance to wall
                    blend = 1.0 - dist_to_wall / (self.delta * d_h[d_idx])
                    blend = max(0.0, min(1.0, blend))

                    # Apply blended correction
                    d_nx[d_idx] = (1 - blend) * nx + blend * new_nx
                    d_ny[d_idx] = (1 - blend) * ny + blend * new_ny


class ComputeStrainRate(Equation):
    """
    Compute velocity gradient tensor and strain rate magnitude for Carreau model.
    Uses SPH gradient of velocity field.
    """

    def initialize(self, d_idx, d_strain_rate):
        d_strain_rate[d_idx] = 0.0

    def loop(self, d_idx, s_idx, d_strain_rate, d_rho, s_m, s_rho,
             d_u, d_v, s_u, s_v, DWIJ):
        # Velocity difference
        du = s_u[s_idx] - d_u[d_idx]
        dv = s_v[s_idx] - d_v[d_idx]

        # Volume of source particle
        Vj = s_m[s_idx] / s_rho[s_idx]

        # Gradient contributions (symmetric part of velocity gradient)
        # du/dx, du/dy, dv/dx, dv/dy
        dudx = du * DWIJ[0] * Vj
        dudy = du * DWIJ[1] * Vj
        dvdx = dv * DWIJ[0] * Vj
        dvdy = dv * DWIJ[1] * Vj

        # Strain rate tensor (symmetric): e_ij = 0.5 * (du_i/dx_j + du_j/dx_i)
        # e_xx = du/dx, e_yy = dv/dy
        # e_xy = 0.5 * (du/dy + dv/dx)
        exx = dudx
        eyy = dvdy
        exy = 0.5 * (dudy + dvdx)

        # Second invariant of strain rate tensor: γ̇ = sqrt(2 * e_ij * e_ij)
        # For 2D: γ̇ = sqrt(2 * (e_xx² + e_yy² + 2*e_xy²))
        d_strain_rate[d_idx] += 2.0 * (exx*exx + eyy*eyy + 2.0*exy*exy)

    def post_loop(self, d_idx, d_strain_rate):
        # Take square root to get magnitude
        if d_strain_rate[d_idx] > 0:
            d_strain_rate[d_idx] = (d_strain_rate[d_idx]) ** 0.5


class CarreauViscosity(Equation):
    """
    Apply Carreau shear-thinning rheology model.

    η = η_inf + (η_0 - η_inf) * [1 + (λ * γ̇)²]^((n-1)/2)

    Parameters:
    -----------
    eta0 : Zero-shear viscosity [Pa.s]
    eta_inf : Infinite-shear viscosity [Pa.s]
    lam : Time constant λ [s]
    n : Power-law index (n < 1 for shear-thinning)
    rho0 : Reference density for kinematic viscosity conversion
    """

    def __init__(self, dest, sources, eta0, eta_inf, lam, n, rho0):
        self.eta0 = eta0
        self.eta_inf = eta_inf
        self.lam = lam
        self.n = n
        self.rho0 = rho0
        super().__init__(dest, sources)
        print(f"[CarreauViscosity] η₀={eta0}, η∞={eta_inf}, λ={lam}, n={n}")

    def loop(self, d_idx, d_nu, d_strain_rate):
        gamma_dot = d_strain_rate[d_idx]

        # Carreau model
        lambda_gamma = self.lam * gamma_dot
        factor = 1.0 + lambda_gamma * lambda_gamma
        exponent = 0.5 * (self.n - 1.0)

        # Dynamic viscosity
        eta = self.eta_inf + (self.eta0 - self.eta_inf) * (factor ** exponent)

        # Convert to kinematic viscosity
        d_nu[d_idx] = eta / self.rho0


class DropletSpreading(Application):
    """
    SPH simulation of droplet spreading on solid substrate with contact angle.
    """

    def initialize(self):
        """Set default parameters."""
        # Domain parameters
        self.domain_width = 1.6e-3      # [m] 1.6 mm
        self.domain_height = 0.8e-3     # [m] 0.8 mm

        # Droplet parameters
        self.droplet_radius = 0.15e-3   # [m] 0.15 mm
        self.droplet_x = 0.8e-3         # [m] Center x
        self.droplet_y = 0.3e-3         # [m] Initial height above substrate
        self.droplet_falling = True     # Start droplet in the air

        # Physical properties
        self.rho_ink = 3000.0           # [kg/m³]
        self.sigma = 0.040              # [N/m] Surface tension
        self.nu = 5e-4                  # [m²/s] Kinematic viscosity
        self.contact_angle = 45.0       # [degrees] Contact angle
        self.gy = -9.81                 # [m/s²] Gravity

        # Numerical parameters
        self.dx = 1e-5                  # [m] Particle spacing
        self.hdx = 1.3                  # h/dx ratio
        self.c0 = 10.0                  # [m/s] Speed of sound

        # Time parameters
        self.tf = 0.01                  # [s] Final time

        # Surface tension scheme
        self.scheme_name = 'morris'
        self.factor1 = 0.8

        # Substrate parameters
        self.substrate_layers = 3       # Number of solid particle layers

        # Cavity parameters (disabled by default)
        self.use_cavity = False
        self.cavity_x_left = 0.2e-3     # Left edge of domain
        self.cavity_x_wall_left = 0.4e-3   # Left wall of cavity
        self.cavity_x_wall_right = 1.2e-3  # Right wall of cavity
        self.cavity_x_right = 1.4e-3    # Right edge of domain
        self.cavity_y_bottom = -0.13e-3 # Bottom of cavity
        self.cavity_theta_bottom = 30.0  # Contact angle at bottom
        self.cavity_theta_left = 45.0    # Contact angle at left wall
        self.cavity_theta_right = 90.0   # Contact angle at right wall
        self.cavity_theta_left_ledge = 41.0   # Contact angle at left platform
        self.cavity_theta_right_ledge = 90.0  # Contact angle at right platform
        self.adhesion_alpha = 15.0            # Adhesion force strength (CD recommends 15)

        # Carreau rheology parameters (shear-thinning)
        self.use_carreau = False
        self.carreau_eta0 = 0.5        # Zero-shear viscosity [Pa.s]
        self.carreau_eta_inf = 0.167   # Infinite-shear viscosity [Pa.s]
        self.carreau_lambda = 0.15     # Time constant [s]
        self.carreau_n = 0.7           # Power-law index

    def add_user_options(self, group):
        """Add command-line options."""
        group.add_argument("--rho0", type=float, dest="rho0", default=None)
        group.add_argument("--sigma", type=float, dest="sigma", default=None)
        group.add_argument("--nu", type=float, dest="nu", default=None)
        group.add_argument("--dx", type=float, dest="dx", default=None)
        group.add_argument("--hdx", type=float, dest="hdx", default=None)
        group.add_argument("--droplet-radius", type=float, dest="droplet_radius", default=None)
        group.add_argument("--contact-angle", type=float, dest="contact_angle", default=None,
                          help="Contact angle in degrees")
        group.add_argument("--falling", action="store_true", dest="falling",
                          help="Start droplet in the air (falling mode)")
        group.add_argument("--no-falling", action="store_false", dest="falling",
                          help="Start droplet on substrate")
        group.add_argument("--droplet-height", type=float, dest="droplet_height", default=None,
                          help="Initial droplet height above substrate [m]")
        group.add_argument("--st-scheme", type=str, dest="st_scheme", default=None,
                          choices=['morris', 'tvf', 'adami_stress', 'adami', 'shadloo'])
        group.add_argument("--config", type=str, dest="config_file", default=None)
        group.add_argument("--cavity", action="store_true", dest="use_cavity",
                          help="Use cavity geometry instead of flat substrate")
        group.add_argument("--carreau", action="store_true", dest="use_carreau",
                          help="Enable Carreau shear-thinning rheology")
        group.add_argument("--eta0", type=float, dest="carreau_eta0", default=None,
                          help="Carreau zero-shear viscosity [Pa.s]")
        group.add_argument("--theta-left-wall", type=float, dest="theta_left_wall", default=None,
                          help="Contact angle at left vertical wall [degrees]")
        group.add_argument("--theta-left-platform", type=float, dest="theta_left_platform", default=None,
                          help="Contact angle at left platform/ledge [degrees]")
        group.add_argument("--theta-right-platform", type=float, dest="theta_right_platform", default=None,
                          help="Contact angle at right platform/ledge [degrees]")
        group.add_argument("--alpha", type=float, dest="adhesion_alpha", default=None,
                          help="Adhesion force strength (default: 15.0, CD recommendation)")
        group.set_defaults(falling=True, use_cavity=False, use_carreau=False)

    def consume_user_options(self):
        """Process options."""
        # Load config file
        if self.options.config_file and os.path.exists(self.options.config_file):
            with open(self.options.config_file) as f:
                config = yaml.safe_load(f)
            self._apply_config(config)

        # Override with command line
        if self.options.rho0 is not None:
            self.rho_ink = self.options.rho0
        if self.options.sigma is not None:
            self.sigma = self.options.sigma
        if self.options.nu is not None:
            self.nu = self.options.nu
        if self.options.dx is not None:
            self.dx = self.options.dx
        if self.options.hdx is not None:
            self.hdx = self.options.hdx
        if self.options.droplet_radius is not None:
            self.droplet_radius = self.options.droplet_radius
        if self.options.contact_angle is not None:
            self.contact_angle = self.options.contact_angle
        if self.options.st_scheme is not None:
            self.scheme_name = self.options.st_scheme
        if self.options.falling is not None:
            self.droplet_falling = self.options.falling
        if self.options.use_cavity:
            self.use_cavity = True
        if self.options.use_carreau:
            self.use_carreau = True
        if self.options.carreau_eta0 is not None:
            self.carreau_eta0 = self.options.carreau_eta0
        if self.options.theta_left_wall is not None:
            self.cavity_theta_left = self.options.theta_left_wall
        if self.options.theta_left_platform is not None:
            self.cavity_theta_left_ledge = self.options.theta_left_platform
        if self.options.theta_right_platform is not None:
            self.cavity_theta_right_ledge = self.options.theta_right_platform
        if self.options.adhesion_alpha is not None:
            self.adhesion_alpha = self.options.adhesion_alpha

        # Set droplet center position
        # droplet_height is the gap between substrate and BOTTOM of droplet
        # Center = gap + radius
        if self.options.droplet_height is not None:
            gap = self.options.droplet_height
            self.droplet_y = gap + self.droplet_radius

        # If not falling, start on substrate (center at radius height)
        if not self.droplet_falling:
            self.droplet_y = self.droplet_radius

        # Derived quantities
        self.h0 = self.hdx * self.dx
        self.rho0 = self.rho_ink
        self.p0 = self.c0 * self.c0 * self.rho0

        # Time step
        dt_cfl = 0.25 * self.h0 / (1.1 * self.c0)
        dt_viscous = 0.125 * self.h0**2 / max(self.nu, 1e-10)
        dt_surface = np.sqrt(self.rho0 * self.h0**3 / (2 * np.pi * max(self.sigma, 1e-10)))
        self.dt = 0.5 * min(dt_cfl, dt_viscous, dt_surface)

        self.factor2 = 1.0 / self.factor1
        self.epsilon = 0.01 / self.h0

        # Compute effective viscosity for Carreau
        if self.use_carreau:
            # Use zero-shear viscosity for timestep calculation
            self.nu = self.carreau_eta0 / self.rho_ink

        print(f"\n=== SPH Droplet Spreading with {'Cavity' if self.use_cavity else 'Flat Substrate'} ===")
        print(f"Density: {self.rho_ink} kg/m³")
        print(f"Surface tension: {self.sigma} N/m")
        if self.use_cavity:
            print(f"Cavity geometry:")
            print(f"  Bottom: θ={self.cavity_theta_bottom}°, y={self.cavity_y_bottom*1e3:.2f} mm")
            print(f"  Left wall: θ={self.cavity_theta_left}°, x={self.cavity_x_wall_left*1e3:.2f} mm")
            print(f"  Right wall: θ={self.cavity_theta_right}°, x={self.cavity_x_wall_right*1e3:.2f} mm")
            print(f"  Left platform: θ={self.cavity_theta_left_ledge}°")
            print(f"  Right platform: θ={self.cavity_theta_right_ledge}°")
        else:
            print(f"Contact angle: {self.contact_angle}°")
        if self.use_carreau:
            print(f"Carreau rheology:")
            print(f"  η₀={self.carreau_eta0} Pa.s, η∞={self.carreau_eta_inf} Pa.s")
            print(f"  λ={self.carreau_lambda} s, n={self.carreau_n}")
            print(f"  nu (from η₀): {self.nu:.2e} m²/s")
        else:
            print(f"Kinematic viscosity: {self.nu} m²/s")
        print(f"Particle spacing dx: {self.dx*1e6:.1f} µm")
        print(f"Time step dt: {self.dt:.2e} s")
        print(f"Final time tf: {self.tf} s")
        print(f"Falling mode: {self.droplet_falling}")
        if self.droplet_falling:
            gap = self.droplet_y - self.droplet_radius
            print(f"Initial gap (bottom to substrate): {gap*1e3:.2f} mm")
            print(f"Droplet center height: {self.droplet_y*1e3:.2f} mm")
        print()

    def _apply_config(self, config):
        """Apply YAML configuration."""
        if 'sph' in config:
            sph = config['sph']
            if 'dx' in sph:
                self.dx = sph['dx']
            if 'hdx' in sph:
                self.hdx = sph['hdx']
            if 'c0' in sph:
                self.c0 = sph['c0']

        if 'physical' in config:
            phys = config['physical']
            if 'rho_ink' in phys:
                self.rho_ink = phys['rho_ink']
            if 'nu' in phys:
                self.nu = phys['nu']

        if 'surface' in config:
            if 'sigma' in config['surface']:
                self.sigma = config['surface']['sigma']

        if 'contact_angles' in config:
            if 'substrate' in config['contact_angles']:
                self.contact_angle = config['contact_angles']['substrate']

        if 'geometry' in config:
            geom = config['geometry']
            if 'droplet_radius' in geom:
                self.droplet_radius = geom['droplet_radius']
            if 'domain_width' in geom:
                self.domain_width = geom['domain_width']
            if 'domain_height' in geom:
                self.domain_height = geom['domain_height']

        if 'process' in config:
            if 'end_time' in config['process']:
                self.tf = config['process']['end_time']

    def create_particles(self):
        """Create fluid and solid particles."""
        dx = self.dx
        volume = dx * dx

        # =====================================================================
        # Create FLUID particles
        # =====================================================================
        cx = self.droplet_x
        cy = self.droplet_y
        r = self.droplet_radius

        if self.droplet_falling:
            # Create ONLY droplet particles (no air) for falling simulation
            # Use SYMMETRIC grid centered on (cx, cy) to avoid drift
            n_half = int(np.ceil(r / dx))  # Number of particles from center to edge
            x_list = []
            y_list = []
            for i in range(-n_half, n_half + 1):
                xi = cx + i * dx  # Symmetric around cx
                for j in range(-n_half, n_half + 1):
                    yi = cy + j * dx  # Symmetric around cy
                    dist = np.sqrt((xi - cx)**2 + (yi - cy)**2)
                    if dist <= r:
                        x_list.append(xi)
                        y_list.append(yi)
            x_fluid = np.array(x_list)
            y_fluid = np.array(y_list)
        else:
            # Create full domain with air + droplet for spreading simulation
            x_fluid, y_fluid = np.mgrid[
                dx/2:self.domain_width:dx,
                dx/2:self.domain_height:dx
            ]
            x_fluid = x_fluid.ravel()
            y_fluid = y_fluid.ravel()

        n_fluid = len(x_fluid)
        m_fluid = np.ones(n_fluid) * volume * self.rho0
        rho_fluid = np.ones(n_fluid) * self.rho0
        h_fluid = np.ones(n_fluid) * self.h0
        cs_fluid = np.ones(n_fluid) * self.c0

        # Additional properties for surface tension and rheology
        additional_props = [
            'V', 'alpha',
            'color', 'scolor', 'cx', 'cy', 'cz', 'cx2', 'cy2', 'cz2',
            'nx', 'ny', 'nz', 'ddelta',
            'kappa',
            'uhat', 'vhat', 'what', 'auhat', 'avhat', 'awhat',
            'ax', 'ay', 'az', 'wij',
            'vmag2',
            'N', 'wij_sum',
            'pi00', 'pi01', 'pi02', 'pi10', 'pi11', 'pi12',
            'pi20', 'pi21', 'pi22', 'nu',
            'strain_rate'  # For Carreau rheology
        ]

        fluid = get_particle_array(
            name='fluid', x=x_fluid, y=y_fluid, h=h_fluid, m=m_fluid,
            rho=rho_fluid, cs=cs_fluid, additional_props=additional_props
        )

        # Set color: 1 for droplet, 0 for air
        if self.droplet_falling:
            # All particles are droplet in falling mode
            fluid.color[:] = 1.0
        else:
            for i in range(len(x_fluid)):
                dist = np.sqrt((fluid.x[i] - cx)**2 + (fluid.y[i] - cy)**2)
                if dist <= r and fluid.y[i] >= 0:
                    fluid.color[i] = 1.0

        fluid.V[:] = 1.0 / volume
        fluid.nu[:] = self.nu
        fluid.alpha[:] = self.sigma

        fluid.add_output_arrays([
            'V', 'color', 'cx', 'cy', 'nx', 'ny',
            'ddelta', 'kappa', 'N', 'scolor', 'p'
        ])

        # =====================================================================
        # Create SOLID particles (substrate or cavity)
        # =====================================================================
        n_layers = self.substrate_layers
        x_solid_list = []
        y_solid_list = []

        if self.use_cavity:
            # Create cavity geometry
            x_wl = self.cavity_x_wall_left
            x_wr = self.cavity_x_wall_right
            y_bot = self.cavity_y_bottom

            # Left ledge (y=0, x from 0 to x_wall_left)
            for layer in range(n_layers):
                y_layer = -dx/2 - layer * dx
                x_row = np.arange(dx/2, x_wl, dx)
                y_row = np.ones_like(x_row) * y_layer
                x_solid_list.append(x_row)
                y_solid_list.append(y_row)

            # Right ledge (y=0, x from x_wall_right to domain_width)
            for layer in range(n_layers):
                y_layer = -dx/2 - layer * dx
                x_row = np.arange(x_wr + dx/2, self.domain_width, dx)
                y_row = np.ones_like(x_row) * y_layer
                x_solid_list.append(x_row)
                y_solid_list.append(y_row)

            # Bottom of cavity (y=y_bottom, x from x_wall_left to x_wall_right)
            for layer in range(n_layers):
                y_layer = y_bot - dx/2 - layer * dx
                x_row = np.arange(x_wl + dx/2, x_wr, dx)
                y_row = np.ones_like(x_row) * y_layer
                x_solid_list.append(x_row)
                y_solid_list.append(y_row)

            # Left vertical wall (x=x_wall_left, y from y_bottom to 0)
            for layer in range(n_layers):
                x_layer = x_wl - dx/2 - layer * dx
                y_row = np.arange(y_bot + dx/2, 0, dx)
                x_row = np.ones_like(y_row) * x_layer
                x_solid_list.append(x_row)
                y_solid_list.append(y_row)

            # Right vertical wall (x=x_wall_right, y from y_bottom to 0)
            for layer in range(n_layers):
                x_layer = x_wr + dx/2 + layer * dx
                y_row = np.arange(y_bot + dx/2, 0, dx)
                x_row = np.ones_like(y_row) * x_layer
                x_solid_list.append(x_row)
                y_solid_list.append(y_row)

        else:
            # Flat substrate at y=0
            for layer in range(n_layers):
                y_layer = -dx/2 - layer * dx
                x_row = np.arange(dx/2, self.domain_width, dx)
                y_row = np.ones_like(x_row) * y_layer
                x_solid_list.append(x_row)
                y_solid_list.append(y_row)

        x_solid = np.concatenate(x_solid_list)
        y_solid = np.concatenate(y_solid_list)

        n_solid = len(x_solid)
        m_solid = np.ones(n_solid) * volume * self.rho0
        rho_solid = np.ones(n_solid) * self.rho0
        h_solid = np.ones(n_solid) * self.h0
        cs_solid = np.ones(n_solid) * self.c0

        solid = get_particle_array(
            name='solid', x=x_solid, y=y_solid, h=h_solid, m=m_solid,
            rho=rho_solid, cs=cs_solid
        )

        # Add properties needed for wall BC
        solid.add_property('V')
        solid.add_property('wij')
        solid.add_property('p')
        solid.add_property('ax')
        solid.add_property('ay')
        solid.add_property('az')
        # Ghost velocities for no-slip BC
        solid.add_property('ug')
        solid.add_property('vg')
        solid.add_property('wg')

        solid.V[:] = 1.0 / volume
        # Ghost velocities are zero for stationary wall
        solid.ug[:] = 0.0
        solid.vg[:] = 0.0
        solid.wg[:] = 0.0

        n_droplet = np.sum(fluid.color > 0.5)
        n_air = np.sum(fluid.color < 0.5)
        print(f"Particles: {n_fluid} fluid ({n_droplet} droplet, {n_air} air), {n_solid} solid")

        return [fluid, solid]

    def create_solver(self):
        """Create SPH solver."""
        kernel = QuinticSpline(dim=2)

        from pysph.sph.integrator_step import VelocityVerletSymplecticWCSPHStep
        if self.scheme_name == 'shadloo':
            stepper = VelocityVerletSymplecticWCSPHStep()
        else:
            stepper = TransportVelocityStep()

        integrator = PECIntegrator(fluid=stepper)

        solver = Solver(
            kernel=kernel, dim=2, integrator=integrator,
            dt=self.dt, tf=self.tf, adaptive_timestep=False,
            pfreq=100
        )
        return solver

    def create_equations(self):
        """Create SPH equations with surface tension and contact angle."""
        equations = [
            # Group 1: Density summation
            Group(equations=[
                SummationDensity(dest='fluid', sources=['fluid', 'solid']),
            ]),
        ]

        # Carreau rheology: compute strain rate and update viscosity
        if self.use_carreau:
            equations.append(
                Group(equations=[
                    ComputeStrainRate(dest='fluid', sources=['fluid']),
                ])
            )
            equations.append(
                Group(equations=[
                    CarreauViscosity(
                        dest='fluid', sources=None,
                        eta0=self.carreau_eta0,
                        eta_inf=self.carreau_eta_inf,
                        lam=self.carreau_lambda,
                        n=self.carreau_n,
                        rho0=self.rho0
                    ),
                ])
            )

        equations.extend([
            # Group 2: State equation and color smoothing
            Group(equations=[
                StateEquation(dest='fluid', sources=None, rho0=self.rho0,
                             p0=self.p0, b=1.0),
                SmoothedColor(dest='fluid', sources=['fluid']),
            ]),

            # Group 3: Wall boundary condition
            Group(equations=[
                SolidWallPressureBC(dest='solid', sources=['fluid'], b=1.0,
                                   rho0=self.rho0, p0=self.p0, gy=self.gy),
            ]),

            # Group 4: Scale smoothing length for interface detection
            Group(equations=[
                ScaleSmoothingLength(dest='fluid', sources=None, factor=self.factor1)
            ], update_nnps=False),

            # Group 5: Compute color gradient (interface normal)
            Group(equations=[
                MorrisColorGradient(dest='fluid', sources=['fluid'],
                                   epsilon=self.epsilon),
            ]),

            # Group 6: Compute interface curvature
            Group(equations=[
                InterfaceCurvatureFromNumberDensity(
                    dest='fluid', sources=['fluid'],
                    with_morris_correction=True
                ),
            ]),

            # Group 7: Contact angle correction
            Group(equations=[
                ContactAngleCorrection(dest='fluid', sources=None,
                                      theta=self.contact_angle,
                                      wall_normal_y=1.0,
                                      delta=2.0),
            ]),

            # Group 8: Restore smoothing length
            Group(equations=[
                ScaleSmoothingLength(dest='fluid', sources=None, factor=self.factor2)
            ], update_nnps=False),

            # Group 9: Main momentum equations
            Group(equations=[
                MomentumEquationPressureGradient(
                    dest='fluid', sources=['fluid', 'solid'], pb=self.p0,
                    gy=self.gy),
                MomentumEquationViscosity(
                    dest='fluid', sources=['fluid'], nu=self.nu),
                ShadlooYildizSurfaceTensionForce(
                    dest='fluid', sources=None, sigma=self.sigma),
                MomentumEquationArtificialStress(
                    dest='fluid', sources=['fluid']),
                SolidWallNoSlipBC(
                    dest='fluid', sources=['solid'], nu=self.nu),
            ]),

            # Group 10: Wall adhesion force for contact angle (separate group)
            Group(equations=[
                CavityAdhesionForce(
                    dest='fluid', sources=['fluid'],
                    sigma=self.sigma,
                    x_wall_left=self.cavity_x_wall_left,
                    x_wall_right=self.cavity_x_wall_right,
                    y_bottom=self.cavity_y_bottom,
                    theta_bottom=self.cavity_theta_bottom,
                    theta_left=self.cavity_theta_left,
                    theta_right=self.cavity_theta_right,
                    theta_left_ledge=self.cavity_theta_left_ledge,
                    theta_right_ledge=self.cavity_theta_right_ledge,
                    alpha=self.adhesion_alpha,
                ) if self.use_cavity else WallAdhesionForce(
                    dest='fluid', sources=['fluid'],
                    theta=self.contact_angle, sigma=self.sigma),
            ]),

            # Group 11: Wall repulsion force to prevent penetration
            Group(equations=[
                CavityRepulsionForce(
                    dest='fluid', sources=['fluid'],
                    x_wall_left=self.cavity_x_wall_left,
                    x_wall_right=self.cavity_x_wall_right,
                    y_bottom=self.cavity_y_bottom,
                    r0=None, k=5000.0, n=2.0,
                ) if self.use_cavity else WallRepulsionForce(
                    dest='fluid', sources=['fluid'],
                    r0=None, k=5000.0, n=2.0),
            ]),
        ])
        return equations

    def post_process(self, info_file_or_dir):
        """Generate plots and metrics."""
        if self.rank > 0:
            return

        self.read_info(info_file_or_dir)
        if len(self.output_files) == 0:
            return

        self._compute_spreading_metrics()
        self._make_plots()

    def _compute_spreading_metrics(self):
        """Compute spreading diameter and contact angles over time."""
        from pysph.solver.utils import iter_output

        times = []
        spreading_diameters = []
        max_heights = []
        contact_widths = []

        for sd, arrays in iter_output(self.output_files, 'fluid'):
            t = sd['t']
            pa = arrays

            mask = pa.color > 0.5
            if np.sum(mask) == 0:
                continue

            x_drop = pa.x[mask]
            y_drop = pa.y[mask]

            # Spreading diameter
            spread = x_drop.max() - x_drop.min()
            height = y_drop.max()

            # Contact width (particles near substrate)
            near_substrate = y_drop < 2 * self.dx
            if np.sum(near_substrate) > 0:
                x_contact = x_drop[near_substrate]
                contact_width = x_contact.max() - x_contact.min()
            else:
                contact_width = 0

            times.append(t)
            spreading_diameters.append(spread)
            max_heights.append(height)
            contact_widths.append(contact_width)

        metrics = {
            'time': np.array(times),
            'spreading_diameter': np.array(spreading_diameters),
            'max_height': np.array(max_heights),
            'contact_width': np.array(contact_widths)
        }

        fname = os.path.join(self.output_dir, 'spreading_metrics.npz')
        np.savez(fname, **metrics)
        print(f"Metrics saved to {fname}")

        if len(times) > 0:
            print(f"\n=== Final Spreading Metrics ===")
            print(f"Time: {times[-1]:.4f} s")
            print(f"Spreading diameter: {spreading_diameters[-1]*1e3:.3f} mm")
            print(f"Contact width: {contact_widths[-1]*1e3:.3f} mm")
            print(f"Max height: {max_heights[-1]*1e3:.3f} mm")

    def _make_plots(self):
        """Generate visualization."""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
        except ImportError:
            print("Matplotlib not available")
            return

        from pysph.solver.utils import load

        last_output = self.output_files[-1]
        data = load(last_output)
        fluid = data['arrays']['fluid']
        solid = data['arrays']['solid']
        tf = data['solver_data']['t']

        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot solid substrate
        ax.scatter(solid.x*1e3, solid.y*1e3, c='gray', s=3, label='Substrate', alpha=0.8)

        # Plot fluid phases
        droplet = fluid.color > 0.5
        air = ~droplet

        ax.scatter(fluid.x[air]*1e3, fluid.y[air]*1e3, c='lightblue', s=1, alpha=0.2, label='Air')
        ax.scatter(fluid.x[droplet]*1e3, fluid.y[droplet]*1e3, c='darkblue', s=2, label='Droplet')

        ax.set_xlabel('x [mm]')
        ax.set_ylabel('y [mm]')
        ax.set_title(f'Droplet on substrate at t={tf*1e3:.2f} ms (θ={self.contact_angle}°)')
        ax.set_aspect('equal')
        ax.legend(loc='upper right')
        ax.axhline(y=0, color='brown', linewidth=2, label='Substrate surface')

        fig_path = os.path.join(self.output_dir, 'final_state.png')
        plt.savefig(fig_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Figure saved to {fig_path}")


if __name__ == '__main__':
    app = DropletSpreading()
    app.run()
    app.post_process(app.info_filename)
