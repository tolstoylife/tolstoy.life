"""
Aldosterone regulation by angiotensin II and potassium.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_aldosterone_rate(AngII: float, K_plasma: float,
                             k_AngII: float = 1.0, k_K: float = 1.0) -> float:
    """
    Calculate aldosterone secretion rate.

    Parameters
    ----------
    AngII : float
        Angiotensin II concentration (primary stimulus)
    K_plasma : float
        Plasma potassium concentration (mM)
    k_AngII : float
        AngII sensitivity constant
    k_K : float
        K+ sensitivity constant

    Returns
    -------
    float
        Aldosterone secretion rate (proportional)

    Notes
    -----
    Primary stimuli:
    - Angiotensin II (RAAS activation)
    - Hyperkalemia (direct effect)
    - ACTH (minor, permissive)
    """
    return k_AngII * AngII * k_K * K_plasma


# Create equation
aldosterone_equation = create_equation(
    id="endocrine.adrenal.aldosterone_regulation",
    name="Aldosterone Regulation",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{Aldosterone} \propto [\text{Ang II}] \times [K^+]",
    simplified="Aldosterone ∝ [Ang II] × [K+]",
    description="Aldosterone secretion from zona glomerulosa. Primary regulation by "
                "angiotensin II (RAAS) and plasma potassium (hyperkalemia stimulates).",
    compute_func=compute_aldosterone_rate,
    parameters=[
        Parameter(
            name="AngII",
            description="Angiotensin II concentration",
            units="pg/mL",
            symbol="[Ang II]",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="K_plasma",
            description="Plasma potassium concentration",
            units="mM",
            symbol="[K^+]",
            physiological_range=(3.0, 6.0)
        ),
        Parameter(
            name="k_AngII",
            description="Angiotensin II sensitivity",
            units="arbitrary",
            symbol="k_{AngII}",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k_K",
            description="Potassium sensitivity",
            units="arbitrary",
            symbol="k_K",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.5"
    )
)

# Register globally
register_equation(aldosterone_equation)
