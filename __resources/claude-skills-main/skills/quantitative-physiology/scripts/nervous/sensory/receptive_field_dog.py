"""
Receptive Field (Difference of Gaussians) - Center-surround organization

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_receptive_field_dog(x: float, y: float, A_c: float, sigma_c: float,
                                 A_s: float, sigma_s: float) -> float:
    """
    Calculate receptive field sensitivity using difference of Gaussians.

    Formula: RF(x,y) = A_c × e^(-(x²+y²)/(2σ_c²)) - A_s × e^(-(x²+y²)/(2σ_s²))

    Parameters:
    -----------
    x : float
        Horizontal position (deg or mm)
    y : float
        Vertical position (deg or mm)
    A_c : float
        Center amplitude
    sigma_c : float
        Center width (standard deviation)
    A_s : float
        Surround amplitude
    sigma_s : float
        Surround width (standard deviation)

    Returns:
    --------
    RF : float
        Receptive field sensitivity at position (x,y)

    Notes:
    ------
    Models center-surround organization of visual, somatosensory receptive fields.
    Typically σ_s > σ_c (surround larger than center).
    Produces Mexican-hat shaped sensitivity profile.
    Used in retinal ganglion cells, LGN, V1 simple cells.
    """
    r_squared = x**2 + y**2
    center = A_c * np.exp(-r_squared / (2 * sigma_c**2))
    surround = A_s * np.exp(-r_squared / (2 * sigma_s**2))
    return center - surround


# Create and register atomic equation
receptive_field_dog = create_equation(
    id="nervous.sensory.receptive_field_dog",
    name="Receptive Field (Difference of Gaussians)",
    category=EquationCategory.NERVOUS,
    latex=r"RF(x,y) = A_c \times e^{-\frac{x^2+y^2}{2\sigma_c^2}} - A_s \times e^{-\frac{x^2+y^2}{2\sigma_s^2}}",
    simplified="RF(x,y) = A_c × e^(-(x²+y²)/(2σ_c²)) - A_s × e^(-(x²+y²)/(2σ_s²))",
    description="Difference of Gaussians model of receptive field with center-surround antagonism. Produces Mexican-hat sensitivity profile characteristic of visual and somatosensory neurons.",
    compute_func=compute_receptive_field_dog,
    parameters=[
        Parameter(
            name="x",
            description="Horizontal position",
            units="deg or mm",
            symbol="x",
            default_value=None,
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="y",
            description="Vertical position",
            units="deg or mm",
            symbol="y",
            default_value=None,
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="A_c",
            description="Center amplitude",
            units="arbitrary",
            symbol="A_c",
            default_value=None,
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="sigma_c",
            description="Center width",
            units="deg or mm",
            symbol=r"\sigma_c",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="A_s",
            description="Surround amplitude",
            units="arbitrary",
            symbol="A_s",
            default_value=None,
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="sigma_s",
            description="Surround width",
            units="deg or mm",
            symbol=r"\sigma_s",
            default_value=None,
            physiological_range=(0.5, 20.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(receptive_field_dog)
