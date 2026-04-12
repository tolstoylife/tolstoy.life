"""Fick's law for transcapillary solute diffusion."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_ficks_law_diffusion(P_s: float, S: float, C_c: float, C_i: float) -> float:
    """
    Calculate solute flux across capillary wall by diffusion.

    Parameters
    ----------
    P_s : float
        Permeability coefficient (cm/s)
    S : float
        Capillary surface area (cm²)
    C_c : float
        Capillary solute concentration (mol/L or mg/dL)
    C_i : float
        Interstitial solute concentration (mol/L or mg/dL)

    Returns
    -------
    float
        Solute flux (amount/time in units consistent with inputs)
    """
    return P_s * S * (C_c - C_i)


ficks_law_diffusion = create_equation(
    id="cardiovascular.microcirculation.ficks_law_diffusion",
    name="Fick's Law for Capillary Diffusion",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"J_s = P_s \times S \times (C_c - C_i)",
    simplified="J_s = P_s × S × (C_c - C_i)",
    description="Diffusive solute flux across capillary wall",
    compute_func=compute_ficks_law_diffusion,
    parameters=[
        Parameter(
            name="P_s",
            description="Permeability coefficient",
            units="cm/s",
            symbol="P_s",
            physiological_range=(1e-7, 1e-3)
        ),
        Parameter(
            name="S",
            description="Capillary surface area",
            units="cm²",
            symbol="S",
            physiological_range=(100.0, 10000.0)
        ),
        Parameter(
            name="C_c",
            description="Capillary concentration",
            units="mol/L or mg/dL",
            symbol="C_c",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="C_i",
            description="Interstitial concentration",
            units="mol/L or mg/dL",
            symbol="C_i",
            physiological_range=(0.0, 1000.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.5"
    )
)

register_equation(ficks_law_diffusion)
