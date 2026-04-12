"""
Calcium-Triggered Release (Cooperative Binding Model) - Vesicle release probability

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_ca_release_cooperative(Ca: float, K_d: float = 15.0) -> float:
    """
    Calculate vesicle release probability using cooperative Ca2+ binding model.

    Formula: P_release = [Ca²⁺]⁴ / (K_d⁴ + [Ca²⁺]⁴)

    Parameters:
    -----------
    Ca : float
        Calcium concentration (μM)
    K_d : float
        Dissociation constant for release machinery (μM), default 15.0 μM

    Returns:
    --------
    P_release : float
        Release probability (0-1)

    Notes:
    ------
    The fourth-power relationship (n≈3-4) reflects cooperative binding
    of ~4 Ca2+ ions to synaptotagmin in the release machinery.
    K_d typically ranges from 10-20 μM for fast release.
    """
    return Ca**4 / (K_d**4 + Ca**4)


# Create and register atomic equation
ca_release_cooperative = create_equation(
    id="nervous.synaptic.ca_release_cooperative",
    name="Calcium-Triggered Release (Cooperative Binding)",
    category=EquationCategory.NERVOUS,
    latex=r"P_{release} = \frac{[Ca^{2+}]^4}{K_d^4 + [Ca^{2+}]^4}",
    simplified="P_release = [Ca]^4 / (K_d^4 + [Ca]^4)",
    description="Vesicle release probability based on cooperative calcium binding to release machinery (synaptotagmin). The fourth-power dependence reflects ~4 Ca2+ binding sites.",
    compute_func=compute_ca_release_cooperative,
    parameters=[
        Parameter(
            name="Ca",
            description="Calcium concentration",
            units="μM",
            symbol="[Ca^{2+}]",
            default_value=None,
            physiological_range=(0.1, 100.0)
        ),
        Parameter(
            name="K_d",
            description="Dissociation constant for release machinery",
            units="μM",
            symbol="K_d",
            default_value=15.0,
            physiological_range=(5.0, 30.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(ca_release_cooperative)
