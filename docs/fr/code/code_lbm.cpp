/*
 * dropletCavity2D.cpp
 * ====================
 * Shan-Chen droplet spreading in a cavity with multiple contact angles
 * With optional Carreau non-Newtonian rheology (shear-thinning)
 *
 * Geometry (thin walls):
 *   y=0    |-------|                              |-------|
 *          |       | θ=60°                  θ=90° |       |
 *          |       |                              |       |
 *   y=-h   |       +------------ θ=30° -----------+       |
 *          0      0.2                       1.0   1.2     x (mm)
 *                  |<------- well (0.8 mm) ------>|
 *
 * Physical dimensions:
 *   - Domain: 1.2 mm x 0.63 mm (x from 0 to 1.2, y from -0.13 to 0.5)
 *   - Well: x = 0.2 to 1.0 mm, depth = 0.13 mm
 *   - Droplet diameter: 300 µm, center at (0.6, 0.3) mm
 *   - Resolution: 5 µm/l.u.
 *
 * Carreau model (optional):
 *   η = η_inf + (η_0 - η_inf) * [1 + (λ * γ̇)²]^((n-1)/2)
 *   τ_local = 3 * ν_local + 0.5, where ν = η/ρ
 */

#include "palabos2D.h"
#include "palabos2D.hh"
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <cmath>
#include <algorithm>

using namespace plb;
using namespace std;

typedef double T;
#define DESCRIPTOR descriptors::ForcedShanChenD2Q9Descriptor

// =============================================================================
// Carreau Parameters Structure
// =============================================================================
struct CarreauParameters {
    T eta0;       // Zero-shear viscosity (Pa.s)
    T etaInf;     // Infinite-shear viscosity (Pa.s)
    T lambda;     // Relaxation time (s in physical, dimensionless in lattice)
    T n;          // Power-law index (n < 1 for shear-thinning)
    T tauMin;     // Minimum tau for stability (> 0.5)
    T tauMax;     // Maximum tau for stability
    T rho_phys;   // Physical density for eta -> nu conversion
    bool enabled; // Whether Carreau is active

    CarreauParameters()
        : eta0(1.5), etaInf(0.167), lambda(0.15), n(0.7),
          tauMin(0.55), tauMax(2.0), rho_phys(3000.0), enabled(false) {}

    // Compute kinematic viscosity from strain rate (in lattice units)
    T computeNu(T gammaDot) const {
        if (!enabled) return (1.0 - 0.5) / 3.0;  // Default nu for tau=1

        // Convert physical viscosities to kinematic (nu = eta / rho)
        T nu0 = eta0 / rho_phys;
        T nuInf = etaInf / rho_phys;

        // Carreau model: nu = nuInf + (nu0 - nuInf) * [1 + (lambda * gammaDot)²]^((n-1)/2)
        T factor = std::pow(1.0 + std::pow(lambda * gammaDot, 2), (n - 1.0) / 2.0);
        return nuInf + (nu0 - nuInf) * factor;
    }

    // Compute tau from strain rate
    T computeTau(T gammaDot) const {
        T nu = computeNu(gammaDot);
        T tau = 3.0 * nu + 0.5;
        return std::max(tauMin, std::min(tauMax, tau));
    }

    // Compute omega from strain rate
    T computeOmega(T gammaDot) const {
        return 1.0 / computeTau(gammaDot);
    }
};

// Global Carreau parameters (set from main)
CarreauParameters gCarreau;

// Physical to lattice conversion
const T dx = 5.0e-3;  // mm per lattice unit (5 µm)

// Physical dimensions (mm)
const T wellDepth_phys = 0.13;
const T platformLeft_phys = 0.2;   // Left platform ends at x = 0.2 mm
const T wellStart_phys = 0.2;      // Well bottom starts at x = 0.2 mm (thin wall)
const T wellEnd_phys = 1.0;        // Well bottom ends at x = 1.0 mm (right wall)
const T domainWidth_phys = 1.2;    // Total domain width
const T domainHeight_phys = 0.80;  // Extended height to prevent boundary effects on droplet

