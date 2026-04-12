"""
Spike-Timing Dependent Plasticity (STDP) - Timing-based synaptic modification

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_stdp(delta_t: float, A_plus: float, A_minus: float,
                 tau_plus: float = 20.0, tau_minus: float = 20.0) -> float:
    """
    Calculate weight change according to STDP rule.

    Formula:
    Δw = A₊ × e^(-Δt/τ₊)  if Δt > 0 (pre before post → LTP)
    Δw = -A₋ × e^(Δt/τ₋)   if Δt < 0 (post before pre → LTD)

    Parameters:
    -----------
    delta_t : float
        Spike time difference: t_post - t_pre (ms)
    A_plus : float
        LTP amplitude (maximum weight increase)
    A_minus : float
        LTD amplitude (maximum weight decrease)
    tau_plus : float
        LTP time constant (ms), default 20 ms
    tau_minus : float
        LTD time constant (ms), default 20 ms

    Returns:
    --------
    delta_w : float
        Weight change

    Notes:
    ------
    STDP implements Hebb's rule: "neurons that fire together wire together"
    Positive Δt (pre → post): LTP (potentiation)
    Negative Δt (post → pre): LTD (depression)
    Critical window: ±40-50 ms
    """
    if delta_t > 0:
        # Pre before post: LTP
        return A_plus * np.exp(-delta_t / tau_plus)
    else:
        # Post before pre: LTD
        return -A_minus * np.exp(delta_t / tau_minus)


# Create and register atomic equation
stdp = create_equation(
    id="nervous.plasticity.stdp",
    name="Spike-Timing Dependent Plasticity",
    category=EquationCategory.NERVOUS,
    latex=r"\Delta w = \begin{cases} A_+ \times e^{-\Delta t/\tau_+} & \text{if } \Delta t > 0 \\ -A_- \times e^{\Delta t/\tau_-} & \text{if } \Delta t < 0 \end{cases}",
    simplified="Δw = A₊×e^(-Δt/τ₊) if Δt>0, -A₋×e^(Δt/τ₋) if Δt<0",
    description="Spike-timing dependent plasticity: synaptic weight changes depend on precise timing of pre- and postsynaptic spikes. Pre→post causes LTP, post→pre causes LTD.",
    compute_func=compute_stdp,
    parameters=[
        Parameter(
            name="delta_t",
            description="Spike time difference (post - pre)",
            units="ms",
            symbol=r"\Delta t",
            default_value=None,
            physiological_range=(-100.0, 100.0)
        ),
        Parameter(
            name="A_plus",
            description="LTP amplitude",
            units="dimensionless",
            symbol="A_+",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="A_minus",
            description="LTD amplitude",
            units="dimensionless",
            symbol="A_-",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="tau_plus",
            description="LTP time constant",
            units="ms",
            symbol=r"\tau_+",
            default_value=20.0,
            physiological_range=(5.0, 50.0)
        ),
        Parameter(
            name="tau_minus",
            description="LTD time constant",
            units="ms",
            symbol=r"\tau_-",
            default_value=20.0,
            physiological_range=(5.0, 50.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.6")
)

register_equation(stdp)
