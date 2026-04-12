"""
Net Filtration Pressure (NFP) - Starling Forces in the Glomerulus.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_nfp(P_GC: float, P_BC: float, pi_GC: float, pi_BC: float = 0.0) -> float:
    """
    Calculate net filtration pressure using Starling forces.

    Args:
        P_GC: Glomerular capillary pressure (mmHg)
        P_BC: Bowman's capsule pressure (mmHg)
        pi_GC: Glomerular capillary oncotic pressure (mmHg)
        pi_BC: Bowman's capsule oncotic pressure (mmHg, typically 0)

    Returns:
        NFP: Net filtration pressure (mmHg)
    """
    return P_GC - P_BC - pi_GC + pi_BC


# Create equation
net_filtration_pressure = create_equation(
    id="renal.glomerular.net_filtration_pressure",
    name="Glomerular Net Filtration Pressure",
    category=EquationCategory.RENAL,
    latex=r"NFP = P_{GC} - P_{BC} - \pi_{GC} + \pi_{BC}",
    simplified="NFP = P_GC - P_BC - π_GC + π_BC",
    description="Net pressure driving glomerular filtration based on Starling forces",
    compute_func=compute_nfp,
    parameters=[
        Parameter(
            name="P_GC",
            description="Glomerular capillary hydrostatic pressure",
            units="mmHg",
            symbol="P_{GC}",
            physiological_range=(50, 70)
        ),
        Parameter(
            name="P_BC",
            description="Bowman's capsule hydrostatic pressure",
            units="mmHg",
            symbol="P_{BC}",
            physiological_range=(10, 20)
        ),
        Parameter(
            name="pi_GC",
            description="Glomerular capillary oncotic pressure",
            units="mmHg",
            symbol=r"\pi_{GC}",
            physiological_range=(25, 35)
        ),
        Parameter(
            name="pi_BC",
            description="Bowman's capsule oncotic pressure",
            units="mmHg",
            symbol=r"\pi_{BC}",
            default_value=0.0,
            physiological_range=(0, 2)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(net_filtration_pressure)
