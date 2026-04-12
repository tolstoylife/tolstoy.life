"""
Photoreceptor Response - Intensity-response relationship for rods

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_photoreceptor_response(I: float, sigma: float, n: float = 0.85) -> float:
    """
    Calculate photoreceptor (rod) response using Hill equation.

    Formula: R/R_max = I^n / (I^n + σ^n)

    Parameters:
    -----------
    I : float
        Light intensity (photons/μm²/s or relative units)
    sigma : float
        Half-saturation intensity
    n : float
        Hill coefficient, default 0.85 (typically 0.7-1.0)

    Returns:
    --------
    R_normalized : float
        Response normalized to maximum (0-1)

    Notes:
    ------
    Describes saturation of photoreceptor response at high intensities.
    For rods: σ ≈ 10-100 photons/μm²/s
    For cones: higher σ (less sensitive, broader dynamic range)
    n < 1 indicates slight negative cooperativity
    """
    return I**n / (I**n + sigma**n)


# Create and register atomic equation
photoreceptor_response = create_equation(
    id="nervous.sensory.photoreceptor_response",
    name="Photoreceptor Response",
    category=EquationCategory.NERVOUS,
    latex=r"\frac{R}{R_{max}} = \frac{I^n}{I^n + \sigma^n}",
    simplified="R/R_max = I^n / (I^n + σ^n)",
    description="Hill equation describing photoreceptor (rod) response saturation. Half-maximal response at I=σ. Used to model adaptation and dynamic range of photoreceptors.",
    compute_func=compute_photoreceptor_response,
    parameters=[
        Parameter(
            name="I",
            description="Light intensity",
            units="photons/μm²/s",
            symbol="I",
            default_value=None,
            physiological_range=(0.001, 10000.0)
        ),
        Parameter(
            name="sigma",
            description="Half-saturation intensity",
            units="photons/μm²/s",
            symbol=r"\sigma",
            default_value=None,
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=0.85,
            physiological_range=(0.5, 1.5)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(photoreceptor_response)
