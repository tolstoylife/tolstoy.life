"""
Sedimentation and Centrifugation Equations

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 40-43)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def sedimentation_rate(m: float, rho_p: float, rho_f: float, f: float,
                       omega: float, r: float) -> float:
    """
    Calculate sedimentation velocity in a centrifuge.

    Formula: v = m(1 - ρ_f/ρ_p) × ω²r / f

    Describes the rate at which particles sediment in a centrifugal field,
    accounting for buoyancy and frictional resistance.

    Parameters:
    -----------
    m : float - Particle mass (kg)
    rho_p : float - Particle density (kg/m³)
    rho_f : float - Fluid density (kg/m³)
    f : float - Frictional coefficient (kg/s)
    omega : float - Angular velocity (rad/s)
    r : float - Radial distance from axis (m)

    Returns:
    --------
    v : float - Sedimentation velocity (m/s)
    """
    buoyancy_factor = 1 - rho_f / rho_p
    centrifugal_acceleration = omega**2 * r
    return m * buoyancy_factor * centrifugal_acceleration / f


def svedberg_coefficient(v: float, omega: float, r: float) -> float:
    """
    Calculate Svedberg coefficient from sedimentation data.

    Formula: s = v / (ω²r)

    The Svedberg unit (S) is 10^-13 seconds. Used to characterize
    macromolecules like ribosomes (70S, 80S) and proteins.

    Parameters:
    -----------
    v : float - Sedimentation velocity (m/s)
    omega : float - Angular velocity (rad/s)
    r : float - Radial distance (m)

    Returns:
    --------
    s : float - Svedberg coefficient (s)
    """
    return v / (omega**2 * r)


def relative_centrifugal_force(omega: float, r: float,
                                g: float = 9.81) -> float:
    """
    Calculate relative centrifugal force (RCF) in units of g.

    Formula: RCF = ω²r / g

    Expresses centrifugal acceleration as multiples of Earth's gravity.
    Common centrifuge specifications use RCF (×g).

    Parameters:
    -----------
    omega : float - Angular velocity (rad/s)
    r : float - Radial distance (m)
    g : float - Gravitational acceleration (m/s²), default 9.81

    Returns:
    --------
    RCF : float - Relative centrifugal force (dimensionless, ×g)
    """
    return (omega**2 * r) / g


def rcf_from_rpm(rpm: float, r: float, g: float = 9.81) -> float:
    """
    Calculate RCF from RPM (common laboratory unit).

    Formula: RCF = (2π × RPM/60)² × r / g = 1.118 × 10⁻⁵ × RPM² × r

    Parameters:
    -----------
    rpm : float - Rotations per minute
    r : float - Radial distance (m)
    g : float - Gravitational acceleration (m/s²), default 9.81

    Returns:
    --------
    RCF : float - Relative centrifugal force (×g)
    """
    omega = 2 * np.pi * rpm / 60
    return (omega**2 * r) / g


# Create and register Svedberg equation
svedberg_eq = create_equation(
    id="foundations.biophysics.svedberg",
    name="Svedberg Coefficient",
    category=EquationCategory.FOUNDATIONS,
    latex=r"s = \frac{v}{\omega^2 r}",
    simplified="s = v / (ω²r)",
    description="Sedimentation coefficient characterizing particle size/shape",
    compute_func=svedberg_coefficient,
    parameters=[
        Parameter(
            name="v",
            description="Sedimentation velocity",
            units="m/s",
            symbol="v",
            physiological_range=(1e-12, 1e-6)  # Very slow settling
        ),
        Parameter(
            name="omega",
            description="Angular velocity",
            units="rad/s",
            symbol=r"\omega",
            physiological_range=(100.0, 100000.0)  # Lab centrifuges
        ),
        Parameter(
            name="r",
            description="Radial distance from rotation axis",
            units="m",
            symbol="r",
            physiological_range=(0.01, 0.2)  # Typical rotor dimensions
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.3",
        textbook_equation_number="A.42"
    )
)
register_equation(svedberg_eq)


# Create and register centrifugal force equation
centrifugal_force_eq = create_equation(
    id="foundations.biophysics.relative_centrifugal_force",
    name="Relative Centrifugal Force (RCF)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"RCF = \frac{\omega^2 r}{g}",
    simplified="RCF = ω²r / g",
    description="Centrifugal acceleration expressed as multiples of gravity",
    compute_func=relative_centrifugal_force,
    parameters=[
        Parameter(
            name="omega",
            description="Angular velocity",
            units="rad/s",
            symbol=r"\omega",
            physiological_range=(100.0, 100000.0)
        ),
        Parameter(
            name="r",
            description="Radial distance",
            units="m",
            symbol="r",
            physiological_range=(0.01, 0.2)
        ),
        Parameter(
            name="g",
            description="Gravitational acceleration",
            units="m/s²",
            symbol="g",
            default_value=9.81,
            physiological_range=(9.78, 9.83)  # Varies slightly with location
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.3",
        textbook_equation_number="A.40"
    )
)
register_equation(centrifugal_force_eq)
