"""
Feedback gain in endocrine regulation.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_feedback_gain(delta_tropic: float, delta_target: float) -> float:
    """
    Calculate feedback loop gain.

    Parameters
    ----------
    delta_tropic : float
        Change in tropic hormone concentration
    delta_target : float
        Change in target hormone concentration

    Returns
    -------
    float
        Feedback gain G (dimensionless)

    Notes
    -----
    High gain = tight regulation around setpoint.
    Negative value indicates negative feedback.
    """
    return delta_tropic / delta_target


# Create equation
feedback_gain_equation = create_equation(
    id="endocrine.feedback.feedback_gain",
    name="Feedback Loop Gain",
    category=EquationCategory.ENDOCRINE,
    latex=r"G = \frac{\Delta[\text{Tropic}]}{\Delta[\text{Target}]}",
    simplified="G = Δ[Tropic] / Δ[Target]",
    description="Gain of negative feedback loop. High gain indicates tight regulation "
                "around hormonal setpoint. Determines sensitivity of response to perturbations.",
    compute_func=compute_feedback_gain,
    parameters=[
        Parameter(
            name="delta_tropic",
            description="Change in tropic hormone",
            units="arbitrary units",
            symbol=r"\Delta[\text{Tropic}]",
            physiological_range=(-100.0, 100.0)
        ),
        Parameter(
            name="delta_target",
            description="Change in target hormone",
            units="arbitrary units",
            symbol=r"\Delta[\text{Target}]",
            physiological_range=(-100.0, 100.0)
        )
    ],
    depends_on=["endocrine.feedback.negative_feedback_tropic", "endocrine.feedback.negative_feedback_target"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.3"
    )
)

# Register globally
register_equation(feedback_gain_equation)
