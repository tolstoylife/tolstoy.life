"""
Basal body temperature elevation from progesterone.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_temperature_elevation(progesterone: float,
                                  T_baseline: float = 36.5) -> float:
    """
    Calculate basal body temperature from progesterone effect.

    Parameters
    ----------
    progesterone : float
        Progesterone concentration (ng/mL)
    T_baseline : float
        Baseline body temperature (°C)

    Returns
    -------
    float
        Body temperature (°C)

    Notes
    -----
    Progesterone is thermogenic:
    - Increases basal body temperature ~0.3°C
    - Temperature rise occurs after ovulation (luteal phase)
    - Used for natural family planning (fertility awareness)

    Progesterone across cycle:
    - Follicular phase: <1 ng/mL (low, no temp rise)
    - Luteal phase: 5-20 ng/mL (high, temp elevation)

    Temperature shift indicates ovulation has occurred.
    """
    delta_T = 0.3 * progesterone / (5.0 + progesterone)
    return T_baseline + delta_T


# Create equation
progesterone_temp_equation = create_equation(
    id="endocrine.reproductive.progesterone_temperature",
    name="Progesterone Basal Body Temperature",
    category=EquationCategory.ENDOCRINE,
    latex=r"T = T_{baseline} + 0.3 \times \frac{[P_4]}{5 + [P_4]}",
    simplified="T = T_baseline + 0.3 × [P4] / (5 + [P4])",
    description="Basal body temperature elevation from progesterone thermogenic effect. "
                "Temperature rises ~0.3°C in luteal phase after ovulation.",
    compute_func=compute_temperature_elevation,
    parameters=[
        Parameter(
            name="progesterone",
            description="Progesterone (P4) concentration",
            units="ng/mL",
            symbol="[P_4]",
            physiological_range=(0.0, 25.0)
        ),
        Parameter(
            name="T_baseline",
            description="Baseline body temperature",
            units="°C",
            symbol="T_{baseline}",
            default_value=36.5,
            physiological_range=(36.0, 37.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.8"
    )
)

# Register globally
register_equation(progesterone_temp_equation)
