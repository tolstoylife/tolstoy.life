#!/usr/bin/env python3
"""
Constraint Validation Framework

Validates constraints against:
- Deontic consistency (no O(φ) ∧ F(φ))
- Hohfeldian correlative balance
- KROG theorem compliance
- Ontolog integration requirements
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List, Dict, Set, Callable, Any
from abc import ABC, abstractmethod


# ============================================================================
# Core Types
# ============================================================================

class DeonticModality(Enum):
    """Deontic operators from SDL."""
    PERMITTED = auto()    # P(φ)
    OBLIGATED = auto()    # O(φ)  
    FORBIDDEN = auto()    # F(φ)
    IMPOSSIBLE = auto()   # I(φ)
    UNKNOWN = auto()      # ?


class ConstraintType(Enum):
    """Juarrero's trichotomy."""
    ENABLING = auto()     # Expands possibilities
    GOVERNING = auto()    # Channels existing possibilities
    CONSTITUTIVE = auto() # Defines identity


class HohfeldianPosition(Enum):
    """Eight fundamental jural positions."""
    # First-order (conduct)
    CLAIM = auto()
    DUTY = auto()
    PRIVILEGE = auto()
    NO_RIGHT = auto()
    # Second-order (normative change)
    POWER = auto()
    LIABILITY = auto()
    IMMUNITY = auto()
    DISABILITY = auto()


class Rigidity(Enum):
    """Constraint mutability levels."""
    CONSTITUTIONAL = auto()  # Never changes
    STATIC = auto()          # Governance-only changes
    DYNAMIC = auto()         # Power-holder changes
    CONTEXTUAL = auto()      # Situational changes


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Agent:
    """Entity subject to constraints."""
    id: str
    roles: Set[str] = field(default_factory=set)
    scope: Optional[str] = None


@dataclass
class Action:
    """Action or state being constrained."""
    id: str
    description: str
    domain: Set[str] = field(default_factory=set)


@dataclass
class Context:
    """Structural context (simplicial complex Σ)."""
    id: str
    elements: Set[str] = field(default_factory=set)
    relationships: Dict[str, Set[str]] = field(default_factory=dict)


@dataclass
class Constraint:
    """Formal constraint definition."""
    id: str
    constraint_type: ConstraintType
    modality: DeonticModality
    domain: Set[str]                      # Agents/roles this applies to
    action: str                           # Action being constrained
    scope: Optional[str] = None           # Holon/jurisdiction scope
    correlative_id: Optional[str] = None  # Linked Hohfeldian correlative
    rigidity: Rigidity = Rigidity.DYNAMIC
    hohfeldian: Optional[HohfeldianPosition] = None
    temporal: Optional[str] = None        # Temporal formula
    
    def to_lambda(self) -> str:
        """Convert to ontolog λ-expression."""
        return f"λσ.λa.{self.modality.name}({self.action})"


@dataclass
class ValidationResult:
    """Result of constraint validation."""
    valid: bool
    constraint_id: str
    checks_passed: List[str] = field(default_factory=list)
    checks_failed: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def add_passed(self, check: str) -> None:
        self.checks_passed.append(check)
    
    def add_failed(self, check: str) -> None:
        self.checks_failed.append(check)
        self.valid = False
    
    def add_warning(self, warning: str) -> None:
        self.warnings.append(warning)


# ============================================================================
# Correlative Mappings
# ============================================================================

CORRELATIVES: Dict[HohfeldianPosition, HohfeldianPosition] = {
    HohfeldianPosition.CLAIM: HohfeldianPosition.DUTY,
    HohfeldianPosition.DUTY: HohfeldianPosition.CLAIM,
    HohfeldianPosition.PRIVILEGE: HohfeldianPosition.NO_RIGHT,
    HohfeldianPosition.NO_RIGHT: HohfeldianPosition.PRIVILEGE,
    HohfeldianPosition.POWER: HohfeldianPosition.LIABILITY,
    HohfeldianPosition.LIABILITY: HohfeldianPosition.POWER,
    HohfeldianPosition.IMMUNITY: HohfeldianPosition.DISABILITY,
    HohfeldianPosition.DISABILITY: HohfeldianPosition.IMMUNITY,
}

OPPOSITES: Dict[HohfeldianPosition, HohfeldianPosition] = {
    HohfeldianPosition.CLAIM: HohfeldianPosition.NO_RIGHT,
    HohfeldianPosition.NO_RIGHT: HohfeldianPosition.CLAIM,
    HohfeldianPosition.DUTY: HohfeldianPosition.PRIVILEGE,
    HohfeldianPosition.PRIVILEGE: HohfeldianPosition.DUTY,
    HohfeldianPosition.POWER: HohfeldianPosition.DISABILITY,
    HohfeldianPosition.DISABILITY: HohfeldianPosition.POWER,
    HohfeldianPosition.LIABILITY: HohfeldianPosition.IMMUNITY,
    HohfeldianPosition.IMMUNITY: HohfeldianPosition.LIABILITY,
}

