#!/usr/bin/env python3
"""
Workflow Pattern Validator for Knowledge Orchestrator

Validates custom workflow pattern definitions against schema requirements.
Ensures workflow patterns are well-formed before deployment.

Usage:
    python validate_workflow.py my_workflow.yaml
    python validate_workflow.py --directory custom_patterns/
"""

import argparse
import yaml
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of workflow validation"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    workflow_name: Optional[str] = None


class WorkflowValidator:
    """Validates workflow pattern definitions"""

    REQUIRED_FIELDS = ["description", "trigger_conditions", "sequence"]
    REQUIRED_STEP_FIELDS = ["skill", "purpose", "input", "output_binding"]
    VALID_SKILLS = ["obsidian-markdown", "hierarchical-reasoning", "knowledge-graph"]

    def validate_file(self, file_path: str) -> ValidationResult:
        """Validate a single workflow pattern file"""
        errors = []
        warnings = []

        # Check file exists
        if not os.path.exists(file_path):
            return ValidationResult(
                valid=False,
                errors=[f"File not found: {file_path}"],
                warnings=[]
            )

        # Check file extension
        if not file_path.endswith(('.yaml', '.yml')):
            warnings.append(f"File extension should be .yaml or .yml")

        # Load YAML
        try:
            with open(file_path, 'r') as f:
                workflow = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return ValidationResult(
                valid=False,
                errors=[f"Invalid YAML: {str(e)}"],
                warnings=warnings
            )

        # Validate structure
        if not isinstance(workflow, dict):
            errors.append("Workflow must be a dictionary at root level")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        # Get workflow name (should be single top-level key)
        if len(workflow) != 1:
            errors.append("Workflow file should have exactly one top-level key (the workflow name)")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        workflow_name = list(workflow.keys())[0]
        workflow_def = workflow[workflow_name]

        # Validate required fields
        for field in self.REQUIRED_FIELDS:
            if field not in workflow_def:
                errors.append(f"Missing required field: {field}")

        if errors:
            return ValidationResult(
                valid=False,
                errors=errors,
                warnings=warnings,
                workflow_name=workflow_name
            )

        # Validate description
        if not isinstance(workflow_def["description"], str):
            errors.append("Description must be a string")
        elif len(workflow_def["description"]) < 10:
            warnings.append("Description is very short - consider adding more detail")

        # Validate trigger conditions
        self._validate_trigger_conditions(workflow_def["trigger_conditions"], errors, warnings)

        # Validate sequence
        self._validate_sequence(workflow_def["sequence"], errors, warnings)

        # Validate optional final_output field
        if "final_output" in workflow_def:
            if not isinstance(workflow_def["final_output"], str):
                errors.append("final_output must be a string (output binding name)")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            workflow_name=workflow_name
        )

    def _validate_trigger_conditions(self, conditions: Any, errors: List[str], warnings: List[str]):
        """Validate trigger conditions structure"""
        if not isinstance(conditions, list):
            errors.append("trigger_conditions must be a list")
            return

        if len(conditions) == 0:
            warnings.append("No trigger conditions defined - workflow may be hard to activate")

        for i, condition in enumerate(conditions):
            if not isinstance(condition, dict):
                errors.append(f"Trigger condition {i+1} must be a dictionary")
                continue

            # Each condition should have one key-value pair
            if len(condition) != 1:
                warnings.append(f"Trigger condition {i+1} has multiple keys - consider splitting")

    def _validate_sequence(self, sequence: Any, errors: List[str], warnings: List[str]):
        """Validate workflow sequence structure"""
        if not isinstance(sequence, list):
            errors.append("sequence must be a list")
            return

        if len(sequence) < 2:
            warnings.append("Sequence has fewer than 2 steps - consider if workflow is necessary")

        output_bindings = set()

        for i, step in enumerate(sequence):
            step_num = i + 1

            if not isinstance(step, dict):
                errors.append(f"Step {step_num} must be a dictionary")
                continue

            # Validate required step fields
            for field in self.REQUIRED_STEP_FIELDS:
                if field not in step:
                    errors.append(f"Step {step_num} missing required field: {field}")

            # Validate skill name
            if "skill" in step:
                if step["skill"] not in self.VALID_SKILLS:
                    errors.append(f"Step {step_num}: Unknown skill '{step['skill']}'. Valid skills: {', '.join(self.VALID_SKILLS)}")

            # Validate purpose
            if "purpose" in step:
                if not isinstance(step["purpose"], str):
                    errors.append(f"Step {step_num}: purpose must be a string")
                elif len(step["purpose"]) < 5:
                    warnings.append(f"Step {step_num}: purpose is very short")

            # Validate input
            if "input" in step:
                if isinstance(step["input"], str):
                    # String input - could be literal or binding reference
                    if "." not in step["input"] and step["input"] != "user_request":
                        if step_num > 1:
                            warnings.append(f"Step {step_num}: input doesn't reference previous output binding")
                elif isinstance(step["input"], dict):
                    # Dict input - validate structure
                    pass  # Complex inputs are OK
                else:
                    errors.append(f"Step {step_num}: input must be string or dict")

            # Validate output_binding
            if "output_binding" in step:
                if not isinstance(step["output_binding"], str):
                    errors.append(f"Step {step_num}: output_binding must be a string")
                else:
                    # Check for duplicate output bindings
                    if step["output_binding"] in output_bindings:
                        warnings.append(f"Step {step_num}: output_binding '{step['output_binding']}' already used")
                    output_bindings.add(step["output_binding"])

            # Validate parameters if present
            if "parameters" in step:
                if not isinstance(step["parameters"], dict):
                    errors.append(f"Step {step_num}: parameters must be a dictionary")

    def validate_directory(self, directory_path: str) -> Dict[str, ValidationResult]:
        """Validate all workflow files in a directory"""
        results = {}

        if not os.path.isdir(directory_path):
            print(f"Error: Directory not found: {directory_path}")
            return results

        for filename in os.listdir(directory_path):
            if filename.endswith(('.yaml', '.yml')):
                file_path = os.path.join(directory_path, filename)
                results[filename] = self.validate_file(file_path)

        return results


