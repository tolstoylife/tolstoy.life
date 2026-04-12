"""
Mass balance equation for excretion.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_excretion(GFR: float, P_x: float, R_x: float, S_x: float) -> float:
    """
    Calculate excretion using mass balance.

    Args:
        GFR: Glomerular filtration rate (mL/min)
        P_x: Plasma concentration (mg/dL or mmol/L)
        R_x: Amount reabsorbed (mg/min or mmol/min)
        S_x: Amount secreted (mg/min or mmol/min)

    Returns:
        Excretion: Amount excreted per unit time (mg/min or mmol/min)
    """
    filtration = GFR * P_x
    return filtration - R_x + S_x


# Create equation
excretion_mass_balance = create_equation(
    id="renal.tubular.excretion_mass_balance",
    name="Excretion Mass Balance",
    category=EquationCategory.RENAL,
    latex=r"Excretion = Filtration - Reabsorption + Secretion",
    simplified="Excretion = GFR × P_x - R_x + S_x",
    description="Mass balance relating filtration, reabsorption, secretion, and excretion",
    compute_func=compute_excretion,
    parameters=[
        Parameter(
            name="GFR",
            description="Glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(90, 140)
        ),
        Parameter(
            name="P_x",
            description="Plasma concentration of substance",
            units="mg/dL or mmol/L",
            symbol="P_x",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="R_x",
            description="Amount reabsorbed",
            units="mg/min or mmol/min",
            symbol="R_x",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="S_x",
            description="Amount secreted",
            units="mg/min or mmol/min",
            symbol="S_x",
            physiological_range=(0, 100)
        )
    ],
    depends_on=["renal.clearance.filtered_load"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equation
register_equation(excretion_mass_balance)
