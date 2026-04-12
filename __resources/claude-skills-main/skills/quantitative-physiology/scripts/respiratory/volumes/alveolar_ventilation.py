"""Alveolar Ventilation equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_alveolar_ventilation(VT: float, VD: float, f: float) -> float:
    """
    Calculate alveolar ventilation (effective gas exchange).

    V_A = (VT - VD) × f

    Parameters
    ----------
    VT : float
        Tidal volume (mL)
    VD : float
        Dead space volume (mL)
    f : float
        Respiratory frequency (breaths/min)

    Returns
    -------
    float
        Alveolar ventilation (mL/min)
    """
    return (VT - VD) * f


# Create equation
alveolar_ventilation = create_equation(
    id="respiratory.volumes.alveolar_ventilation",
    name="Alveolar Ventilation",
    category=EquationCategory.RESPIRATORY,
    latex=r"\dot{V}_A = (V_T - V_D) \times f",
    simplified="V_A = (VT - VD) × f",
    description="Effective ventilation reaching alveoli for gas exchange",
    compute_func=compute_alveolar_ventilation,
    parameters=[
        Parameter(
            name="VT",
            description="Tidal volume",
            units="mL",
            symbol="V_T",
            default_value=500.0,
            physiological_range=(400.0, 700.0)
        ),
        Parameter(
            name="VD",
            description="Dead space volume",
            units="mL",
            symbol="V_D",
            default_value=150.0,
            physiological_range=(100.0, 200.0)
        ),
        Parameter(
            name="f",
            description="Respiratory frequency",
            units="breaths/min",
            symbol="f",
            default_value=12.0,
            physiological_range=(10.0, 20.0)
        )
    ],
    depends_on=["respiratory.volumes.minute_ventilation"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(alveolar_ventilation)