// Lattice dimensions
const plint wellDepth = (plint)(wellDepth_phys / dx);  // 26 l.u.
const plint platformLeft = (plint)(platformLeft_phys / dx);  // 40 l.u.
const plint wellStartX = (plint)(wellStart_phys / dx);  // 40 l.u. (left wall at x = 0.2 mm)
const plint wellEndX = (plint)(wellEnd_phys / dx);  // 200 l.u. (right wall at x = 1.0 mm)
const plint nx = (plint)(domainWidth_phys / dx);  // 240 l.u.
const plint ny = (plint)(domainHeight_phys / dx);  // 126 l.u.

// Contact angles (degrees) - Default values, can be overridden via CLI
T theta_wellBottom = 30.0;        // Well bottom (substrate)
T theta_leftWall = 45.0;          // Left vertical wall
T theta_rightWall = 90.0;         // Right vertical wall
T theta_leftPlatform = 41.0;      // Left platform (critical for migration)
T theta_rightPlatform = 90.0;     // Right platform (neutral)

// =============================================================================
// Wall region enumeration
// =============================================================================
enum WallRegion {
    WALL_NONE = 0,
    WALL_LEFT_PLATFORM,        // Surface horizontale du plateau gauche (angle de contact)
    WALL_LEFT_PLATFORM_SOLID,  // Zone solide interne sous le plateau gauche (neutre)
    WALL_LEFT_VERTICAL,
    WALL_BOTTOM,
    WALL_RIGHT_VERTICAL,
    WALL_RIGHT_PLATFORM,       // Surface horizontale du plateau droit (angle de contact)
    WALL_RIGHT_PLATFORM_SOLID, // Zone solide interne sous le plateau droit (neutre)
    WALL_TOP,
    WALL_SIDE
};

// =============================================================================
// Function to determine wall region for a given cell
// =============================================================================
WallRegion getWallRegion(plint iX, plint iY) {
    // Domain coordinates: y=0 is well bottom, y=wellDepth is platform level
    // Geometry (thin walls):
    //   x < wellStartX (< 40 l.u. = 0.2 mm): left platform region
    //   x = wellStartX (40 l.u. = 0.2 mm): left vertical wall (thin)
    //   wellStartX < x < wellEndX (40-200 l.u. = 0.2-1.0 mm): well region
    //   x = wellEndX (200 l.u. = 1.0 mm): right vertical wall (thin)
    //   x > wellEndX (> 200 l.u. = 1.0 mm): right platform region

    // Top boundary
    if (iY == ny - 1) return WALL_TOP;

    // Side boundaries (domain edges)
    if (iX == 0 || iX == nx - 1) return WALL_SIDE;

    // Left platform floor (y = wellDepth, x <= wellStartX) - include corner!
    if (iY == wellDepth && iX <= wellStartX) return WALL_LEFT_PLATFORM;

    // Right platform floor (y = wellDepth, x >= wellEndX) - include corner!
    if (iY == wellDepth && iX >= wellEndX) return WALL_RIGHT_PLATFORM;

    // Well bottom (y = 0, inside well: wellStartX < x < wellEndX)
    if (iY == 0 && iX > wellStartX && iX < wellEndX) return WALL_BOTTOM;

    // Left vertical wall (x = wellStartX, y < wellDepth) - thin wall, corner goes to platform
    if (iX == wellStartX && iY < wellDepth) return WALL_LEFT_VERTICAL;

    // Right vertical wall (x = wellEndX, y < wellDepth) - thin wall, corner goes to platform
    if (iX == wellEndX && iY < wellDepth) return WALL_RIGHT_VERTICAL;

    // Left platform solid region (x < wellStartX, y < wellDepth)
    // This is INTERNAL solid - must NOT have contact angle applied!
    if (iX < wellStartX && iY < wellDepth) return WALL_LEFT_PLATFORM_SOLID;

    // Right platform solid region (x > wellEndX, y < wellDepth)
    // This is INTERNAL solid - must NOT have contact angle applied!
    if (iX > wellEndX && iY < wellDepth) return WALL_RIGHT_PLATFORM_SOLID;

    return WALL_NONE;
}

// =============================================================================
// Function to compute wall density from contact angle
// =============================================================================
T computeWallDensity(T theta, T rhoGas, T rhoLiq) {
    if (theta >= 90.0) {
        return rhoGas * (180.0 - theta) / 90.0;
    } else {
        return rhoGas + (rhoLiq - rhoGas) * (90.0 - theta) / 90.0;
    }
}

