"""
Negative feedback regulation of target hormone dynamics.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_target_derivative(tropic_conc: float, target_conc: float,
                               k_stim: float, k_deg: float) -> float:
    """
    Calculate rate of change of target hormone concentration.

    Parameters
    ----------
    tropic_conc : float
        Tropic hormone concentration (e.g., TSH, ACTH)
    target_conc : float
        Target hormone concentration (e.g., T4, cortisol)
    k_stim : float
        Stimulation rate constant (1/time)
    k_deg : float
        Degradation rate constant (1/time)

    Returns
    -------
    float
        d[Target]/dt
    """
    return k_stim * tropic_conc - k_deg * target_conc


# Create equation
target_feedback_equation = create_equation(
    id="endocrine.feedback.negative_feedback_target",
    name="Target Hormone Dynamics (Negative Feedback)",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[\text{Target}]}{dt} = k_{stim} \times [\text{Tropic}] - k_{deg} \times [\text{Target}]",
    simplified="d[Target]/dt = k_stim × [Tropic] - k_deg × [Target]",
    description="Rate equation for target hormone under tropic hormone stimulation. "
                "Used in negative feedback loops (e.g., TSH→T4, ACTH→cortisol).",
    compute_func=compute_target_derivative,
    parameters=[
        Parameter(
            name="tropic_conc",
            description="Tropic hormone concentration",
            units="arbitrary units",
            symbol="[Tropic]",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="target_conc",
            description="Target hormone concentration",
            units="arbitrary units",
            symbol="[Target]",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="k_stim",
            description="Stimulation rate constant",
            units="1/time",
            symbol="k_{stim}",
            physiological_range=(0.01, 10.0)
        ),
        Parameter(
            name="k_deg",
            description="Degradation rate constant",
            units="1/time",
            symbol="k_{deg}",
            physiological_range=(0.001, 1.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.3"
    )
)

# Register globally
register_equation(target_feedback_equation)
