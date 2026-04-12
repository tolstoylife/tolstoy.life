"""
Cross-domain equation registry.

Tracks equations that are used across multiple physiological domains,
enabling symlink-based integration and minimal redundancy.

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher
"""

from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .base import EquationCategory


@dataclass
class CrossDomainEquation:
    """
    Represents an equation used in multiple domains.

    Attributes:
        id: Equation identifier
        name: Human-readable name
        primary_domain: The domain where equation is defined
        used_in_domains: List of other domains using this equation
        module_path: Import path to the defining module
        description: Brief description of cross-domain usage
    """
    id: str
    name: str
    primary_domain: EquationCategory
    used_in_domains: List[EquationCategory]
    module_path: str
    description: str = ""

    def all_domains(self) -> List[EquationCategory]:
        """Return all domains where this equation is used."""
        return [self.primary_domain] + self.used_in_domains

    def is_used_in(self, domain: EquationCategory) -> bool:
        """Check if equation is used in a specific domain."""
        return domain == self.primary_domain or domain in self.used_in_domains


class CrossDomainRegistry:
    """
    Registry for tracking cross-domain equation usage.

    Enables:
    - Identification of shared equations
    - Symlink generation for reference files
    - Import path resolution
    - Redundancy detection

    Usage:
        registry = CrossDomainRegistry()
        registry.register(CrossDomainEquation(
            id="starling_forces",
            name="Starling Forces",
            primary_domain=EquationCategory.CARDIOVASCULAR,
            used_in_domains=[EquationCategory.RENAL, EquationCategory.GASTROINTESTINAL],
            module_path="scripts.cardiovascular.microcirculation"
        ))

        # Find shared equations
        cv_renal_shared = registry.shared_between(
            EquationCategory.CARDIOVASCULAR,
            EquationCategory.RENAL
        )
    """

    def __init__(self):
        """Initialize empty registry."""
        self._equations: Dict[str, CrossDomainEquation] = {}
        self._by_primary: Dict[EquationCategory, List[str]] = {}
        self._by_usage: Dict[EquationCategory, List[str]] = {}

    def register(self, equation: CrossDomainEquation) -> None:
        """
        Register a cross-domain equation.

        Args:
            equation: CrossDomainEquation to register

        Raises:
            ValueError: If equation with same ID exists
        """
        if equation.id in self._equations:
            raise ValueError(f"Equation '{equation.id}' already registered")

        self._equations[equation.id] = equation

        # Index by primary domain
        if equation.primary_domain not in self._by_primary:
            self._by_primary[equation.primary_domain] = []
        self._by_primary[equation.primary_domain].append(equation.id)

        # Index by all usage domains
        for domain in equation.all_domains():
            if domain not in self._by_usage:
                self._by_usage[domain] = []
            if equation.id not in self._by_usage[domain]:
                self._by_usage[domain].append(equation.id)

    def get(self, eq_id: str) -> Optional[CrossDomainEquation]:
        """Get a cross-domain equation by ID."""
        return self._equations.get(eq_id)

    def defined_in(self, domain: EquationCategory) -> List[CrossDomainEquation]:
        """Get equations primarily defined in a domain."""
        return [
            self._equations[eid]
            for eid in self._by_primary.get(domain, [])
        ]

    def used_in(self, domain: EquationCategory) -> List[CrossDomainEquation]:
        """Get all equations used in a domain (including primary)."""
        return [
            self._equations[eid]
            for eid in self._by_usage.get(domain, [])
        ]

    def imported_to(self, domain: EquationCategory) -> List[CrossDomainEquation]:
        """Get equations imported to a domain (not primary)."""
        return [
            eq for eq in self.used_in(domain)
            if eq.primary_domain != domain
        ]

    def shared_between(
        self,
        domain1: EquationCategory,
        domain2: EquationCategory
    ) -> List[CrossDomainEquation]:
        """Get equations shared between two domains."""
        eqs1 = set(self._by_usage.get(domain1, []))
        eqs2 = set(self._by_usage.get(domain2, []))
        shared = eqs1 & eqs2
        return [self._equations[eid] for eid in shared]

    def get_import_path(self, eq_id: str) -> Optional[str]:
        """Get the import path for an equation."""
        eq = self._equations.get(eq_id)
        return eq.module_path if eq else None

    def generate_imports(self, domain: EquationCategory) -> List[str]:
        """
        Generate Python import statements for a domain.

        Returns imports for all equations used in the domain,
        grouped by source module.
        """
        imports = []
        by_module: Dict[str, List[str]] = {}

        for eq in self.used_in(domain):
            if eq.module_path not in by_module:
                by_module[eq.module_path] = []
            by_module[eq.module_path].append(eq.id)

        for module, eq_ids in sorted(by_module.items()):
            names = ", ".join(sorted(eq_ids))
            imports.append(f"from {module} import {names}")

        return imports

    def all_equations(self) -> List[CrossDomainEquation]:
        """Get all registered cross-domain equations."""
        return list(self._equations.values())

    def stats(self) -> Dict[str, int]:
        """Return statistics about the registry."""
        total_usages = sum(
            len(eq.used_in_domains) + 1  # +1 for primary
            for eq in self._equations.values()
        )
        return {
            "total_equations": len(self._equations),
            "total_cross_domain_usages": total_usages,
            "domains_with_shared": len(self._by_usage),
            "average_domains_per_equation": (
                total_usages / len(self._equations)
                if self._equations else 0
            )
        }


