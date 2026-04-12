"""
NCX Reversal Potential - Na+/Ca2+ exchanger equilibrium potential

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_ncx_reversal(E_Na: float, E_Ca: float) -> float:
    """
    Calculate Na+/Ca2+ exchanger reversal potential.

    Formula: E_NCX = 3E_Na - 2E_Ca

    The NCX exchanges 3 Na+ for 1 Ca2+, making it electrogenic.

    Parameters:
    -----------
    E_Na : float
        Sodium reversal potential (mV)
    E_Ca : float
        Calcium reversal potential (mV)

    Returns:
    --------
    E_NCX : float
        NCX reversal potential (mV)

    Notes:
        When V_m > E_NCX: Ca2+ extrusion (forward mode)
        When V_m < E_NCX: Ca2+ influx (reverse mode)
    """
    return 3 * E_Na - 2 * E_Ca


# Create and register atomic equation
ncx_reversal = create_equation(
    id="membrane.transport.ncx_reversal",
    name="Na+/Ca2+ Exchanger Reversal Potential",
    category=EquationCategory.MEMBRANE,
    latex=r"E_{NCX} = 3E_{Na} - 2E_{Ca}",
    simplified="E_NCX = 3*E_Na - 2*E_Ca",
    description="Reversal potential for the Na+/Ca2+ exchanger (NCX), which exchanges 3 Na+ for 1 Ca2+ (electrogenic).",
    compute_func=compute_ncx_reversal,
    parameters=[
        Parameter(
            name="E_Na",
            description="Sodium reversal potential",
            units="mV",
            symbol="E_{Na}",
            default_value=None,
            physiological_range=(40.0, 70.0)
        ),
        Parameter(
            name="E_Ca",
            description="Calcium reversal potential",
            units="mV",
            symbol="E_{Ca}",
            default_value=None,
            physiological_range=(100.0, 150.0)
        ),
    ],
    depends_on=[],  # Could depend on Nernst equation
    metadata=EquationMetadata(source_unit=2, source_chapter="2.3")
)

register_equation(ncx_reversal)
