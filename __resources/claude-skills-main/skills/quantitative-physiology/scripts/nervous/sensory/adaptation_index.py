"""
Adaptation Index - Quantifies degree of receptor adaptation

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_adaptation_index(R_peak: float, R_ss: float) -> float:
    """
    Calculate adaptation index (fraction of response that adapts).

    Formula: AI = (R_peak - R_ss) / R_peak

    Parameters:
    -----------
    R_peak : float
        Peak initial response
    R_ss : float
        Steady-state sustained response

    Returns:
    --------
    AI : float
        Adaptation index (0-1)

    Notes:
    ------
    Quantifies the degree of adaptation:
    - AI ≈ 0: Purely tonic (no adaptation)
    - AI ≈ 0.5: Mixed response
    - AI ≈ 1: Purely phasic (complete adaptation)

    Examples:
    - Merkel disc (slowly adapting): AI ≈ 0.1-0.3
    - Meissner corpuscle (rapidly adapting): AI ≈ 0.6-0.8
    - Pacinian corpuscle (very rapidly adapting): AI ≈ 0.9-1.0
    """
    if R_peak == 0:
        return 0.0
    return (R_peak - R_ss) / R_peak


# Create and register atomic equation
adaptation_index = create_equation(
    id="nervous.sensory.adaptation_index",
    name="Adaptation Index",
    category=EquationCategory.NERVOUS,
    latex=r"AI = \frac{R_{peak} - R_{ss}}{R_{peak}}",
    simplified="AI = (R_peak - R_ss) / R_peak",
    description="Adaptation index quantifies the fraction of response that decays during sustained stimulation. AI=0 is purely tonic, AI=1 is purely phasic.",
    compute_func=compute_adaptation_index,
    parameters=[
        Parameter(
            name="R_peak",
            description="Peak initial response",
            units="arbitrary",
            symbol="R_{peak}",
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
    ],
    depends_on=["nervous.sensory.receptor_adaptation"],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(adaptation_index)
