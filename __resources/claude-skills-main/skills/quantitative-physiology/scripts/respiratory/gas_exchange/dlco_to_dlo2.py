"""DLCO to DLO2 Conversion equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_dlco_to_dlo2(D_LCO: float) -> float:
    """
    Convert CO diffusing capacity to O2 diffusing capacity.

    D_LO2 ≈ 1.23 × D_LCO

    Parameters
    ----------
    D_LCO : float
        CO diffusing capacity (mL/(min·mmHg))

    Returns
    -------
    float
        O2 diffusing capacity (mL/(min·mmHg))
    """
    return 1.23 * D_LCO


# Create equation
dlco_to_dlo2 = create_equation(
    id="respiratory.gas_exchange.dlco_to_dlo2",
    name="DLCO to DLO2 Conversion",
    category=EquationCategory.RESPIRATORY,
    latex=r"D_{LO2} \approx 1.23 \times D_{LCO}",
    simplified="D_LO2 ≈ 1.23 × D_LCO",
    description="Convert carbon monoxide diffusing capacity to oxygen diffusing capacity",
    compute_func=compute_dlco_to_dlo2,
    parameters=[
        Parameter(
            name="D_LCO",
            description="CO diffusing capacity",
            units="mL/(min·mmHg)",
            symbol="D_{LCO}",
            default_value=25.0,
            physiological_range=(15.0, 40.0)
        )
    ],
    depends_on=["respiratory.gas_exchange.diffusing_capacity"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(dlco_to_dlo2)
