"""
Psychophysics Equations (Weber-Fechner Law, Stevens Power Law)

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 26-28)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def weber_fraction(delta_I: float, I: float) -> float:
    """
    Calculate Weber fraction (just noticeable difference ratio).

    Formula: k = ΔI / I

    Weber's law states that the just noticeable difference (JND) is
    proportional to the stimulus intensity. The Weber fraction k is
    relatively constant for a given sensory modality.

    Parameters:
    -----------
    delta_I : float - Just noticeable difference in intensity
    I : float - Reference intensity (same units)

    Returns:
    --------
    k : float - Weber fraction (dimensionless)

    Typical values:
    - Brightness: k ≈ 0.08
    - Loudness: k ≈ 0.05
    - Weight: k ≈ 0.02
    - Taste (salt): k ≈ 0.20
    """
    return delta_I / I


def fechner_sensation(I: float, I_0: float, k: float) -> float:
    """
    Calculate perceived sensation using Fechner's law.

    Formula: S = k × ln(I/I₀)

    Fechner integrated Weber's law to derive that perceived
    sensation is logarithmic with stimulus intensity.

    Parameters:
    -----------
    I : float - Stimulus intensity
    I_0 : float - Threshold intensity (same units)
    k : float - Sensory constant (modality-dependent)

    Returns:
    --------
    S : float - Perceived sensation (arbitrary units)
    """
    return k * np.log(I / I_0)


def stevens_power_law(I: float, I_0: float, k: float, n: float) -> float:
    """
    Calculate perceived sensation using Stevens' power law.

    Formula: S = k × (I - I₀)ⁿ

    Stevens' power law is a more general formulation than Fechner's law.
    The exponent n varies by sensory modality:
    - Brightness: n ≈ 0.33 (compressive)
    - Loudness: n ≈ 0.6 (compressive)
    - Electric shock: n ≈ 3.5 (expansive)
    - Pain: n ≈ 1.0-2.0 (linear to expansive)

    Parameters:
    -----------
    I : float - Stimulus intensity
    I_0 : float - Threshold intensity
    k : float - Proportionality constant
    n : float - Stevens exponent

    Returns:
    --------
    S : float - Perceived sensation magnitude
    """
    if I <= I_0:
        return 0.0
    return k * (I - I_0)**n


def jnd_from_weber(I: float, k: float) -> float:
    """
    Calculate just noticeable difference from Weber fraction.

    Formula: ΔI = k × I

    Parameters:
    -----------
    I : float - Current stimulus intensity
    k : float - Weber fraction for this modality

    Returns:
    --------
    delta_I : float - Just noticeable difference (JND)
    """
    return k * I


def threshold_ratio(I: float, I_0: float) -> float:
    """
    Calculate stimulus intensity relative to threshold.

    Formula: ratio = I / I₀

    Expressed in decibels for auditory stimuli:
    dB SPL = 10 × log₁₀(I/I₀)

    Parameters:
    -----------
    I : float - Stimulus intensity
    I_0 : float - Threshold intensity

    Returns:
    --------
    ratio : float - Ratio above threshold (dimensionless)
    """
    return I / I_0


# Create and register Weber fraction equation
weber_fraction_eq = create_equation(
    id="foundations.sensory.weber_fraction",
    name="Weber's Fraction",
    category=EquationCategory.FOUNDATIONS,
    latex=r"k = \frac{\Delta I}{I}",
    simplified="k = ΔI / I",
    description="Just noticeable difference as fraction of stimulus intensity",
    compute_func=weber_fraction,
    parameters=[
        Parameter(
            name="delta_I",
            description="Just noticeable difference (JND)",
            units="variable",
            symbol=r"\Delta I",
            physiological_range=(0.0, 1e6)
        ),
        Parameter(
            name="I",
            description="Reference stimulus intensity",
            units="variable",
            symbol="I",
            physiological_range=(1e-12, 1e6)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.8",
        textbook_equation_number="A.26"
    )
)
register_equation(weber_fraction_eq)


# Create and register Fechner's law equation
fechner_law_eq = create_equation(
    id="foundations.sensory.fechner_law",
    name="Fechner's Law",
    category=EquationCategory.FOUNDATIONS,
    latex=r"S = k \ln\left(\frac{I}{I_0}\right)",
    simplified="S = k × ln(I/I₀)",
    description="Perceived sensation as logarithm of stimulus intensity",
    compute_func=fechner_sensation,
    parameters=[
        Parameter(
            name="I",
            description="Stimulus intensity",
            units="variable",
            symbol="I",
            physiological_range=(1e-12, 1e6)
        ),
        Parameter(
            name="I_0",
            description="Threshold intensity",
            units="variable",
            symbol="I_0",
            physiological_range=(1e-12, 1e6)
        ),
        Parameter(
            name="k",
            description="Sensory constant",
            units="variable",
            symbol="k",
            physiological_range=(0.01, 100.0)
        ),
    ],
    depends_on=["foundations.sensory.weber_fraction"],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.8",
        textbook_equation_number="A.27"
    )
)
register_equation(fechner_law_eq)


# Create and register Stevens' power law equation
stevens_law_eq = create_equation(
    id="foundations.sensory.stevens_power_law",
    name="Stevens' Power Law",
    category=EquationCategory.FOUNDATIONS,
    latex=r"S = k(I - I_0)^n",
    simplified="S = k × (I - I₀)ⁿ",
    description="Perceived sensation as power function of stimulus intensity",
    compute_func=stevens_power_law,
    parameters=[
        Parameter(
            name="I",
            description="Stimulus intensity",
            units="variable",
            symbol="I",
            physiological_range=(1e-12, 1e6)
        ),
        Parameter(
            name="I_0",
            description="Threshold intensity",
            units="variable",
            symbol="I_0",
            physiological_range=(1e-12, 1e6)
        ),
        Parameter(
            name="k",
            description="Proportionality constant",
            units="variable",
            symbol="k",
            physiological_range=(0.001, 1000.0)
        ),
        Parameter(
            name="n",
            description="Stevens exponent (modality-dependent)",
            units="dimensionless",
            symbol="n",
            physiological_range=(0.1, 4.0)  # Compressive to expansive
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.8",
        textbook_equation_number="A.28"
    )
)
register_equation(stevens_law_eq)
