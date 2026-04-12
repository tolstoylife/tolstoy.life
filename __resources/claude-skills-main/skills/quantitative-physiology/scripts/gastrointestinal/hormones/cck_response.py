"""CCK release in response to fat and amino acids."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_cck_response(fat_g: float, aa_g: float, EC50_fat: float = 5.0, EC50_aa: float = 10.0) -> float:
    """
    Calculate CCK release based on fat and amino acid content.

    CCK released by I cells (duodenum) stimulates:
    - Enzyme secretion (pancreas)
    - Gallbladder contraction
    - Satiety

    Parameters
    ----------
    fat_g : float
        Fat content in duodenum (g)
    aa_g : float
        Amino acid content in duodenum (g)
    EC50_fat : float
        Half-maximal fat concentration (g), default 5.0
    EC50_aa : float
        Half-maximal amino acid concentration (g), default 10.0

    Returns
    -------
    float
        CCK response signal (dimensionless, 0-2 range)
    """
    fat_signal = fat_g / (EC50_fat + fat_g)
    aa_signal = aa_g / (EC50_aa + aa_g)
    return fat_signal + aa_signal


cck_response = create_equation(
    id="gastrointestinal.hormones.cck_response",
    name="CCK Response to Fat and Amino Acids",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{CCK} = \frac{[\text{Fat}]}{EC_{50,\text{fat}} + [\text{Fat}]} + \frac{[\text{AA}]}{EC_{50,\text{AA}} + [\text{AA}]}",
    simplified="CCK = [Fat]/(EC50_fat + [Fat]) + [AA]/(EC50_AA + [AA])",
    description="CCK release by I cells in response to fat and amino acids. Stimulates enzyme secretion, gallbladder contraction, satiety",
    compute_func=compute_cck_response,
    parameters=[
        Parameter(
            name="fat_g",
            description="Fat content in duodenum",
            units="g",
            symbol=r"[\text{Fat}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="aa_g",
            description="Amino acid content in duodenum",
            units="g",
            symbol=r"[\text{AA}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="EC50_fat",
            description="Half-maximal fat concentration",
            units="g",
            symbol=r"EC_{50,\text{fat}}",
            default_value=5.0,
            physiological_range=(3.0, 7.0)
        ),
        Parameter(
            name="EC50_aa",
            description="Half-maximal amino acid concentration",
            units="g",
            symbol=r"EC_{50,\text{AA}}",
            default_value=10.0,
            physiological_range=(8.0, 12.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(cck_response)
