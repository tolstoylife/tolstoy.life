"""
Glucose excretion calculation considering Tm limitation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_glucose_excretion(filtered_load: float, T_max: float = 375.0) -> float:
    """
    Calculate glucose excretion based on filtered load and transport maximum.

    Args:
        filtered_load: Glucose filtered load (mg/min)
        T_max: Maximum glucose reabsorption rate (mg/min, default 375)

    Returns:
        excretion: Glucose excreted in urine (mg/min)
    """
    if filtered_load <= T_max:
        return 0.0  # All glucose reabsorbed
    else:
        return filtered_load - T_max


# Create equation
glucose_excretion = create_equation(
    id="renal.tubular.glucose_excretion",
    name="Glucose Excretion",
    category=EquationCategory.RENAL,
    latex=r"Excretion = \begin{cases} 0 & \text{if } FL \leq T_{max} \\ FL - T_{max} & \text{if } FL > T_{max} \end{cases}",
    simplified="Excretion = max(0, FL - T_max)",
    description="Glucose excretion occurs only when filtered load exceeds transport maximum",
    compute_func=compute_glucose_excretion,
    parameters=[
        Parameter(
            name="filtered_load",
            description="Glucose filtered load",
            units="mg/min",
            symbol="FL",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="T_max",
            description="Maximum glucose reabsorption rate",
            units="mg/min",
            symbol="T_{max}",
            default_value=375.0,
            physiological_range=(300, 450)
        )
    ],
    depends_on=["renal.clearance.filtered_load", "renal.tubular.transport_tm"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equation
register_equation(glucose_excretion)