def main():
    """CLI interface for workflow validation"""
    parser = argparse.ArgumentParser(
        description="Validate custom workflow pattern definitions"
    )
    parser.add_argument(
        "path",
        help="Path to workflow YAML file or directory"
    )
    parser.add_argument(
        "--directory", "-d",
        action="store_true",
        help="Validate all workflow files in directory"
    )

    args = parser.parse_args()

    validator = WorkflowValidator()

    if args.directory or os.path.isdir(args.path):
        # Validate directory
        results = validator.validate_directory(args.path)

        if not results:
            print("No workflow files found in directory")
            return

        print(f"\n{'='*80}")
        print(f"WORKFLOW VALIDATION RESULTS - Directory: {args.path}")
        print(f"{'='*80}\n")

        total_valid = 0
        total_invalid = 0

        for filename, result in results.items():
            print(f"File: {filename}")
            if result.workflow_name:
                print(f"Workflow: {result.workflow_name}")

            if result.valid:
                print(f"  ✅ VALID")
                total_valid += 1
            else:
                print(f"  ❌ INVALID")
                total_invalid += 1

            if result.errors:
                print(f"\n  Errors:")
                for error in result.errors:
                    print(f"    - {error}")

            if result.warnings:
                print(f"\n  Warnings:")
                for warning in result.warnings:
                    print(f"    - {warning}")

            print()

        print(f"{'='*80}")
        print(f"Summary: {total_valid} valid, {total_invalid} invalid")
        print(f"{'='*80}\n")

    else:
        # Validate single file
        result = validator.validate_file(args.path)

        print(f"\n{'='*80}")
        print(f"WORKFLOW VALIDATION - File: {os.path.basename(args.path)}")
        if result.workflow_name:
            print(f"Workflow Name: {result.workflow_name}")
        print(f"{'='*80}\n")

        if result.valid:
            print("✅ VALID WORKFLOW")
        else:
            print("❌ INVALID WORKFLOW")

        if result.errors:
            print(f"\nErrors ({len(result.errors)}):")
            for error in result.errors:
                print(f"  - {error}")

        if result.warnings:
            print(f"\nWarnings ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"  - {warning}")

        print()

        exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
