"""Bramwell-Hill equation for pulse wave velocity."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_bramwell_hill(V: float, dP: float, dV: float, rho: float = 1060.0) -> float:
    """
    Calculate pulse wave velocity using Bramwell-Hill equation.

    Parameters
    ----------
    V : float
        Volume (mL)
    dP : float
        Pressure change (mmHg)
    dV : float
        Volume change (mL)
    rho : float, optional
        Blood density (kg/m³, default: 1060)

    Returns
    -------
    float
        Pulse wave velocity (m/s)
    """
    # Convert mmHg to Pa: 1 mmHg = 133.322 Pa
    # Convert mL to m³: 1 mL = 1e-6 m³
    dP_Pa = dP * 133.322
    V_m3 = V * 1e-6
    dV_m3 = dV * 1e-6

    return np.sqrt((V_m3 * dP_Pa) / (rho * dV_m3))


bramwell_hill = create_equation(
    id="cardiovascular.hemodynamics.bramwell_hill_pwv",
    name="Bramwell-Hill Pulse Wave Velocity",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{PWV} = \sqrt{\frac{V \, dP}{\rho \, dV}} = \sqrt{\frac{1}{\rho C_A}}",
    simplified="PWV = √(V·dP / ρ·dV)",
    description="Pulse wave velocity from arterial compliance",
    compute_func=compute_bramwell_hill,
    parameters=[
        Parameter(
            name="V",
            description="Arterial volume",
            units="mL",
            symbol="V",
            physiological_range=(500.0, 1000.0)
        ),
        Parameter(
            name="dP",
            description="Pressure change",
            units="mmHg",
            symbol="dP",
            physiological_range=(20.0, 60.0)
        ),
        Parameter(
            name="dV",
            description="Volume change",
            units="mL",
            symbol="dV",
            physiological_range=(10.0, 50.0)
        ),
        Parameter(
            name="rho",
            description="Blood density",
            units="kg/m³",
            symbol=r"\rho",
            default_value=1060.0,
            physiological_range=(1050.0, 1070.0)
        )
    ],
    depends_on=["cardiovascular.hemodynamics.vascular_compliance"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(bramwell_hill)
