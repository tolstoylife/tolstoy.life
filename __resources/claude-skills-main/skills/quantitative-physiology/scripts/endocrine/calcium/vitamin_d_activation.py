"""
1,25(OH)2D (calcitriol) production rate from 25(OH)D.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_vitamin_d_activation(PTH: float, phosphate: float, FGF23: float,
                                 k_PTH: float = 1.0, k_phos: float = 0.5,
                                 k_FGF23: float = 0.3) -> float:
    """
    Calculate 1,25(OH)2D production rate (1α-hydroxylase activity).

    Parameters
    ----------
    PTH : float
        PTH concentration (stimulates)
    phosphate : float
        Plasma phosphate concentration (mM)
    FGF23 : float
        FGF23 concentration (inhibits)
    k_PTH : float
        PTH stimulation constant
    k_phos : float
        Hypophosphatemia stimulation constant
    k_FGF23 : float
        FGF23 inhibition constant

    Returns
    -------
    float
        1,25(OH)2D production rate (proportional)

    Notes
    -----
    Synthesis pathway:
    7-dehydrocholesterol → (UV-B) → Vitamin D3
    → (Liver 25-hydroxylase) → 25(OH)D
    → (Kidney 1α-hydroxylase) → 1,25(OH)2D (calcitriol)

    1α-hydroxylase regulation:
    - Stimulators: PTH, hypophosphatemia
    - Inhibitors: 1,25(OH)2D (feedback), FGF23, hypercalcemia

    Normal ranges:
    - 25(OH)D: 30-100 ng/mL (sufficient)
    - 1,25(OH)2D: 20-60 pg/mL
    """
    stimulation = k_PTH * PTH + k_phos / (phosphate + 0.1)
    inhibition = 1.0 + k_FGF23 * FGF23
    return stimulation / inhibition


# Create equation
vitamin_d_activation_equation = create_equation(
    id="endocrine.calcium.vitamin_d_activation",
    name="Vitamin D Activation (1α-hydroxylase)",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{1,25(OH)}_2\text{D production} = \frac{k_{PTH} \times PTH + \frac{k_{phos}}{[PO_4] + 0.1}}{1 + k_{FGF23} \times FGF23}",
    simplified="1,25(OH)2D_production = (k_PTH×PTH + k_phos/[PO4]) / (1 + k_FGF23×FGF23)",
    description="1,25(OH)2D (calcitriol) production via renal 1α-hydroxylase. "
                "Stimulated by PTH and low phosphate, inhibited by FGF23.",
    compute_func=compute_vitamin_d_activation,
    parameters=[
        Parameter(
            name="PTH",
            description="PTH concentration",
            units="pg/mL",
            symbol="PTH",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="phosphate",
            description="Plasma phosphate concentration",
            units="mM",
            symbol="[PO_4]",
            physiological_range=(0.5, 3.0)
        ),
        Parameter(
            name="FGF23",
            description="FGF23 concentration",
            units="arbitrary units",
            symbol="FGF23",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="k_PTH",
            description="PTH stimulation constant",
            units="arbitrary",
            symbol="k_{PTH}",
            default_value=1.0,
            physiological_range=(0.1, 5.0)
        ),
        Parameter(
            name="k_phos",
            description="Hypophosphatemia stimulation constant",
            units="arbitrary",
            symbol="k_{phos}",
            default_value=0.5,
            physiological_range=(0.1, 2.0)
        ),
        Parameter(
            name="k_FGF23",
            description="FGF23 inhibition constant",
            units="arbitrary",
            symbol="k_{FGF23}",
            default_value=0.3,
            physiological_range=(0.1, 1.0)
        )
    ],
    depends_on=["endocrine.calcium.pth_secretion"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.7"
    )
)

# Register globally
register_equation(vitamin_d_activation_equation)
