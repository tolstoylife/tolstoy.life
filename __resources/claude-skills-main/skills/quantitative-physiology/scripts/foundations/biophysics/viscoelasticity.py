"""
Viscoelastic Models (Kelvin-Voigt and Maxwell)

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 37-38)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def kelvin_voigt_stress(E: float, eta: float, epsilon: float, d_epsilon_dt: float) -> float:
    """
    Calculate stress in a Kelvin-Voigt viscoelastic material.

    Formula: σ = E × ε + η × (dε/dt)

    The Kelvin-Voigt model represents a spring (elastic) and dashpot (viscous)
    in parallel. Describes creep behavior of biological tissues like
    cartilage and cytoplasm.

    Parameters:
    -----------
    E : float - Elastic modulus (Pa)
    eta : float - Viscosity coefficient (Pa·s)
    epsilon : float - Strain (dimensionless)
    d_epsilon_dt : float - Strain rate (1/s)

    Returns:
    --------
    sigma : float - Stress (Pa)
    """
    return E * epsilon + eta * d_epsilon_dt


def kelvin_voigt_creep(sigma_0: float, E: float, eta: float, t: float) -> float:
    """
    Calculate strain during creep for Kelvin-Voigt model.

    Formula: ε(t) = (σ₀/E) × [1 - e^(-Et/η)]

    Describes time-dependent strain response to constant stress.

    Parameters:
    -----------
    sigma_0 : float - Applied constant stress (Pa)
    E : float - Elastic modulus (Pa)
    eta : float - Viscosity coefficient (Pa·s)
    t : float - Time (s)

    Returns:
    --------
    epsilon : float - Strain (dimensionless)
    """
    tau = eta / E  # Retardation time
    return (sigma_0 / E) * (1 - np.exp(-t / tau))


def maxwell_stress_relaxation(E: float, epsilon_0: float, eta: float, t: float) -> float:
    """
    Calculate stress relaxation in a Maxwell viscoelastic material.

    Formula: σ(t) = E × ε₀ × e^(-Et/η)

    The Maxwell model represents a spring and dashpot in series.
    Describes stress relaxation in biological tissues.

    Parameters:
    -----------
    E : float - Elastic modulus (Pa)
    epsilon_0 : float - Initial strain (dimensionless)
    eta : float - Viscosity coefficient (Pa·s)
    t : float - Time (s)

    Returns:
    --------
    sigma : float - Stress at time t (Pa)
    """
    tau = eta / E  # Relaxation time
    return E * epsilon_0 * np.exp(-t / tau)


def maxwell_strain_rate(sigma: float, E: float, eta: float, d_sigma_dt: float) -> float:
    """
    Calculate strain rate in Maxwell model.

    Formula: dε/dt = (1/E) × (dσ/dt) + σ/η

    Parameters:
    -----------
    sigma : float - Current stress (Pa)
    E : float - Elastic modulus (Pa)
    eta : float - Viscosity coefficient (Pa·s)
    d_sigma_dt : float - Stress rate (Pa/s)

    Returns:
    --------
    d_epsilon_dt : float - Strain rate (1/s)
    """
    return (1 / E) * d_sigma_dt + sigma / eta


# Create and register Kelvin-Voigt equation
kelvin_voigt_eq = create_equation(
    id="foundations.biophysics.kelvin_voigt",
    name="Kelvin-Voigt Viscoelastic Model",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\sigma = E\varepsilon + \eta\frac{d\varepsilon}{dt}",
    simplified="σ = E×ε + η×(dε/dt)",
    description="Stress in viscoelastic material with parallel spring-dashpot",
    compute_func=kelvin_voigt_stress,
    parameters=[
        Parameter(
            name="E",
            description="Elastic modulus (Young's modulus)",
            units="Pa",
            symbol="E",
            physiological_range=(100.0, 1e9)  # Soft tissue to bone
        ),
        Parameter(
            name="eta",
            description="Viscosity coefficient",
            units="Pa·s",
            symbol=r"\eta",
            physiological_range=(0.001, 1e6)
        ),
        Parameter(
            name="epsilon",
            description="Strain",
            units="dimensionless",
            symbol=r"\varepsilon",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="d_epsilon_dt",
            description="Strain rate",
            units="1/s",
            symbol=r"\frac{d\varepsilon}{dt}",
            physiological_range=(-100.0, 100.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.3",
        textbook_equation_number="A.37"
    )
)
register_equation(kelvin_voigt_eq)


# Create and register Maxwell equation
maxwell_eq = create_equation(
    id="foundations.biophysics.maxwell_relaxation",
    name="Maxwell Stress Relaxation",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\sigma(t) = E\varepsilon_0 e^{-Et/\eta}",
    simplified="σ(t) = E×ε₀×e^(-Et/η)",
    description="Stress relaxation in series spring-dashpot viscoelastic model",
    compute_func=maxwell_stress_relaxation,
    parameters=[
        Parameter(
            name="E",
            description="Elastic modulus",
            units="Pa",
            symbol="E",
            physiological_range=(100.0, 1e9)
        ),
        Parameter(
            name="epsilon_0",
            description="Initial strain",
            units="dimensionless",
            symbol=r"\varepsilon_0",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="eta",
            description="Viscosity coefficient",
            units="Pa·s",
            symbol=r"\eta",
            physiological_range=(0.001, 1e6)
        ),
        Parameter(
            name="t",
            description="Time",
            units="s",
            symbol="t",
            physiological_range=(0.0, 1e4)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.3",
        textbook_equation_number="A.38"
    )
)
register_equation(maxwell_eq)