// =============================================================================
// Function to mask internal solid cells for visualization
// This prevents showing high wall density in solid regions as "liquid"
// =============================================================================
void maskInternalSolids(MultiScalarField2D<T>& rho, T rhoGas) {
    for (plint iX = 0; iX < nx; ++iX) {
        for (plint iY = 0; iY < ny; ++iY) {
            WallRegion region = getWallRegion(iX, iY);
            // Mask internal solid regions (not surface cells)
            if (region == WALL_LEFT_PLATFORM_SOLID || region == WALL_RIGHT_PLATFORM_SOLID) {
                rho.get(iX, iY) = rhoGas;  // Show as gas/empty
            }
        }
    }
}

// =============================================================================
// Droplet Initializer
// =============================================================================
template<typename T, template<typename U> class Descriptor>
class DropletInitializer : public BoxProcessingFunctional2D_L<T, Descriptor>
{
public:
    DropletInitializer(T centerX_, T centerY_, T radius_, T rhoIn_, T rhoOut_)
        : centerX(centerX_), centerY(centerY_), radius(radius_),
          rhoIn(rhoIn_), rhoOut(rhoOut_)
    { }

    virtual void process(Box2D domain, BlockLattice2D<T, Descriptor>& lattice)
    {
        for (plint iX = domain.x0; iX <= domain.x1; ++iX) {
            for (plint iY = domain.y0; iY <= domain.y1; ++iY) {
                Cell<T, Descriptor>& cell = lattice.get(iX, iY);
                if (cell.getDynamics().isBoundary()) continue;

                T ddx = (T)iX - centerX;
                T ddy = (T)iY - centerY;
                T dist = sqrt(ddx*ddx + ddy*ddy);

                T interfaceWidth = 4.0;
                T phi = 0.5 * (1.0 - tanh(2.0 * (dist - radius) / interfaceWidth));
                T rho = rhoOut + phi * (rhoIn - rhoOut);

                Array<T, 2> zeroVelocity(0.0, 0.0);
                Array<T, 2> zeroForce(0.0, 0.0);

                iniCellAtEquilibrium(cell, rho, zeroVelocity);

                cell.setExternalField(
                    Descriptor<T>::ExternalField::densityBeginsAt,
                    Descriptor<T>::ExternalField::sizeOfDensity, &rho);
                cell.setExternalField(
                    Descriptor<T>::ExternalField::momentumBeginsAt,
                    Descriptor<T>::ExternalField::sizeOfMomentum, &zeroVelocity[0]);
                cell.setExternalField(
                    Descriptor<T>::ExternalField::forceBeginsAt,
                    Descriptor<T>::ExternalField::sizeOfForce, &zeroForce[0]);
            }
        }
    }

    virtual DropletInitializer<T, Descriptor>* clone() const {
        return new DropletInitializer<T, Descriptor>(*this);
    }

    virtual void getTypeOfModification(std::vector<modif::ModifT>& modified) const {
        modified[0] = modif::staticVariables;
    }

private:
    T centerX, centerY, radius;
    T rhoIn, rhoOut;
};

// =============================================================================
// Gravity Processor
// =============================================================================
template<typename T, template<typename U> class Descriptor>
class SetGravityForce : public BoxProcessingFunctional2D_L<T, Descriptor>
{
public:
    SetGravityForce(T gx_, T gy_) : gx(gx_), gy(gy_) { }

    virtual void process(Box2D domain, BlockLattice2D<T, Descriptor>& lattice)
    {
        for (plint iX = domain.x0; iX <= domain.x1; ++iX) {
            for (plint iY = domain.y0; iY <= domain.y1; ++iY) {
                Cell<T, Descriptor>& cell = lattice.get(iX, iY);
                if (cell.getDynamics().isBoundary()) continue;

                T rho = cell.computeDensity();
                Array<T, 2> force(rho * gx, rho * gy);

                cell.setExternalField(
                    Descriptor<T>::ExternalField::forceBeginsAt,
                    Descriptor<T>::ExternalField::sizeOfForce, &force[0]);
            }
        }
    }

    virtual SetGravityForce<T, Descriptor>* clone() const {
        return new SetGravityForce<T, Descriptor>(*this);
    }

    virtual void getTypeOfModification(std::vector<modif::ModifT>& modified) const {
        modified[0] = modif::dynamicVariables;
    }

private:
    T gx, gy;
};

