"""
Beer-Lambert Law for Light Absorption

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 35-36)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def beer_lambert_absorbance(epsilon: float, c: float, l: float) -> float:
    """
    Calculate optical absorbance using Beer-Lambert law.

    Formula: A = ε × c × l

    Beer-Lambert law relates absorbance to concentration. Fundamental for
    spectrophotometry, pulse oximetry, and colorimetric assays in
    clinical biochemistry.

    Parameters:
    -----------
    epsilon : float - Molar extinction coefficient (L/(mol·cm))
    c : float - Concentration (mol/L = M)
    l : float - Path length (cm)

    Returns:
    --------
    A : float - Absorbance (dimensionless, optical density units)
    """
    return epsilon * c * l


def absorbance_definition(I_0: float, I: float) -> float:
    """
    Calculate absorbance from incident and transmitted light intensities.

    Formula: A = log₁₀(I₀/I)

    Defines absorbance as the negative logarithm of transmittance.

    Parameters:
    -----------
    I_0 : float - Incident light intensity (arbitrary units)
    I : float - Transmitted light intensity (same units as I_0)

    Returns:
    --------
    A : float - Absorbance (dimensionless)
    """
    return np.log10(I_0 / I)


def transmittance(I_0: float, I: float) -> float:
    """
    Calculate transmittance as fraction of light transmitted.

    Formula: T = I / I₀

    Parameters:
    -----------
    I_0 : float - Incident light intensity (arbitrary units)
    I : float - Transmitted light intensity (same units)

    Returns:
    --------
    T : float - Transmittance (dimensionless, 0-1)
    """
    return I / I_0


def concentration_from_absorbance(A: float, epsilon: float, l: float) -> float:
    """
    Calculate concentration from absorbance (Beer-Lambert rearranged).

    Formula: c = A / (ε × l)

    Parameters:
    -----------
    A : float - Absorbance (dimensionless)
    epsilon : float - Molar extinction coefficient (L/(mol·cm))
    l : float - Path length (cm)

    Returns:
    --------
    c : float - Concentration (mol/L)
    """
    return A / (epsilon * l)


# Create and register Beer-Lambert equation
beer_lambert_eq = create_equation(
    id="foundations.kinetics.beer_lambert",
    name="Beer-Lambert Law",
    category=EquationCategory.FOUNDATIONS,
    latex=r"A = \varepsilon c l",
    simplified="A = ε × c × l",
    description="Relationship between absorbance, concentration, and path length",
    compute_func=beer_lambert_absorbance,
    parameters=[
        Parameter(
            name="epsilon",
            description="Molar extinction coefficient",
            units="L/(mol·cm)",
            symbol=r"\varepsilon",
            physiological_range=(100.0, 1e6)  # Varies widely by compound
        ),
        Parameter(
            name="c",
            description="Molar concentration",
            units="mol/L",
            symbol="c",
            physiological_range=(1e-9, 1.0)  # nM to M range
        ),
        Parameter(
            name="l",
            description="Path length",
            units="cm",
            symbol="l",
            default_value=1.0,  # Standard cuvette
            physiological_range=(0.01, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.6",
        textbook_equation_number="A.36"
    )
)
register_equation(beer_lambert_eq)


# Create and register absorbance definition equation
absorbance_definition_eq = create_equation(
    id="foundations.kinetics.absorbance_definition",
    name="Absorbance Definition",
    category=EquationCategory.FOUNDATIONS,
    latex=r"A = \log_{10}\left(\frac{I_0}{I}\right)",
    simplified="A = log₁₀(I₀/I)",
    description="Optical absorbance from transmitted light ratio",
    compute_func=absorbance_definition,
    parameters=[
        Parameter(
            name="I_0",
            description="Incident light intensity",
            units="arbitrary",
            symbol="I_0",
            physiological_range=(0.001, 1e6)
        ),
        Parameter(
            name="I",
            description="Transmitted light intensity",
            units="arbitrary",
            symbol="I",
            physiological_range=(0.001, 1e6)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.6",
        textbook_equation_number="A.35"
    )
)
register_equation(absorbance_definition_eq)
