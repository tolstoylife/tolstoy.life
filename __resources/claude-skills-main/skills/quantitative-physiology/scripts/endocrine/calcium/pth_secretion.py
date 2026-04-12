"""
PTH secretion as inverse function of ionized calcium.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_pth_secretion(Ca_ionized: float, PTH_max: float = 65.0,
                          K: float = 1.1, n: float = 3.5) -> float:
    """
    Calculate PTH secretion rate as inverse function of ionized calcium.

    Parameters
    ----------
    Ca_ionized : float
        Ionized (free) calcium concentration (mM)
    PTH_max : float
        Maximum PTH concentration (pg/mL)
    K : float
        Calcium setpoint (mM)
    n : float
        Hill coefficient (steepness)

    Returns
    -------
    float
        PTH concentration (pg/mL)

    Notes
    -----
    Calcium-sensing receptor (CaSR) mediates inverse regulation:
    ↑ Ca²⁺ → ↑ CaSR activation → ↓ PTH secretion

    Normal ranges:
    - Ionized Ca²⁺: 1.0-1.3 mM
    - PTH (intact): 10-65 pg/mL

    Steep inverse response (n ≈ 3-4) provides tight calcium regulation.
    """
    return PTH_max * (K ** n) / (K ** n + Ca_ionized ** n)


# Create equation
pth_secretion_equation = create_equation(
    id="endocrine.calcium.pth_secretion",
    name="PTH Secretion (Calcium Feedback)",
    category=EquationCategory.ENDOCRINE,
    latex=r"PTH = PTH_{max} \times \frac{K^n}{K^n + [Ca^{2+}]^n}",
    simplified="PTH = PTH_max × K^n / (K^n + [Ca²⁺]^n)",
    description="PTH secretion from parathyroid glands as steep inverse function of ionized calcium. "
                "Calcium-sensing receptor (CaSR) mediates negative feedback (n ≈ 3-4).",
    compute_func=compute_pth_secretion,
    parameters=[
        Parameter(
            name="Ca_ionized",
            description="Ionized calcium concentration",
            units="mM",
            symbol="[Ca^{2+}]",
            physiological_range=(0.8, 1.5)
        ),
        Parameter(
            name="PTH_max",
            description="Maximum PTH concentration",
            units="pg/mL",
            symbol="PTH_{max}",
            default_value=65.0,
            physiological_range=(50.0, 100.0)
        ),
        Parameter(
            name="K",
            description="Calcium setpoint",
            units="mM",
            symbol="K",
            default_value=1.1,
            physiological_range=(1.0, 1.3)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=3.5,
            physiological_range=(3.0, 4.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.7"
    )
)

# Register globally
register_equation(pth_secretion_equation)
