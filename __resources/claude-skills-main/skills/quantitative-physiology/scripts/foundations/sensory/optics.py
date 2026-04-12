"""
Optical Physics Equations (Snell's Law, Thin Lens)

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 31-34)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def snell_law(n1: float, theta1: float, n2: float) -> float:
    """
    Calculate refracted angle using Snell's law.

    Formula: n₁ sin(θ₁) = n₂ sin(θ₂)
    Rearranged: θ₂ = arcsin(n₁ sin(θ₁) / n₂)

    Describes light refraction at interface between media.
    Critical for understanding vision, cornea/lens optics.

    Parameters:
    -----------
    n1 : float - Refractive index of first medium (dimensionless)
    theta1 : float - Angle of incidence (radians)
    n2 : float - Refractive index of second medium (dimensionless)

    Returns:
    --------
    theta2 : float - Angle of refraction (radians)
    """
    sin_theta2 = (n1 * np.sin(theta1)) / n2
    # Check for total internal reflection
    if abs(sin_theta2) > 1.0:
        return np.nan  # Total internal reflection
    return np.arcsin(sin_theta2)


def critical_angle(n1: float, n2: float) -> float:
    """
    Calculate critical angle for total internal reflection.

    Formula: θ_c = arcsin(n₂/n₁)

    Only valid when n₁ > n₂ (going from denser to less dense medium).

    Parameters:
    -----------
    n1 : float - Refractive index of first (denser) medium
    n2 : float - Refractive index of second (less dense) medium

    Returns:
    --------
    theta_c : float - Critical angle (radians)
    """
    if n1 <= n2:
        return np.nan  # No total internal reflection possible
    return np.arcsin(n2 / n1)


def thin_lens_equation(f: float, d_o: float) -> float:
    """
    Calculate image distance using thin lens equation.

    Formula: 1/f = 1/d_o + 1/d_i
    Rearranged: d_i = (f × d_o) / (d_o - f)

    Fundamental for understanding eye optics, corrective lenses.

    Parameters:
    -----------
    f : float - Focal length (m), positive for converging lens
    d_o : float - Object distance (m), positive in front of lens

    Returns:
    --------
    d_i : float - Image distance (m), positive behind lens (real image)
    """
    if d_o == f:
        return np.inf  # Object at focal point
    return (f * d_o) / (d_o - f)


def lens_power(f: float) -> float:
    """
    Calculate lens power in diopters.

    Formula: P = 1/f (where f is in meters)

    Diopters are the standard clinical unit for prescribing
    corrective lenses.

    Parameters:
    -----------
    f : float - Focal length (m)

    Returns:
    --------
    P : float - Lens power (diopters, D = 1/m)
    """
    return 1.0 / f


def magnification(d_i: float, d_o: float) -> float:
    """
    Calculate linear magnification of lens.

    Formula: M = -d_i / d_o

    Negative M indicates inverted image (as in eye).

    Parameters:
    -----------
    d_i : float - Image distance (m)
    d_o : float - Object distance (m)

    Returns:
    --------
    M : float - Magnification (dimensionless)
    """
    return -d_i / d_o


def accommodation_power(d_near: float, d_far: float = np.inf) -> float:
    """
    Calculate accommodation amplitude (range of focus).

    Formula: A = 1/d_near - 1/d_far

    Measures the eye's ability to change focus from far to near.
    Decreases with age (presbyopia).

    Parameters:
    -----------
    d_near : float - Near point distance (m)
    d_far : float - Far point distance (m), default infinity

    Returns:
    --------
    A : float - Accommodation amplitude (diopters)
    """
    return (1.0 / d_near) - (1.0 / d_far if d_far != np.inf else 0)


# Create and register Snell's law equation
snell_law_eq = create_equation(
    id="foundations.sensory.snell_law",
    name="Snell's Law of Refraction",
    category=EquationCategory.FOUNDATIONS,
    latex=r"n_1 \sin\theta_1 = n_2 \sin\theta_2",
    simplified="n₁ sin(θ₁) = n₂ sin(θ₂)",
    description="Light refraction at interface between media with different refractive indices",
    compute_func=snell_law,
    parameters=[
        Parameter(
            name="n1",
            description="Refractive index of first medium",
            units="dimensionless",
            symbol="n_1",
            physiological_range=(1.0, 2.0)  # Air to diamond range
        ),
        Parameter(
            name="theta1",
            description="Angle of incidence",
            units="rad",
            symbol=r"\theta_1",
            physiological_range=(0.0, np.pi/2)
        ),
        Parameter(
            name="n2",
            description="Refractive index of second medium",
            units="dimensionless",
            symbol="n_2",
            physiological_range=(1.0, 2.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.7",
        textbook_equation_number="A.31"
    )
)
register_equation(snell_law_eq)


# Create and register thin lens equation
thin_lens_eq = create_equation(
    id="foundations.sensory.thin_lens",
    name="Thin Lens Equation",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\frac{1}{f} = \frac{1}{d_o} + \frac{1}{d_i}",
    simplified="1/f = 1/dₒ + 1/dᵢ",
    description="Relationship between focal length, object distance, and image distance",
    compute_func=thin_lens_equation,
    parameters=[
        Parameter(
            name="f",
            description="Focal length (positive for converging)",
            units="m",
            symbol="f",
            physiological_range=(0.001, 1.0)  # mm to m range
        ),
        Parameter(
            name="d_o",
            description="Object distance from lens",
            units="m",
            symbol="d_o",
            physiological_range=(0.01, 100.0)  # Near to far objects
        ),
    ],
    depends_on=["foundations.sensory.snell_law"],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.7",
        textbook_equation_number="A.32"
    )
)
register_equation(thin_lens_eq)


# Create and register lens power equation
lens_power_eq = create_equation(
    id="foundations.sensory.lens_power",
    name="Lens Power (Diopters)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"P = \frac{1}{f}",
    simplified="P = 1/f",
    description="Lens refractive power in diopters (clinical unit for eyeglasses)",
    compute_func=lens_power,
    parameters=[
        Parameter(
            name="f",
            description="Focal length",
            units="m",
            symbol="f",
            physiological_range=(0.001, 10.0)
        ),
    ],
    depends_on=["foundations.sensory.thin_lens"],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.7",
        textbook_equation_number="A.33"
    )
)
register_equation(lens_power_eq)
