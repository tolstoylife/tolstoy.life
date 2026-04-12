"""
Negative feedback regulation of tropic hormone dynamics.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_tropic_derivative(target_conc: float, k_basal: float, k_fb: float) -> float:
    """
    Calculate rate of change of tropic hormone with feedback.

    Parameters
    ----------
    target_conc : float
        Target hormone concentration providing feedback
    k_basal : float
        Basal secretion rate
    k_fb : float
        Feedback inhibition constant

    Returns
    -------
    float
        d[Tropic]/dt
    """
    return k_basal - k_fb * target_conc


# Create equation
tropic_feedback_equation = create_equation(
    id="endocrine.feedback.negative_feedback_tropic",
    name="Tropic Hormone Dynamics (Negative Feedback)",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[\text{Tropic}]}{dt} = k_{basal} - k_{fb} \times [\text{Target}]",
    simplified="d[Tropic]/dt = k_basal - k_fb × [Target]",
    description="Rate equation for tropic hormone with negative feedback from target hormone. "
                "Steady-state setpoint: [Target]_ss = k_basal / k_fb.",
    compute_func=compute_tropic_derivative,
    parameters=[
        Parameter(
            name="target_conc",
            description="Target hormone concentration (feedback signal)",
            units="arbitrary units",
            symbol="[Target]",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="k_basal",
            description="Basal secretion rate",
            units="concentration/time",
            symbol="k_{basal}",
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k_fb",
            description="Feedback inhibition constant",
            units="1/time",
            symbol="k_{fb}",
            physiological_range=(0.001, 1.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.3"
    )
)

# Register globally
register_equation(tropic_feedback_equation)
