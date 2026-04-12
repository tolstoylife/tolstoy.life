"""
Carrier-Mediated Transport - Facilitated diffusion via carriers (Michaelis-Menten)

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_carrier_transport(S: float, J_max: float, K_m: float) -> float:
    """
    Calculate carrier-mediated transport rate (Michaelis-Menten kinetics).

    Formula: J = J_max × [S] / (K_m + [S])

    Parameters:
    -----------
    S : float
        Substrate concentration (mM or mol/m³)
    J_max : float
        Maximum transport rate (mol/(m²·s) or similar)
    K_m : float
        Half-saturation constant (mM or mol/m³)

    Returns:
    --------
    J : float
        Transport rate (same units as J_max)

    Characteristics:
        - Saturable (approaches J_max at high [S])
        - Specific (substrate selectivity)
        - Competitive inhibition possible
        - Temperature dependent (Q₁₀ > 1)
    """
    return J_max * S / (K_m + S)


# Create and register atomic equation
carrier_transport = create_equation(
    id="membrane.transport.carrier_transport",
    name="Carrier-Mediated Transport (Michaelis-Menten)",
    category=EquationCategory.MEMBRANE,
    latex=r"J = \frac{J_{max} \cdot [S]}{K_m + [S]}",
    simplified="J = (J_max * S) / (K_m + S)",
    description="Facilitated diffusion via carrier proteins showing saturation kinetics, following Michaelis-Menten form.",
    compute_func=compute_carrier_transport,
    parameters=[
        Parameter(
            name="S",
            description="Substrate concentration",
            units="mol/m³",
            symbol="[S]",
            default_value=None,
            physiological_range=(0.0, 1000.0)  # mM range
        ),
        Parameter(
            name="J_max",
            description="Maximum transport rate",
            units="mol/(m²·s)",
            symbol="J_{max}",
            default_value=None
        ),
        Parameter(
            name="K_m",
            description="Half-saturation constant (Michaelis constant)",
            units="mol/m³",
            symbol="K_m",
            default_value=None
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.2")
)

register_equation(carrier_transport)
