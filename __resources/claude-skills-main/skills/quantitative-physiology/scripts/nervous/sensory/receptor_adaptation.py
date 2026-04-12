"""
Receptor Adaptation - First-order adaptation dynamics

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_receptor_adaptation(t: float, R_0: float, R_ss: float, tau_adapt: float) -> float:
    """
    Calculate receptor response during adaptation.

    Formula: R(t) = R_ss + (R_0 - R_ss) × e^(-t/τ_adapt)

    Parameters:
    -----------
    t : float
        Time after stimulus onset (s)
    R_0 : float
        Initial response (peak)
    R_ss : float
        Steady-state response
    tau_adapt : float
        Adaptation time constant (s)

    Returns:
    --------
    R : float
        Receptor response at time t

    Notes:
    ------
    First-order adaptation model describes decay from initial to sustained response.
    Adaptation index: AI = (R_0 - R_ss) / R_0
    - Phasic receptors: High AI (≈0.8-1.0), rapid adaptation (Pacinian corpuscle)
    - Tonic receptors: Low AI (≈0-0.3), sustained response (Merkel disc)
    """
    return R_ss + (R_0 - R_ss) * np.exp(-t / tau_adapt)


# Create and register atomic equation
receptor_adaptation = create_equation(
    id="nervous.sensory.receptor_adaptation",
    name="Receptor Adaptation",
    category=EquationCategory.NERVOUS,
    latex=r"R(t) = R_{ss} + (R_0 - R_{ss}) \times e^{-t/\tau_{adapt}}",
    simplified="R(t) = R_ss + (R_0 - R_ss) × e^(-t/τ_adapt)",
    description="First-order model of receptor adaptation: response decays exponentially from initial peak to steady-state level. Characterizes phasic vs tonic receptors.",
    compute_func=compute_receptor_adaptation,
    parameters=[
        Parameter(
            name="t",
            description="Time after stimulus onset",
            units="s",
            symbol="t",
            default_value=None,
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="R_0",
            description="Initial response (peak)",
            units="arbitrary",
            symbol="R_0",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="R_ss",
            description="Steady-state response",
            units="arbitrary",
            symbol="R_{ss}",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="tau_adapt",
            description="Adaptation time constant",
            units="s",
            symbol=r"\tau_{adapt}",
            default_value=None,
            physiological_range=(0.01, 100.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(receptor_adaptation)