# Mapping Hohfeldian positions to constraint types
POSITION_TO_TYPE: Dict[HohfeldianPosition, ConstraintType] = {
    HohfeldianPosition.CLAIM: ConstraintType.GOVERNING,
    HohfeldianPosition.DUTY: ConstraintType.GOVERNING,
    HohfeldianPosition.PRIVILEGE: ConstraintType.ENABLING,
    HohfeldianPosition.NO_RIGHT: ConstraintType.ENABLING,
    HohfeldianPosition.POWER: ConstraintType.ENABLING,
    HohfeldianPosition.LIABILITY: ConstraintType.GOVERNING,
    HohfeldianPosition.IMMUNITY: ConstraintType.CONSTITUTIVE,
    HohfeldianPosition.DISABILITY: ConstraintType.CONSTITUTIVE,
}


# ============================================================================
# Validation Engine
# ============================================================================

class ConstraintValidator:
    """Validates constraint sets for consistency."""
    
    def __init__(self, constraints: List[Constraint]):
        self.constraints = {c.id: c for c in constraints}
        self.by_action: Dict[str, List[Constraint]] = {}
        self._index_constraints()
    
    def _index_constraints(self) -> None:
        """Build indices for efficient lookup."""
        for c in self.constraints.values():
            if c.action not in self.by_action:
                self.by_action[c.action] = []
            self.by_action[c.action].append(c)
    
    def validate_all(self) -> List[ValidationResult]:
        """Validate all constraints."""
        results = []
        for c in self.constraints.values():
            results.append(self.validate(c))
        return results
    
    def validate(self, constraint: Constraint) -> ValidationResult:
        """Validate a single constraint."""
        result = ValidationResult(valid=True, constraint_id=constraint.id)
        
        # 1. Deontic consistency check
        self._check_deontic_consistency(constraint, result)
        
        # 2. Hohfeldian correlative check
        self._check_correlative_balance(constraint, result)
        
        # 3. Type-position alignment check
        self._check_type_alignment(constraint, result)
        
        # 4. KROG theorem check
        self._check_krog_compliance(constraint, result)
        
        # 5. Rigidity check
        self._check_rigidity_consistency(constraint, result)
        
        return result
    
    def _check_deontic_consistency(
        self, constraint: Constraint, result: ValidationResult
    ) -> None:
        """Check for deontic contradictions."""
        action_constraints = self.by_action.get(constraint.action, [])
        
        for other in action_constraints:
            if other.id == constraint.id:
                continue
            
            # Check O(φ) ∧ F(φ) contradiction
            if (constraint.modality == DeonticModality.OBLIGATED and
                other.modality == DeonticModality.FORBIDDEN):
                if self._scopes_overlap(constraint, other):
                    result.add_failed(
                        f"Deontic contradiction: {constraint.id} OBLIGATES "
                        f"while {other.id} FORBIDS same action"
                    )
                    return
            
            # Check P(φ) ∧ I(φ) contradiction
            if (constraint.modality == DeonticModality.PERMITTED and
                other.modality == DeonticModality.IMPOSSIBLE):
                if self._scopes_overlap(constraint, other):
                    result.add_failed(
                        f"Deontic contradiction: {constraint.id} PERMITS "
                        f"while {other.id} makes IMPOSSIBLE same action"
                    )
                    return
        
        result.add_passed("Deontic consistency")
    
    def _check_correlative_balance(
        self, constraint: Constraint, result: ValidationResult
    ) -> None:
        """Check that Hohfeldian correlatives are paired."""
        if constraint.hohfeldian is None:
            result.add_warning("No Hohfeldian position specified")
            return
        
        if constraint.correlative_id is None:
            result.add_warning(
                f"No correlative specified for {constraint.hohfeldian.name}"
            )
            return
        
        correlative = self.constraints.get(constraint.correlative_id)
        if correlative is None:
            result.add_failed(
                f"Missing correlative constraint: {constraint.correlative_id}"
            )
            return
        
        expected_position = CORRELATIVES[constraint.hohfeldian]
        if correlative.hohfeldian != expected_position:
            result.add_failed(
                f"Correlative mismatch: {constraint.hohfeldian.name} expects "
                f"{expected_position.name}, got {correlative.hohfeldian.name if correlative.hohfeldian else 'None'}"
            )
            return
        
        result.add_passed("Hohfeldian correlative balance")
    
    def _check_type_alignment(
        self, constraint: Constraint, result: ValidationResult
    ) -> None:
        """Check constraint type aligns with Hohfeldian position."""
        if constraint.hohfeldian is None:
            return
        
        expected_type = POSITION_TO_TYPE[constraint.hohfeldian]
        if constraint.constraint_type != expected_type:
            result.add_warning(
                f"Type-position mismatch: {constraint.hohfeldian.name} "
                f"typically implies {expected_type.name}, got {constraint.constraint_type.name}"
            )
        else:
            result.add_passed("Type-position alignment")
    
    def _check_krog_compliance(
        self, constraint: Constraint, result: ValidationResult
    ) -> None:
        """Check KROG theorem: K ∧ R ∧ O ⊆ G."""
        # K: Knowledge - constraint must be queryable
        if not constraint.id:
            result.add_failed("KROG K-violation: Constraint not identifiable")
            return
        
        # R: Rights - must have valid Hohfeldian structure
        # (Already checked in correlative balance)
        
        # O: Obligations - must have defined modality
        if constraint.modality == DeonticModality.UNKNOWN:
            result.add_failed("KROG O-violation: Undefined modality")
            return
        
        # G: Governance - constitutional constraints cannot be modified
        if (constraint.rigidity == Rigidity.CONSTITUTIONAL and
            constraint.constraint_type != ConstraintType.CONSTITUTIVE):
            result.add_warning(
                "Constitutional rigidity typically pairs with constitutive type"
            )
        
        result.add_passed("KROG compliance")
    
    def _check_rigidity_consistency(
        self, constraint: Constraint, result: ValidationResult
    ) -> None:
        """Check rigidity is consistent with constraint type."""
        if (constraint.constraint_type == ConstraintType.CONSTITUTIVE and
            constraint.rigidity == Rigidity.CONTEXTUAL):
            result.add_warning(
                "Constitutive constraints rarely have contextual rigidity"
            )
        
        if (constraint.constraint_type == ConstraintType.ENABLING and
            constraint.rigidity == Rigidity.CONSTITUTIONAL):
            result.add_warning(
                "Enabling constraints rarely have constitutional rigidity"
            )
        
        result.add_passed("Rigidity consistency")
    
    def _scopes_overlap(self, c1: Constraint, c2: Constraint) -> bool:
        """Check if two constraints have overlapping scopes."""
        # If either has no scope, assume universal
        if c1.scope is None or c2.scope is None:
            return bool(c1.domain & c2.domain)
        
        # Check scope hierarchy
        return c1.scope == c2.scope or c1.domain & c2.domain


