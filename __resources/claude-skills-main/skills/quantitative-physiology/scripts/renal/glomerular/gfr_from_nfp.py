"""
Glomerular Filtration Rate (GFR) from ultrafiltration coefficient and NFP.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_gfr(K_f: float, NFP: float) -> float:
    """
    Calculate GFR from ultrafiltration coefficient and net filtration pressure.

    Args:
        K_f: Ultrafiltration coefficient (mL/min/mmHg)
        NFP: Net filtration pressure (mmHg)

    Returns:
        GFR: Glomerular filtration rate (mL/min)
    """
    return K_f * NFP


# Create equation
gfr_from_nfp = create_equation(
    id="renal.glomerular.gfr_from_nfp",
    name="GFR from Ultrafiltration Coefficient",
    category=EquationCategory.RENAL,
    latex=r"GFR = K_f \times NFP",
    simplified="GFR = K_f × NFP",
    description="Glomerular filtration rate determined by membrane permeability and driving pressure",
    compute_func=compute_gfr,
    parameters=[
        Parameter(
            name="K_f",
            description="Ultrafiltration coefficient (product of hydraulic conductivity and surface area)",
            units="mL/min/mmHg",
            symbol="K_f",
            physiological_range=(5, 15)
        ),
        Parameter(
            name="NFP",
            description="Net filtration pressure",
            units="mmHg",
            symbol="NFP",
            physiological_range=(5, 20)
        )
    ],
    depends_on=["renal.glomerular.net_filtration_pressure"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(gfr_from_nfp)
