"""Shunt Equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_shunt_equation(C_cO2: float, C_aO2: float, C_vO2: float) -> float:
    """
    Calculate shunt fraction (V̇A/Q̇ = 0).

    Q̇_S/Q̇_T = (C_cO2 - C_aO2) / (C_cO2 - C_vO2)

    Parameters
    ----------
    C_cO2 : float
        End-capillary O2 content (mL O2/dL)
    C_aO2 : float
        Arterial O2 content (mL O2/dL)
    C_vO2 : float
        Mixed venous O2 content (mL O2/dL)

    Returns
    -------
    float
        Shunt fraction (dimensionless, 0-1)
    """
    return (C_cO2 - C_aO2) / (C_cO2 - C_vO2)


# Create equation
shunt_equation = create_equation(
    id="respiratory.vq_matching.shunt_equation",
    name="Shunt Equation",
    category=EquationCategory.RESPIRATORY,
    latex=r"\frac{\dot{Q}_S}{\dot{Q}_T} = \frac{C_{cO2} - C_{aO2}}{C_{cO2} - C_{vO2}}",
    simplified="Q̇_S/Q̇_T = (C_cO2 - C_aO2) / (C_cO2 - C_vO2)",
    description="Fraction of cardiac output that bypasses gas exchange (V̇A/Q̇ = 0)",
    compute_func=compute_shunt_equation,
    parameters=[
        Parameter(
            name="C_cO2",
            description="End-capillary O2 content",
            units="mL O2/dL",
            symbol="C_{cO2}",
            default_value=20.0,
            physiological_range=(15.0, 23.0)
        ),
        Parameter(
            name="C_aO2",
            description="Arterial O2 content",
            units="mL O2/dL",
            symbol="C_{aO2}",
            default_value=19.5,
            physiological_range=(10.0, 22.0)
        ),
        Parameter(
            name="C_vO2",
            description="Mixed venous O2 content",
            units="mL O2/dL",
            symbol="C_{vO2}",
            default_value=15.0,
            physiological_range=(8.0, 18.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.4"
    )
)

# Register in global index
register_equation(shunt_equation)
