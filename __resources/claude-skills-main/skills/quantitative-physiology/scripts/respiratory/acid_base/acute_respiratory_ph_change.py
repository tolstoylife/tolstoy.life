"""Acute Respiratory pH Change equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_acute_respiratory_ph_change(delta_PCO2: float) -> float:
    """
    Calculate pH change in acute respiratory disorder.

    ΔpH = -0.008 × ΔP_CO2

    Parameters
    ----------
    delta_PCO2 : float
        Change in PCO2 from normal (mmHg)

    Returns
    -------
    float
        Change in pH
    """
    return -0.008 * delta_PCO2


# Create equation
acute_respiratory_ph_change = create_equation(
    id="respiratory.acid_base.acute_respiratory_ph_change",
    name="Acute Respiratory pH Change",
    category=EquationCategory.RESPIRATORY,
    latex=r"\Delta pH = -0.008 \times \Delta P_{CO2}",
    simplified="ΔpH = -0.008 × ΔP_CO2",
    description="Expected pH change per mmHg PCO2 change in acute respiratory disorders",
    compute_func=compute_acute_respiratory_ph_change,
    parameters=[
        Parameter(
            name="delta_PCO2",
            description="Change in PCO2 from normal",
            units="mmHg",
            symbol=r"\Delta P_{CO2}",
            physiological_range=(-40.0, 40.0)
        )
    ],
    depends_on=["respiratory.acid_base.henderson_hasselbalch"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(acute_respiratory_ph_change)