// =============================================================================
// Carreau Rheology Processor
// Computes local strain rate and applies variable-viscosity collision
// =============================================================================
template<typename T, template<typename U> class Descriptor>
class CarreauRheologyProcessor : public BoxProcessingFunctional2D_L<T, Descriptor>
{
public:
    CarreauRheologyProcessor(T baseOmega_) : baseOmega(baseOmega_) { }

    virtual void process(Box2D domain, BlockLattice2D<T, Descriptor>& lattice)
    {
        if (!gCarreau.enabled) return;

        for (plint iX = domain.x0; iX <= domain.x1; ++iX) {
            for (plint iY = domain.y0; iY <= domain.y1; ++iY) {
                Cell<T, Descriptor>& cell = lattice.get(iX, iY);
                if (cell.getDynamics().isBoundary()) continue;

                // Compute local density and velocity
                T rho = cell.computeDensity();
                Array<T, 2> u;
                cell.computeVelocity(u);

                // Compute strain rate tensor from non-equilibrium stress
                // Pi_neq_ab = sum_i (c_ia * c_ib) * f_i^neq
                T Pi_xx = T();
                T Pi_yy = T();
                T Pi_xy = T();

                // D2Q9 velocities
                static const int cx[9] = {0, 1, 0, -1, 0, 1, -1, -1, 1};
                static const int cy[9] = {0, 0, 1, 0, -1, 1, 1, -1, -1};
                static const T w[9] = {4.0/9.0,
                                       1.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/9.0,
                                       1.0/36.0, 1.0/36.0, 1.0/36.0, 1.0/36.0};

                for (plint i = 0; i < 9; ++i) {
                    T cix = cx[i];
                    T ciy = cy[i];
                    T cu = cix * u[0] + ciy * u[1];
                    T u2 = u[0] * u[0] + u[1] * u[1];

                    // Equilibrium distribution
                    T feq = w[i] * rho * (1.0 + 3.0 * cu + 4.5 * cu * cu - 1.5 * u2);

                    // Non-equilibrium part
                    T fneq = cell[i] - feq;

                    Pi_xx += cix * cix * fneq;
                    Pi_yy += ciy * ciy * fneq;
                    Pi_xy += cix * ciy * fneq;
                }

                // Strain rate tensor: S_ab = -(omega / (2 * rho * cs²)) * Pi_neq_ab
                // For D2Q9: cs² = 1/3
                T omegaRef = baseOmega;
                T Sxx = -1.5 * omegaRef * Pi_xx / rho;
                T Syy = -1.5 * omegaRef * Pi_yy / rho;
                T Sxy = -1.5 * omegaRef * Pi_xy / rho;

                // Strain rate magnitude: gamma_dot = sqrt(2 * S_ij * S_ij)
                T gammaDot = std::sqrt(2.0 * (Sxx*Sxx + Syy*Syy + 2.0*Sxy*Sxy));

                // Compute local omega from Carreau model
                T omegaLocal = gCarreau.computeOmega(gammaDot);

                // Apply collision correction if omega differs from base
                // The idea: cell has already been collided with baseOmega
                // We need to apply a correction: f_corrected = f + (1/omegaLocal - 1/baseOmega) * f_neq
                if (std::abs(omegaLocal - baseOmega) > 1e-10) {
                    T correction = (1.0/omegaLocal - 1.0/baseOmega) * baseOmega;

                    for (plint i = 0; i < 9; ++i) {
                        T cix = cx[i];
                        T ciy = cy[i];
                        T cu = cix * u[0] + ciy * u[1];
                        T u2 = u[0] * u[0] + u[1] * u[1];
                        T feq = w[i] * rho * (1.0 + 3.0 * cu + 4.5 * cu * cu - 1.5 * u2);
                        T fneq = cell[i] - feq;

                        cell[i] += correction * fneq;
                    }
                }
            }
        }
    }

    virtual CarreauRheologyProcessor<T, Descriptor>* clone() const {
        return new CarreauRheologyProcessor<T, Descriptor>(*this);
    }

    virtual void getTypeOfModification(std::vector<modif::ModifT>& modified) const {
        modified[0] = modif::staticVariables;
    }

private:
    T baseOmega;
};

