"""Starling equation for capillary fluid filtration."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_starling_filtration(
    L_p: float,
    S: float,
    P_c: float,
    P_i: float,
    pi_c: float,
    pi_i: float,
    sigma: float = 1.0
) -> float:
    """
    Calculate fluid filtration rate across capillary wall.

    Parameters
    ----------
    L_p : float
        Hydraulic conductivity (mL/(min·mmHg·cm²))
    S : float
        Capillary surface area (cm²)
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
        Fluid flux (mL/min), positive = filtration
    """
    return L_p * S * ((P_c - P_i) - sigma * (pi_c - pi_i))


starling_filtration = create_equation(
    id="cardiovascular.microcirculation.starling_filtration",
    name="Starling Equation for Fluid Filtration",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"J_v = L_p \times S \times [(P_c - P_i) - \sigma(\pi_c - \pi_i)]",
    simplified="J_v = L_p × S × [(P_c - P_i) - σ(π_c - π_i)]",
    description="Net fluid flux across capillary wall determined by balance of hydrostatic and oncotic forces",
    compute_func=compute_starling_filtration,
    parameters=[
        Parameter(
            name="L_p",
            description="Hydraulic conductivity",
            units="mL/(min·mmHg·cm²)",
            symbol="L_p",
            physiological_range=(1e-7, 1e-5)
        ),
        Parameter(
            name="S",
            description="Capillary surface area",
            units="cm²",
            symbol="S",
            physiological_range=(100.0, 10000.0)
        ),
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

register_equation(starling_filtration)
