"""Total Respiratory System Compliance equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_total_compliance(C_L: float, C_CW: float) -> float:
    """
    Calculate total respiratory system compliance (series combination).

    1/C_RS = 1/C_L + 1/C_CW

    Parameters
    ----------
    C_L : float
        Lung compliance (L/cmH2O)
    C_CW : float
        Chest wall compliance (L/cmH2O)

    Returns
    -------
    float
        Total respiratory system compliance (L/cmH2O)
    """
    return 1.0 / (1.0/C_L + 1.0/C_CW)


# Create equation
total_compliance = create_equation(
    id="respiratory.mechanics.total_compliance",
    name="Total Respiratory System Compliance",
    category=EquationCategory.RESPIRATORY,
    latex=r"\frac{1}{C_{RS}} = \frac{1}{C_L} + \frac{1}{C_{CW}}",
    simplified="1/C_RS = 1/C_L + 1/C_CW",
    description="Combined compliance of lung and chest wall in series",
    compute_func=compute_total_compliance,
    parameters=[
        Parameter(
            name="C_L",
            description="Lung compliance",
            units="L/cmH2O",
            symbol="C_L",
            default_value=0.2,
            physiological_range=(0.1, 0.3)
        ),
        Parameter(
            name="C_CW",
            description="Chest wall compliance",
            units="L/cmH2O",
            symbol="C_{CW}",
            default_value=0.2,
            physiological_range=(0.1, 0.3)
        )
    ],
    depends_on=["respiratory.mechanics.compliance"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(total_compliance)
