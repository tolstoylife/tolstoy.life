"""Calcium absorption (active and passive)."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_calcium_absorption_fraction(Ca_intake: float, vitamin_D_status: float = 1.0, baseline: float = 0.15) -> float:
    """
    Calculate fractional calcium absorption.

    Active absorption (duodenum): TRPV6 → calbindin → PMCA/NCX
    Passive absorption (paracellular): throughout small intestine

    Parameters
    ----------
    Ca_intake : float
        Calcium intake (mg)
    vitamin_D_status : float
        Vitamin D status (0-1 scale), default 1.0 (normal)
    baseline : float
        Baseline absorption fraction, default 0.15

    Returns
    -------
    float
        Fractional calcium absorption (0-1)
    """
    max_absorption = 0.40
    fraction = baseline + (max_absorption - baseline) * vitamin_D_status
    return fraction


calcium_absorption = create_equation(
    id="gastrointestinal.absorption.calcium_absorption",
    name="Calcium Absorption (GI)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"f_{Ca} = f_{\text{baseline}} + (f_{\max} - f_{\text{baseline}}) \times \text{VitD}",
    simplified="f_Ca = f_baseline + (f_max - f_baseline) × VitD",
    description="Fractional Ca absorption. Active (duodenum, TRPV6) + passive (paracellular). ~30% of intake absorbed, higher with vitamin D",
    compute_func=compute_calcium_absorption_fraction,
    parameters=[
        Parameter(
            name="Ca_intake",
            description="Calcium intake",
            units="mg",
            symbol=r"\text{Ca}_{\text{intake}}",
            physiological_range=(200.0, 2000.0)
        ),
        Parameter(
            name="vitamin_D_status",
            description="Vitamin D status (0-1 scale)",
            units="dimensionless",
            symbol=r"\text{VitD}",
            default_value=1.0,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="baseline",
            description="Baseline absorption fraction",
            units="dimensionless",
            symbol=r"f_{\text{baseline}}",
            default_value=0.15,
            physiological_range=(0.10, 0.20)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(calcium_absorption)
