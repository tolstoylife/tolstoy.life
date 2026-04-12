"""
NMDA Receptor Mg2+ Block - Voltage-dependent magnesium block

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_nmda_mg_block(V: float, Mg_out: float = 1.0, K_Mg: float = 3.6, V_half: float = -17.0) -> float:
    """
    Calculate voltage-dependent Mg2+ block factor for NMDA receptors.

    Formula: g_NMDA(V) = g_max / (1 + [Mg²⁺]_o/K_Mg × e^(-V/V_half))

    Parameters:
    -----------
    V : float
        Membrane potential (mV)
    Mg_out : float
        External magnesium concentration (mM), default 1.0 mM
    K_Mg : float
        Mg2+ affinity constant (mM), default 3.6 mM
    V_half : float
        Half-maximal voltage (mV), default -17 mV

    Returns:
    --------
    block_factor : float
        Fraction of unblocked conductance (0-1)

    Notes:
    ------
    At rest (V ≈ -70 mV): strong block, minimal conductance
    During depolarization: block relieved, conductance increases
    This voltage dependence makes NMDA receptors coincidence detectors
    """
    return 1.0 / (1.0 + (Mg_out / K_Mg) * np.exp(-V / V_half))


# Create and register atomic equation
nmda_mg_block = create_equation(
    id="nervous.synaptic.nmda_mg_block",
    name="NMDA Receptor Mg2+ Block",
    category=EquationCategory.NERVOUS,
    latex=r"g_{NMDA}(V) = \frac{g_{max}}{1 + \frac{[Mg^{2+}]_o}{K_{Mg}} \times e^{-V/V_{half}}}",
    simplified="g_NMDA(V) = g_max / (1 + [Mg]_o/K_Mg × e^(-V/V_half))",
    description="Voltage-dependent magnesium block of NMDA receptors. At rest, Mg2+ blocks the pore; depolarization relieves block, making NMDA receptors coincidence detectors.",
    compute_func=compute_nmda_mg_block,
    parameters=[
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            default_value=None,
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="Mg_out",
            description="External magnesium concentration",
            units="mM",
            symbol="[Mg^{2+}]_o",
            default_value=1.0,
            physiological_range=(0.1, 5.0)
        ),
        Parameter(
            name="K_Mg",
            description="Mg2+ affinity constant",
            units="mM",
            symbol="K_{Mg}",
            default_value=3.6,
            physiological_range=(1.0, 10.0)
        ),
        Parameter(
            name="V_half",
            description="Half-maximal voltage",
            units="mV",
            symbol="V_{half}",
            default_value=-17.0,
            physiological_range=(-30.0, 0.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.2")
)

register_equation(nmda_mg_block)
