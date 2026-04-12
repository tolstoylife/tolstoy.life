"""
Transport maximum (Tm) - Saturable transport kinetics.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_transport_tm(T_max: float, S: float, K_m: float) -> float:
    """
    Calculate saturable transport rate using Michaelis-Menten kinetics.

    Args:
        T_max: Maximum transport rate
        S: Substrate concentration
        K_m: Michaelis constant (concentration at half-maximal transport)

    Returns:
        T: Transport rate
    """
    return T_max * S / (K_m + S)


# Create equation
transport_tm = create_equation(
    id="renal.tubular.transport_tm",
    name="Transport Maximum (Michaelis-Menten)",
    category=EquationCategory.RENAL,
    latex=r"T = \frac{T_{max} \times [S]}{K_m + [S]}",
    simplified="T = T_max × [S] / (K_m + [S])",
    description="Saturable carrier-mediated transport following Michaelis-Menten kinetics",
    compute_func=compute_transport_tm,
    parameters=[
        Parameter(
            name="T_max",
            description="Maximum transport rate",
            units="mg/min or mmol/min",
            symbol="T_{max}",
            physiological_range=(100, 500)
        ),
        Parameter(
            name="S",
            description="Substrate concentration",
            units="mg/dL or mmol/L",
            symbol="[S]",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="K_m",
            description="Michaelis constant",
            units="mg/dL or mmol/L",
            symbol="K_m",
            physiological_range=(1, 100)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equation
register_equation(transport_tm)