// =============================================================================
// Main
// =============================================================================
int main(int argc, char* argv[])
{
    plbInit(&argc, &argv);

    // Default parameters
    string outputDir = "./output/";
    T G = -112.0;  // Calibrated for shear-thinning ink wetting
    T gravity = -5.0e-5;
    T dropletRadius = 30.0;  // 150 µm = 30 l.u.
    T tau = 1.0;
    int maxIter = 50000;
    int saveIter = 500;
    int warmupIter = 1000;
    T shiftX_mm = 0.0;  // Droplet center X shift from well center (mm)

    // Carreau parameters (default: shear-thinning ink)
    bool useCarreau = false;
    T eta0 = 1.5;       // Pa.s
    T etaInf = 0.167;   // Pa.s
    T lambda = 0.15;    // s (relaxation time)
    T n_carreau = 0.7;  // power-law index
    T rho_phys = 3000.0; // kg/m³

    // Parse command-line arguments
    for (int i = 1; i < argc; ++i) {
        string arg = argv[i];
        if (arg == "--output" && i + 1 < argc) {
            outputDir = argv[++i];
        } else if (arg == "--G" && i + 1 < argc) {
            G = atof(argv[++i]);
        } else if (arg == "--gravity" && i + 1 < argc) {
            gravity = atof(argv[++i]);
        } else if (arg == "--radius" && i + 1 < argc) {
            dropletRadius = atof(argv[++i]);
        } else if (arg == "--maxIter" && i + 1 < argc) {
            maxIter = atoi(argv[++i]);
        } else if (arg == "--saveIter" && i + 1 < argc) {
            saveIter = atoi(argv[++i]);
        } else if (arg == "--warmup" && i + 1 < argc) {
            warmupIter = atoi(argv[++i]);
        } else if (arg == "--tau" && i + 1 < argc) {
            tau = atof(argv[++i]);
        } else if (arg == "--carreau") {
            useCarreau = true;
        } else if (arg == "--eta0" && i + 1 < argc) {
            eta0 = atof(argv[++i]);
            useCarreau = true;
        } else if (arg == "--etaInf" && i + 1 < argc) {
            etaInf = atof(argv[++i]);
            useCarreau = true;
        } else if (arg == "--lambda" && i + 1 < argc) {
            lambda = atof(argv[++i]);
            useCarreau = true;
        } else if (arg == "--n" && i + 1 < argc) {
            n_carreau = atof(argv[++i]);
            useCarreau = true;
        } else if (arg == "--rho" && i + 1 < argc) {
            rho_phys = atof(argv[++i]);
        }
        // Contact angles (degrees)
        else if (arg == "--theta-wellBottom" && i + 1 < argc) {
            theta_wellBottom = atof(argv[++i]);
        } else if (arg == "--theta-leftWall" && i + 1 < argc) {
            theta_leftWall = atof(argv[++i]);
        } else if (arg == "--theta-rightWall" && i + 1 < argc) {
            theta_rightWall = atof(argv[++i]);
        } else if (arg == "--theta-leftPlatform" && i + 1 < argc) {
            theta_leftPlatform = atof(argv[++i]);
        } else if (arg == "--theta-rightPlatform" && i + 1 < argc) {
            theta_rightPlatform = atof(argv[++i]);
        } else if (arg == "--shiftX" && i + 1 < argc) {
            shiftX_mm = atof(argv[++i]);
        }
    }

    // Set up global Carreau parameters
    gCarreau.enabled = useCarreau;
    gCarreau.eta0 = eta0;
    gCarreau.etaInf = etaInf;
    gCarreau.lambda = lambda;
    gCarreau.n = n_carreau;
    gCarreau.rho_phys = rho_phys;
    gCarreau.tauMin = 0.55;
    gCarreau.tauMax = 2.0;

    global::directories().setOutputDir(outputDir);

    const T omega = 1.0 / tau;
    const T psi0 = 4.0;
    const T rho0 = 200.0;

    // Equilibrium densities for G=-120 (pre-computed from Shan-Chen EOS)
    // These are the stable coexistence densities after phase separation
    const T rho_heavy = 530.0;  // Liquid phase equilibrium density
    const T rho_light = 85.0;   // Gas phase equilibrium density

    // Droplet center in lattice units
    // Physical: (0.6 mm + shiftX, 0.3 mm) -> Lattice: (120 + shift_lu, wellDepth + 60)
    // Well center is at 0.6 mm, shiftX allows offsetting (negative = toward left platform)
    T dropletCenterX = (0.6 + shiftX_mm) / dx;  // Default: 120 l.u., with shift
    T dropletCenterY = wellDepth + 0.3 / dx;  // 26 + 60 = 86 l.u.

    pcout << "============================================" << endl;
    pcout << "Droplet in Cavity - Multi-Contact Angle" << endl;
    pcout << "============================================" << endl;
    pcout << "Output: " << outputDir << endl;
    pcout << "Domain: " << nx << " x " << ny << " l.u." << endl;
    pcout << "Physical: " << nx * dx << " x " << ny * dx << " mm" << endl;
    pcout << "Well depth: " << wellDepth << " l.u. (" << wellDepth * dx << " mm)" << endl;
    pcout << "Well width: " << (wellEndX - wellStartX) << " l.u. (" << (wellEndX - wellStartX) * dx << " mm)" << endl;
    pcout << "Droplet center: (" << dropletCenterX << ", " << dropletCenterY << ") l.u." << endl;
    pcout << "Droplet shift X: " << shiftX_mm << " mm (" << shiftX_mm / dx << " l.u.)" << endl;
    pcout << "Droplet radius: " << dropletRadius << " l.u. (" << dropletRadius * dx << " mm)" << endl;
    pcout << "Contact angles:" << endl;
    pcout << "  Well bottom: " << theta_wellBottom << " deg" << endl;
    pcout << "  Left wall: " << theta_leftWall << " deg" << endl;
    pcout << "  Right wall: " << theta_rightWall << " deg" << endl;
    pcout << "  Left platform: " << theta_leftPlatform << " deg" << endl;
    pcout << "  Right platform: " << theta_rightPlatform << " deg" << endl;
    pcout << "G: " << G << ", tau: " << tau << ", gravity: " << gravity << endl;
    if (useCarreau) {
        pcout << "Carreau rheology: ENABLED" << endl;
        pcout << "  eta0: " << eta0 << " Pa.s (zero-shear)" << endl;
        pcout << "  etaInf: " << etaInf << " Pa.s (infinite-shear)" << endl;
        pcout << "  lambda: " << lambda << " s" << endl;
        pcout << "  n: " << n_carreau << " (shear-thinning)" << endl;
        pcout << "  rho: " << rho_phys << " kg/m³" << endl;
        pcout << "  tau range: [" << gCarreau.tauMin << ", " << gCarreau.tauMax << "]" << endl;
    } else {
        pcout << "Carreau rheology: DISABLED (Newtonian)" << endl;
    }
    pcout << "============================================" << endl;

    // Create lattice
    MultiBlockLattice2D<T, DESCRIPTOR> lattice(
        nx, ny,
        new ExternalMomentBGKdynamics<T, DESCRIPTOR>(omega)
    );

    lattice.periodicity().toggle(0, false);
    lattice.periodicity().toggle(1, false);

    // Set up cavity geometry with neutral walls initially
    const T rho_neutral = 90.0;

    pcout << "Setting up cavity geometry..." << endl;

    // Iterate over all cells and set BounceBack for wall regions
    // IMPORTANT: Exclude top boundary (WALL_TOP) to use open outlet condition
    // This prevents artificial compression of the droplet during equilibration
    for (plint iX = 0; iX < nx; ++iX) {
        for (plint iY = 0; iY < ny; ++iY) {
            WallRegion region = getWallRegion(iX, iY);
            if (region != WALL_NONE && region != WALL_TOP) {
                defineDynamics(lattice, Box2D(iX, iX, iY, iY),
                               new BounceBack<T, DESCRIPTOR>(rho_neutral));
            }
        }
    }

    // Initialize droplet
    applyProcessingFunctional(
        new DropletInitializer<T, DESCRIPTOR>(
            dropletCenterX, dropletCenterY, dropletRadius,
            rho_heavy, rho_light),
        lattice.getBoundingBox(), lattice);

    // Add Shan-Chen processor
    integrateProcessingFunctional(
        new ShanChenSingleComponentProcessor2D<T, DESCRIPTOR>(
            G, new interparticlePotential::PsiShanChen94<T>(psi0, rho0)),
        lattice.getBoundingBox(), lattice, 0);

    // NOTE: Carreau rheology is added AFTER warmup to allow proper spherical equilibration
    // (high viscosity at rest would prevent droplet from relaxing to equilibrium shape)

    lattice.initialize();

    // Phase 1: Equilibration without gravity (Newtonian - no Carreau yet)
    pcout << "Phase 1: Equilibrating phases (no gravity, Newtonian)..." << endl;
    for (int iT = 0; iT < warmupIter; ++iT) {
        lattice.collideAndStream();
        if (iT % 500 == 0) {
            std::unique_ptr<MultiScalarField2D<T>> rho(computeDensity(lattice));
            pcout << "  Warmup " << iT << " - rho: [" << computeMin(*rho)
                  << ", " << computeMax(*rho) << "]" << endl;
        }
    }

    // Get equilibrium densities
    std::unique_ptr<MultiScalarField2D<T>> rhoEq(computeDensity(lattice));
    T rhoGas = computeMin(*rhoEq);
    T rhoLiq = computeMax(*rhoEq);
    pcout << "Equilibrium: gas=" << rhoGas << ", liquid=" << rhoLiq << endl;

    // Compute wall densities for each region
    T rhoWall_bottom = computeWallDensity(theta_wellBottom, rhoGas, rhoLiq);
    T rhoWall_leftVert = computeWallDensity(theta_leftWall, rhoGas, rhoLiq);
    T rhoWall_rightVert = computeWallDensity(theta_rightWall, rhoGas, rhoLiq);
    T rhoWall_leftPlatform = computeWallDensity(theta_leftPlatform, rhoGas, rhoLiq);
    T rhoWall_rightPlatform = computeWallDensity(theta_rightPlatform, rhoGas, rhoLiq);

    pcout << "Wall densities:" << endl;
    pcout << "  Bottom (30°): " << rhoWall_bottom << endl;
    pcout << "  Left wall (60°): " << rhoWall_leftVert << endl;
    pcout << "  Right wall (90°): " << rhoWall_rightVert << endl;
    pcout << "  Left platform (60°): " << rhoWall_leftPlatform << endl;
    pcout << "  Right platform (90°): " << rhoWall_rightPlatform << endl;

    // Save initial state
    {
        std::unique_ptr<MultiScalarField2D<T>> rho(computeDensity(lattice));
        maskInternalSolids(*rho, rhoGas);  // Hide internal solid regions
        VtkImageOutput2D<T> vtkOut("droplet_0", 1.0);
        vtkOut.writeData<float>(*rho, "density", 1.0);
        pcout << "Initial state saved" << endl;
    }

    // Phase 2: Add Carreau rheology (now that droplet is spherical)
    if (useCarreau) {
        integrateProcessingFunctional(
            new CarreauRheologyProcessor<T, DESCRIPTOR>(omega),
            lattice.getBoundingBox(), lattice, 1);
        pcout << "Carreau rheology processor integrated (after equilibration)." << endl;
    }

    // Phase 3: Add gravity
    pcout << "Phase 3: Adding gravity g=" << gravity << endl;
    integrateProcessingFunctional(
        new SetGravityForce<T, DESCRIPTOR>(0.0, gravity),
        lattice.getBoundingBox(), lattice, 2);

    // Main loop with PROGRESSIVE wall density application
    // Wall densities are applied locally only where liquid is present
    const T contactThreshold = (rhoGas + rhoLiq) / 2.0;
    const T liquidThreshold = rhoGas + 0.15 * (rhoLiq - rhoGas);  // ~15% liquid fraction (lower = more sensitive)

    // Track which wall cells have been activated (to avoid repeated updates)
    std::vector<std::vector<bool>> wallActivated(nx, std::vector<bool>(ny, false));
    bool contactDetected = false;
    int contactIter = 0;

    for (int iT = 1; iT <= maxIter; ++iT) {
        lattice.collideAndStream();

        // Progressive wall density application based on local liquid presence
        // Check every 10 iterations to reduce computational cost
        if (iT % 10 == 0) {
            std::unique_ptr<MultiScalarField2D<T>> rho(computeDensity(lattice));

            // Detect first contact with bottom
            if (!contactDetected) {
                for (plint iX = wellStartX + 1; iX < wellEndX; ++iX) {
                    if (rho->get(iX, 2) > contactThreshold) {
                        contactDetected = true;
                        contactIter = iT;
                        pcout << "  Contact detected at iter " << iT << endl;
                        // All walls (including vertical) will be activated progressively
                        // when liquid actually reaches them
                        break;
                    }
                }
            }

            // Apply wall densities progressively where liquid is present
            if (contactDetected) {
                int newActivations = 0;

                for (plint iX = 0; iX < nx; ++iX) {
                    for (plint iY = 0; iY < ny; ++iY) {
                        WallRegion region = getWallRegion(iX, iY);
                        if (region == WALL_NONE || wallActivated[iX][iY]) continue;

                        // Skip internal solid regions - they should NEVER get contact angle
                        // Only surface cells need wetting properties
                        if (region == WALL_LEFT_PLATFORM_SOLID || region == WALL_RIGHT_PLATFORM_SOLID) continue;

                        // Check if liquid is adjacent to this wall cell
                        bool liquidNearby = false;
                        for (int dx = -1; dx <= 1; ++dx) {
                            for (int dy = -1; dy <= 1; ++dy) {
                                if (dx == 0 && dy == 0) continue;
                                plint nx_ = iX + dx;
                                plint ny_ = iY + dy;
                                if (nx_ >= 0 && nx_ < nx && ny_ >= 0 && ny_ < ny) {
                                    if (getWallRegion(nx_, ny_) == WALL_NONE) {
                                        if (rho->get(nx_, ny_) > liquidThreshold) {
                                            liquidNearby = true;
                                            break;
                                        }
                                    }
                                }
                            }
                            if (liquidNearby) break;
                        }

                        if (liquidNearby) {
                            T rhoWall = rho_neutral;
                            switch (region) {
                                case WALL_BOTTOM:
                                    rhoWall = rhoWall_bottom;
                                    break;
                                case WALL_LEFT_VERTICAL:
                                    rhoWall = rhoWall_leftVert;
                                    break;
                                case WALL_RIGHT_VERTICAL:
                                    rhoWall = rhoWall_rightVert;
                                    break;
                                case WALL_LEFT_PLATFORM:
                                    rhoWall = rhoWall_leftPlatform;
                                    break;
                                case WALL_RIGHT_PLATFORM:
                                    rhoWall = rhoWall_rightPlatform;
                                    break;
                                default:
                                    rhoWall = rho_neutral;
                            }

                            defineDynamics(lattice, Box2D(iX, iX, iY, iY),
                                           new BounceBack<T, DESCRIPTOR>(rhoWall));
                            wallActivated[iX][iY] = true;
                            newActivations++;
                        }
                    }
                }

                if (newActivations > 0 && iT % saveIter == 0) {
                    pcout << "  Activated " << newActivations << " wall cells at iter " << iT << endl;
                }
            }
        }

        if (iT % saveIter == 0) {
            std::unique_ptr<MultiScalarField2D<T>> rho(computeDensity(lattice));
            pcout << "Iter " << iT << " - rho: [" << computeMin(*rho)
                  << ", " << computeMax(*rho) << "]" << endl;

            maskInternalSolids(*rho, rhoGas);  // Hide internal solid regions before saving
            string filename = "droplet_" + util::val2str(iT);
            VtkImageOutput2D<T> vtkOut(filename, 1.0);
            vtkOut.writeData<float>(*rho, "density", 1.0);
        }
    }

    // Save parameters
    {
        ofstream paramFile(outputDir + "/parameters.txt");
        paramFile << "# Cavity droplet simulation" << endl;
        paramFile << "G=" << G << endl;
        paramFile << "gravity=" << gravity << endl;
        paramFile << "radius=" << dropletRadius << endl;
        paramFile << "tau=" << tau << endl;
        paramFile << "theta_bottom=" << theta_wellBottom << endl;
        paramFile << "theta_leftWall=" << theta_leftWall << endl;
        paramFile << "theta_rightWall=" << theta_rightWall << endl;
        paramFile << "theta_leftPlatform=" << theta_leftPlatform << endl;
        paramFile << "theta_rightPlatform=" << theta_rightPlatform << endl;
        paramFile << "wellDepth_lu=" << wellDepth << endl;
        paramFile << "wellWidth_lu=" << (wellEndX - wellStartX) << endl;
        paramFile << "dx_mm=" << dx << endl;
        paramFile << "# Carreau rheology" << endl;
        paramFile << "carreau_enabled=" << (useCarreau ? "true" : "false") << endl;
        if (useCarreau) {
            paramFile << "eta0=" << eta0 << endl;
            paramFile << "etaInf=" << etaInf << endl;
            paramFile << "lambda=" << lambda << endl;
            paramFile << "n=" << n_carreau << endl;
            paramFile << "rho_phys=" << rho_phys << endl;
        }
        paramFile.close();
    }

    pcout << "Done!" << endl;
    return 0;
}
