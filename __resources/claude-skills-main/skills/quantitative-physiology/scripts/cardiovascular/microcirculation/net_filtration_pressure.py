"""Net filtration pressure calculation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_net_filtration_pressure(
    P_c: float,
    P_i: float,
    pi_c: float,
    pi_i: float,
    sigma: float = 1.0
) -> float:
    """
    Calculate net filtration pressure across capillary wall.

    Parameters
    ----------
    P_c : float
        Capillary hydrostatic pressure (mmHg)
    P_i : float
        Interstitial hydrostatic pressure (mmHg)
    pi_c : float
        Capillary oncotic pressure (mmHg)
    pi_i : float
        Interstitial oncotic pressure (mmHg)
    sigma : float, optional
        Reflection coefficient (0-1, default: 1.0)

    Returns
    -------
    float
        Net filtration pressure (mmHg)
    """
    return (P_c - P_i) - sigma * (pi_c - pi_i)


net_filtration_pressure = create_equation(
    id="cardiovascular.microcirculation.net_filtration_pressure",
    name="Net Filtration Pressure",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{NFP} = (P_c - P_i) - \sigma(\pi_c - \pi_i)",
    simplified="NFP = (P_c - P_i) - σ(π_c - π_i)",
    description="Net driving force for capillary filtration",
    compute_func=compute_net_filtration_pressure,
    parameters=[
        Parameter(
            name="P_c",
            description="Capillary hydrostatic pressure",
            units="mmHg",
            symbol="P_c",
            physiological_range=(15.0, 35.0)
        ),
        Parameter(
            name="P_i",
            description="Interstitial hydrostatic pressure",
            units="mmHg",
            symbol="P_i",
            physiological_range=(-5.0, 2.0)
        ),
        Parameter(
            name="pi_c",
            description="Capillary oncotic pressure",
            units="mmHg",
            symbol=r"\pi_c",
            physiological_range=(20.0, 28.0)
        ),
        Parameter(
            name="pi_i",
            description="Interstitial oncotic pressure",
            units="mmHg",
            symbol=r"\pi_i",
            physiological_range=(3.0, 8.0)
        ),
        Parameter(
            name="sigma",
            description="Reflection coefficient",
            units="dimensionless",
            symbol=r"\sigma",
            default_value=1.0,
            physiological_range=(0.0, 1.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.5"
    )
)

register_equation(net_filtration_pressure)
