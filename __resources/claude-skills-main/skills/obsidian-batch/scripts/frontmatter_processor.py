#!/usr/bin/env python3
"""
Frontmatter Processor
Process YAML frontmatter in Obsidian vault files.

Supports:
- Add/update/remove frontmatter fields
- Validate frontmatter structure
- Batch update metadata
- Template-based frontmatter generation
"""

import re
import json
import yaml
from pathlib import Path
from typing import List, Dict, Set, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

from batch_processor import BatchProcessor, ProcessingResult

logger = logging.getLogger(__name__)


@dataclass
class FrontmatterField:
    """Represents a frontmatter field."""
    key: str
    value: Any
    source_file: str
    valid: bool = True
    validation_error: Optional[str] = None


class FrontmatterProcessor(BatchProcessor):
    """Process YAML frontmatter in Obsidian vault."""

    FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL | re.MULTILINE)

    def __init__(self, vault_path: Path, dry_run: bool = False, verbose: bool = False):
        super().__init__(vault_path, dry_run, verbose)
        self.validators: Dict[str, Callable] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}

    def register_validator(self, key: str, validator: Callable[[Any], bool]) -> None:
        """Register a validation function for a frontmatter key."""
        self.validators[key] = validator

    def register_template(self, name: str, template: Dict[str, Any]) -> None:
        """Register a frontmatter template."""
        self.templates[name] = template

    def extract_frontmatter(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract frontmatter from content."""
        match = self.FRONTMATTER_PATTERN.match(content)
        if not match:
            return None

        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            return None

    def has_frontmatter(self, content: str) -> bool:
        """Check if content has frontmatter."""
        return self.FRONTMATTER_PATTERN.match(content) is not None

    def create_frontmatter(self, data: Dict[str, Any]) -> str:
        """Create frontmatter string from dictionary."""
        yaml_str = yaml.dump(
            data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=float('inf')  # Prevent line wrapping
        )
        return f"---\n{yaml_str}---\n"

    def add_frontmatter(self, content: str, data: Dict[str, Any]) -> str:
        """Add frontmatter to content that doesn't have it."""
        if self.has_frontmatter(content):
            # Update existing frontmatter
            return self.update_frontmatter(content, data)

        # Add new frontmatter at the beginning
        frontmatter = self.create_frontmatter(data)
        return frontmatter + content

    def update_frontmatter(self, content: str, updates: Dict[str, Any]) -> str:
        """Update existing frontmatter."""
        match = self.FRONTMATTER_PATTERN.match(content)
        if not match:
            # No frontmatter, add it
            return self.add_frontmatter(content, updates)

        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
            frontmatter.update(updates)

            # Reconstruct content
            new_fm = self.create_frontmatter(frontmatter)
            body = content[match.end():]
            return new_fm + body

        except yaml.YAMLError as e:
            self.errors.append(f"YAML error during update: {e}")
            return content

    def remove_frontmatter_key(self, content: str, key: str) -> str:
        """Remove a key from frontmatter."""
        match = self.FRONTMATTER_PATTERN.match(content)
        if not match:
            return content

        try:
            frontmatter = yaml.safe_load(match.group(1))
            if not frontmatter:
                return content

            if key in frontmatter:
                del frontmatter[key]

                # If frontmatter is now empty, remove it entirely
                if not frontmatter:
                    return content[match.end():]

                # Reconstruct content
                new_fm = self.create_frontmatter(frontmatter)
                body = content[match.end():]
                return new_fm + body

            return content

        except yaml.YAMLError as e:
            self.errors.append(f"YAML error during removal: {e}")
            return content

    def validate_frontmatter(self, frontmatter: Dict[str, Any], file_path: Path) -> List[str]:
        """
        Validate frontmatter against registered validators.

        Returns:
            List of validation errors
        """
        errors = []

        for key, value in frontmatter.items():
            if key in self.validators:
                try:
                    if not self.validators[key](value):
                        errors.append(f"Validation failed for '{key}' in {file_path}")
                except Exception as e:
                    errors.append(f"Validator error for '{key}' in {file_path}: {e}")

        return errors

    def apply_template(self, content: str, template_name: str, overwrite: bool = False) -> str:
        """Apply a frontmatter template to content."""
        if template_name not in self.templates:
            self.errors.append(f"Template '{template_name}' not found")
            return content

        template = self.templates[template_name].copy()

        # Add dynamic fields
        template.setdefault('created', datetime.now().isoformat())
        template.setdefault('modified', datetime.now().isoformat())

        if overwrite or not self.has_frontmatter(content):
            return self.add_frontmatter(content, template)
        else:
            # Merge with existing frontmatter
            return self.update_frontmatter(content, template)

    def process_file(
        self,
        file_path: Path,
        operation: str,
        key: Optional[str] = None,
        value: Optional[Any] = None,
        template_name: Optional[str] = None
    ) -> bool:
        """
        Process frontmatter in a single file.

        Args:
            file_path: Path to file
            operation: 'add', 'remove', 'update', 'validate', 'template'
            key: Frontmatter key (for add/remove/update)
            value: Value to set (for add/update)
            template_name: Template name (for template operation)

        Returns:
            True if file was modified
        """
        content = self.read_file(file_path)
        if content is None:
            return False

        modified = False
        new_content = content

        if operation == 'add':
            if not key:
                self.errors.append(f"Key required for 'add' operation")
                return False

            # Parse value as JSON if it looks like JSON
            if isinstance(value, str):
                try:
                    if value.startswith('[') or value.startswith('{'):
                        value = json.loads(value)
                except json.JSONDecodeError:
                    pass

            new_content = self.add_frontmatter(content, {key: value})
            modified = new_content != content

        elif operation == 'remove':
            if not key:
                self.errors.append(f"Key required for 'remove' operation")
                return False

            new_content = self.remove_frontmatter_key(content, key)
            modified = new_content != content

        elif operation == 'update':
            if not key:
                self.errors.append(f"Key required for 'update' operation")
                return False

            # Parse value as JSON if it looks like JSON
            if isinstance(value, str):
                try:
                    if value.startswith('[') or value.startswith('{'):
                        value = json.loads(value)
                except json.JSONDecodeError:
                    pass

            new_content = self.update_frontmatter(content, {key: value})
            modified = new_content != content

        elif operation == 'validate':
            frontmatter = self.extract_frontmatter(content)
            if frontmatter:
                validation_errors = self.validate_frontmatter(frontmatter, file_path)
                if validation_errors:
                    self.errors.extend(validation_errors)
            return False  # Validation doesn't modify files

        elif operation == 'template':
            if not template_name:
                self.errors.append(f"Template name required for 'template' operation")
                return False

            new_content = self.apply_template(content, template_name)
            modified = new_content != content

        else:
            self.errors.append(f"Unknown operation: {operation}")
            return False

        if modified:
            if self.write_file(file_path, new_content):
                return True

        return False

    def setup_default_validators(self):
        """Setup default validators for common frontmatter fields."""
        # Date validator
        def validate_date(value):
            if isinstance(value, str):
                try:
                    datetime.fromisoformat(value)
                    return True
                except ValueError:
                    return False
            return False

        # List validator
        def validate_list(value):
            return isinstance(value, list)

        # String validator
        def validate_string(value):
            return isinstance(value, str)

        # Boolean validator
        def validate_boolean(value):
            return isinstance(value, bool)

        self.register_validator('created', validate_date)
        self.register_validator('modified', validate_date)
        self.register_validator('tags', validate_list)
        self.register_validator('aliases', validate_list)
        self.register_validator('published', validate_boolean)

    def setup_default_templates(self):
        """Setup default frontmatter templates."""
        self.register_template('basic', {
            'created': datetime.now().isoformat(),
            'tags': [],
            'aliases': []
        })

        self.register_template('article', {
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat(),
            'tags': [],
            'aliases': [],
            'author': '',
            'published': False,
            'draft': True
        })

        self.register_template('meeting', {
            'created': datetime.now().isoformat(),
            'tags': ['meeting'],
            'attendees': [],
            'date': datetime.now().date().isoformat(),
            'location': ''
        })

    def process(
        self,
        operation: str,
        key: Optional[str] = None,
        value: Optional[Any] = None,
        template_name: Optional[str] = None
    ) -> ProcessingResult:
        """
        Process frontmatter across the vault.

        Args:
            operation: 'add', 'remove', 'update', 'validate', 'template'
            key: Frontmatter key (for add/remove/update)
            value: Value to set (for add/update)
            template_name: Template name (for template operation)

        Returns:
            ProcessingResult with processing results
        """
        logger.info(f"Processing frontmatter in vault: {self.vault_path}")
        logger.info(f"Operation: {operation}")

        # Setup defaults
        self.setup_default_validators()
        self.setup_default_templates()

        # Find all markdown files
        md_files = self.find_markdown_files()
        files_processed = 0
        files_modified = 0

        # Process each file
        for file_path in md_files:
            if self.verbose:
                logger.info(f"Processing {file_path.relative_to(self.vault_path)}")

            if self.process_file(
                file_path,
                operation,
                key=key,
                value=value,
                template_name=template_name
            ):
                files_modified += 1

            files_processed += 1

        logger.info(f"Processed {files_processed} files, modified {files_modified}")

        return ProcessingResult(
            success=True,
            files_processed=files_processed,
            files_modified=files_modified,
            errors=self.errors,
            warnings=self.warnings,
            metadata={
                'operation': operation,
                'key': key,
                'template': template_name
            }
        )


def main():
    """Standalone execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Process frontmatter in Obsidian vault')
    parser.add_argument('--vault', type=Path, required=True, help='Vault path')
    parser.add_argument('--operation', required=True,
                       choices=['add', 'remove', 'update', 'validate', 'template'],
                       help='Frontmatter operation')
    parser.add_argument('--key', help='Frontmatter key')
    parser.add_argument('--value', help='Value to set')
    parser.add_argument('--template', help='Template name')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    processor = FrontmatterProcessor(
        args.vault,
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    result = processor.process(
        operation=args.operation,
        key=args.key,
        value=args.value,
        template_name=args.template
    )

    print(json.dumps(asdict(result), indent=2))


if __name__ == '__main__':
    main()