# Pre-populated registry with known cross-domain equations
# These are equations that appear in multiple physiological systems

CROSS_DOMAIN_EQUATIONS = CrossDomainRegistry()

# Foundational equations used across many domains
_FOUNDATIONAL_CROSS_DOMAIN = [
    CrossDomainEquation(
        id="fick_diffusion",
        name="Fick's First Law of Diffusion",
        primary_domain=EquationCategory.FOUNDATIONS,
        used_in_domains=[
            EquationCategory.MEMBRANE,
            EquationCategory.RESPIRATORY,
            EquationCategory.RENAL,
            EquationCategory.GASTROINTESTINAL
        ],
        module_path="scripts.foundations.transport.diffusion",
        description="Diffusive flux proportional to concentration gradient"
    ),
    CrossDomainEquation(
        id="poiseuille_flow",
        name="Poiseuille's Law",
        primary_domain=EquationCategory.FOUNDATIONS,
        used_in_domains=[
            EquationCategory.CARDIOVASCULAR,
            EquationCategory.RESPIRATORY,
            EquationCategory.RENAL
        ],
        module_path="scripts.foundations.transport.poiseuille",
        description="Laminar flow through cylindrical vessels"
    ),
    CrossDomainEquation(
        id="michaelis_menten",
        name="Michaelis-Menten Kinetics",
        primary_domain=EquationCategory.FOUNDATIONS,
        used_in_domains=[
            EquationCategory.MEMBRANE,
            EquationCategory.RENAL,
            EquationCategory.GASTROINTESTINAL,
            EquationCategory.ENDOCRINE
        ],
        module_path="scripts.foundations.kinetics.michaelis_menten",
        description="Saturation kinetics for enzyme-mediated processes"
    ),
    CrossDomainEquation(
        id="hill_equation",
        name="Hill Equation",
        primary_domain=EquationCategory.FOUNDATIONS,
        used_in_domains=[
            EquationCategory.RESPIRATORY,  # O2-Hb binding
            EquationCategory.MEMBRANE,     # Cooperative binding
            EquationCategory.ENDOCRINE     # Hormone-receptor
        ],
        module_path="scripts.foundations.kinetics.hill",
        description="Cooperative binding with Hill coefficient"
    ),
    CrossDomainEquation(
        id="henderson_hasselbalch",
        name="Henderson-Hasselbalch Equation",
        primary_domain=EquationCategory.FOUNDATIONS,
        used_in_domains=[
            EquationCategory.RESPIRATORY,
            EquationCategory.RENAL,
            EquationCategory.GASTROINTESTINAL
        ],
        module_path="scripts.foundations.thermodynamics.acid_base",
        description="pH from pKa and conjugate ratio"
    ),
    CrossDomainEquation(
        id="laplace_law",
        name="Law of Laplace",
        primary_domain=EquationCategory.FOUNDATIONS,
        used_in_domains=[
            EquationCategory.CARDIOVASCULAR,  # Cardiac wall stress
            EquationCategory.RESPIRATORY,     # Alveolar surface tension
            EquationCategory.GASTROINTESTINAL # GI wall tension
        ],
        module_path="scripts.foundations.transport.laplace",
        description="Wall tension vs pressure and radius"
    ),
]