# ============================================================================
# Utility Functions
# ============================================================================

def get_correlative(position: HohfeldianPosition) -> HohfeldianPosition:
    """Get the correlative of a Hohfeldian position."""
    return CORRELATIVES[position]


def get_opposite(position: HohfeldianPosition) -> HohfeldianPosition:
    """Get the opposite of a Hohfeldian position."""
    return OPPOSITES[position]


def deontic_entails(d1: DeonticModality, d2: DeonticModality) -> bool:
    """Check if d1 entails d2 (d1 → d2)."""
    # O(φ) → P(φ)  (Ought implies may)
    if d1 == DeonticModality.OBLIGATED and d2 == DeonticModality.PERMITTED:
        return True
    # I(φ) → F(φ)  (Impossible implies forbidden)
    if d1 == DeonticModality.IMPOSSIBLE and d2 == DeonticModality.FORBIDDEN:
        return True
    return d1 == d2


def constraint_type_for_position(position: HohfeldianPosition) -> ConstraintType:
    """Get typical constraint type for Hohfeldian position."""
    return POSITION_TO_TYPE[position]


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Example: Employment relationship
    constraints = [
        Constraint(
            id="employer_hire_power",
            constraint_type=ConstraintType.ENABLING,
            modality=DeonticModality.PERMITTED,
            domain={"Manager"},
            action="hire",
            scope="department",
            correlative_id="employee_hire_liability",
            rigidity=Rigidity.DYNAMIC,
            hohfeldian=HohfeldianPosition.POWER,
        ),
        Constraint(
            id="employee_hire_liability",
            constraint_type=ConstraintType.GOVERNING,
            modality=DeonticModality.PERMITTED,
            domain={"Employee"},
            action="hire",
            scope="department",
            correlative_id="employer_hire_power",
            rigidity=Rigidity.DYNAMIC,
            hohfeldian=HohfeldianPosition.LIABILITY,
        ),
        Constraint(
            id="employee_work_duty",
            constraint_type=ConstraintType.GOVERNING,
            modality=DeonticModality.OBLIGATED,
            domain={"Employee"},
            action="perform_work",
            scope="contract",
            correlative_id="employer_work_claim",
            rigidity=Rigidity.STATIC,
            hohfeldian=HohfeldianPosition.DUTY,
        ),
        Constraint(
            id="employer_work_claim",
            constraint_type=ConstraintType.GOVERNING,
            modality=DeonticModality.PERMITTED,
            domain={"Employer"},
            action="perform_work",
            scope="contract",
            correlative_id="employee_work_duty",
            rigidity=Rigidity.STATIC,
            hohfeldian=HohfeldianPosition.CLAIM,
        ),
    ]
    
    validator = ConstraintValidator(constraints)
    results = validator.validate_all()
    
    print("=" * 60)
    print("CONSTRAINT VALIDATION RESULTS")
    print("=" * 60)
    
    for result in results:
        status = "✓ VALID" if result.valid else "✗ INVALID"
        print(f"\n{result.constraint_id}: {status}")
        
        if result.checks_passed:
            print("  Passed:")
            for check in result.checks_passed:
                print(f"    + {check}")
        
        if result.checks_failed:
            print("  Failed:")
            for check in result.checks_failed:
                print(f"    - {check}")
        
        if result.warnings:
            print("  Warnings:")
            for warning in result.warnings:
                print(f"    ! {warning}")
