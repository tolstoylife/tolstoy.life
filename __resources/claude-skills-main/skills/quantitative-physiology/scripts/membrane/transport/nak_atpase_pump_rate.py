"""
Na+/K+-ATPase Pump Rate - Sodium-potassium pump kinetics

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_nak_pump_rate(Na_in: float, K_out: float, ATP: float,
                          J_max: float = 200.0, K_Na: float = 10.0,
                          K_K: float = 2.0, K_ATP: float = 0.5) -> float:
    """
    Calculate Na+/K+-ATPase pump rate.

    Formula: J_pump = J_max × f([Na+]_i, [K+]_o, [ATP])
    where f includes Hill-type cooperativity for Na+ and K+

    Parameters:
    -----------
    Na_in : float
        Intracellular Na+ concentration (mM)
    K_out : float
        Extracellular K+ concentration (mM)
    ATP : float
        Intracellular ATP concentration (mM)
    J_max : float
        Maximum pump rate (cycles/s), default: 200
    K_Na : float
        Half-saturation for Na+ (mM), default: 10
    K_K : float
        Half-saturation for K+ (mM), default: 2
    K_ATP : float
        Half-saturation for ATP (mM), default: 0.5

    Returns:
    --------
    J_pump : float
        Pump rate (cycles/s)
        Stoichiometry: 3 Na+ out : 2 K+ in per cycle

    Typical pump rate: 100-300 cycles/second
    """
    # Hill cooperativity: n=3 for Na+, n=2 for K+
    f_Na = (Na_in / K_Na)**3 / (1 + (Na_in / K_Na)**3)
    f_K = (K_out / K_K)**2 / (1 + (K_out / K_K)**2)
    f_ATP = ATP / (K_ATP + ATP)

    return J_max * f_Na * f_K * f_ATP


# Create and register atomic equation
nak_pump_rate = create_equation(
    id="membrane.transport.nak_pump_rate",
    name="Na+/K+-ATPase Pump Rate",
    category=EquationCategory.MEMBRANE,
    latex=r"J_{pump} = J_{max} \cdot f_{Na} \cdot f_K \cdot f_{ATP}",
    simplified="J_pump = J_max * f_Na * f_K * f_ATP",
    description="Rate of the Na+/K+-ATPase pump with cooperative binding kinetics (3 Na+ out, 2 K+ in per ATP).",
    compute_func=compute_nak_pump_rate,
    parameters=[
        Parameter(
            name="Na_in",
            description="Intracellular Na+ concentration",
            units="mM",
            symbol="[Na^+]_i",
            default_value=None,
            physiological_range=(5.0, 50.0)
        ),
        Parameter(
            name="K_out",
            description="Extracellular K+ concentration",
            units="mM",
            symbol="[K^+]_o",
            default_value=None,
            physiological_range=(2.0, 10.0)
        ),
        Parameter(
            name="ATP",
            description="Intracellular ATP concentration",
            units="mM",
            symbol="[ATP]",
            default_value=None,
            physiological_range=(1.0, 10.0)
        ),
        Parameter(
            name="J_max",
            description="Maximum pump rate",
            units="cycles/s",
            symbol="J_{max}",
            default_value=200.0,
            physiological_range=(100.0, 300.0)
        ),
        Parameter(
            name="K_Na",
            description="Half-saturation constant for Na+",
            units="mM",
            symbol="K_{Na}",
            default_value=10.0
        ),
        Parameter(
            name="K_K",
            description="Half-saturation constant for K+",
            units="mM",
            symbol="K_K",
            default_value=2.0
        ),
        Parameter(
            name="K_ATP",
            description="Half-saturation constant for ATP",
            units="mM",
            symbol="K_{ATP}",
            default_value=0.5
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.3")
)

register_equation(nak_pump_rate)