# Membrane equations used in excitable/organ systems
_MEMBRANE_CROSS_DOMAIN = [
    CrossDomainEquation(
        id="nernst_potential",
        name="Nernst Equation",
        primary_domain=EquationCategory.MEMBRANE,
        used_in_domains=[
            EquationCategory.EXCITABLE,
            EquationCategory.NERVOUS,
            EquationCategory.CARDIOVASCULAR  # Cardiac cells
        ],
        module_path="scripts.membrane.potential.nernst",
        description="Equilibrium potential for single ion"
    ),
    CrossDomainEquation(
        id="goldman_hodgkin_katz",
        name="Goldman-Hodgkin-Katz Equation",
        primary_domain=EquationCategory.MEMBRANE,
        used_in_domains=[
            EquationCategory.EXCITABLE,
            EquationCategory.NERVOUS,
            EquationCategory.CARDIOVASCULAR
        ],
        module_path="scripts.membrane.potential.goldman",
        description="Resting membrane potential from multiple ions"
    ),
]

# Cardiovascular equations used in other organ systems
_CARDIOVASCULAR_CROSS_DOMAIN = [
    CrossDomainEquation(
        id="starling_forces",
        name="Starling Forces (Capillary Filtration)",
        primary_domain=EquationCategory.CARDIOVASCULAR,
        used_in_domains=[
            EquationCategory.RENAL,           # Glomerular filtration
            EquationCategory.GASTROINTESTINAL, # Intestinal capillaries
            EquationCategory.RESPIRATORY       # Pulmonary edema
        ],
        module_path="scripts.cardiovascular.microcirculation.starling",
        description="Net filtration from hydrostatic and oncotic pressures"
    ),
    CrossDomainEquation(
        id="fick_principle_cardiac",
        name="Fick Principle (Cardiac Output)",
        primary_domain=EquationCategory.CARDIOVASCULAR,
        used_in_domains=[
            EquationCategory.RESPIRATORY  # VO2 measurement
        ],
        module_path="scripts.cardiovascular.hemodynamics.fick_cardiac",
        description="Cardiac output from O2 consumption and A-V difference"
    ),
]

# Respiratory equations used elsewhere
_RESPIRATORY_CROSS_DOMAIN = [
    CrossDomainEquation(
        id="oxygen_content",
        name="Oxygen Content Equation",
        primary_domain=EquationCategory.RESPIRATORY,
        used_in_domains=[
            EquationCategory.CARDIOVASCULAR  # DO2 calculations
        ],
        module_path="scripts.respiratory.gas_transport.oxygen_content",
        description="Total O2 content from Hb saturation and dissolved"
    ),
    CrossDomainEquation(
        id="alveolar_gas_equation",
        name="Alveolar Gas Equation",
        primary_domain=EquationCategory.RESPIRATORY,
        used_in_domains=[
            EquationCategory.CARDIOVASCULAR  # A-a gradient
        ],
        module_path="scripts.respiratory.gas_exchange.alveolar_gas",
        description="Alveolar PO2 from inspired O2 and CO2"
    ),
]

# Register all pre-defined cross-domain equations
for eq in _FOUNDATIONAL_CROSS_DOMAIN:
    CROSS_DOMAIN_EQUATIONS.register(eq)

for eq in _MEMBRANE_CROSS_DOMAIN:
    CROSS_DOMAIN_EQUATIONS.register(eq)

for eq in _CARDIOVASCULAR_CROSS_DOMAIN:
    CROSS_DOMAIN_EQUATIONS.register(eq)

for eq in _RESPIRATORY_CROSS_DOMAIN:
    CROSS_DOMAIN_EQUATIONS.register(eq)


def get_cross_domain_registry() -> CrossDomainRegistry:
    """Get the pre-populated cross-domain registry."""
    return CROSS_DOMAIN_EQUATIONS


def find_shared_equations(
    domain1: EquationCategory,
    domain2: EquationCategory
) -> List[CrossDomainEquation]:
    """Find equations shared between two domains."""
    return CROSS_DOMAIN_EQUATIONS.shared_between(domain1, domain2)


def get_domain_imports(domain: EquationCategory) -> List[str]:
    """Get import statements for a domain's cross-domain equations."""
    return CROSS_DOMAIN_EQUATIONS.generate_imports(domain)
