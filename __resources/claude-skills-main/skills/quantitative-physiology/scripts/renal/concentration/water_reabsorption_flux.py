"""
Water reabsorption flux in collecting duct.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_water_flux(L_p: float, A: float, pi_int: float, pi_lumen: float) -> float:
    """
    Calculate water reabsorption flux driven by osmotic gradient.

    Args:
        L_p: Hydraulic conductivity (water permeability)
        A: Surface area
        pi_int: Interstitial osmotic pressure
        pi_lumen: Luminal osmotic pressure

    Returns:
        J_water: Water flux (volume per unit time)
    """
    return L_p * A * (pi_int - pi_lumen)


# Create equation
water_reabsorption_flux = create_equation(
    id="renal.concentration.water_reabsorption_flux",
    name="Water Reabsorption Flux",
    category=EquationCategory.RENAL,
    latex=r"J_{water} = L_p \times A \times (\pi_{int} - \pi_{lumen})",
    simplified="J_water = L_p × A × (π_int - π_lumen)",
    description="Osmotic water movement from tubular lumen to interstitium in collecting duct",
    compute_func=compute_water_flux,
    parameters=[
        Parameter(
            name="L_p",
            description="Hydraulic conductivity (water permeability)",
            units="cm/s/mOsm",
            symbol="L_p",
            physiological_range=(1e-7, 1e-4)
        ),
        Parameter(
            name="A",
            description="Surface area",
            units="cm²",
            symbol="A",
            physiological_range=(0.1, 10)
        ),
        Parameter(
            name="pi_int",
            description="Interstitial osmotic pressure",
            units="mOsm/kg",
            symbol=r"\pi_{int}",
            physiological_range=(300, 1200)
        ),
        Parameter(
            name="pi_lumen",
            description="Luminal osmotic pressure",
            units="mOsm/kg",
            symbol=r"\pi_{lumen}",
            physiological_range=(50, 1200)
        )
    ],
    depends_on=["renal.concentration.adh_water_permeability"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.6"
    )
)

# Register equation
register_equation(water_reabsorption_flux)
