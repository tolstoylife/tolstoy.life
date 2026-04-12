#!/usr/bin/env python3
"""
Test suite for LSP Integration module.

Usage:
    python test_lsp_integration.py
"""

import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from lsp_integration import (
    LSPClient,
    MarkdownOxideIntegration,
    RecursiveLSP,
    VaultLSPAnalyzer,
    LSPPosition,
    LSPRange,
    LSPLocation,
    DocumentSymbol,
    WorkspaceSymbol,
)


class TestLSPDataStructures(unittest.TestCase):
    """Test LSP data structure classes."""

    def test_lsp_position(self):
        """Test LSPPosition creation."""
        pos = LSPPosition(line=5, character=10)
        self.assertEqual(pos.line, 5)
        self.assertEqual(pos.character, 10)

    def test_lsp_range(self):
        """Test LSPRange creation."""
        start = LSPPosition(line=1, character=0)
        end = LSPPosition(line=1, character=10)
        range_obj = LSPRange(start=start, end=end)
        self.assertEqual(range_obj.start.line, 1)
        self.assertEqual(range_obj.end.character, 10)

    def test_document_symbol_kind_name(self):
        """Test DocumentSymbol kind name conversion."""
        symbol = DocumentSymbol(
            name="MyFunction",
            kind=12,  # Function
            range=LSPRange(LSPPosition(0, 0), LSPPosition(0, 10)),
            selection_range=LSPRange(LSPPosition(0, 0), LSPPosition(0, 10))
        )
        self.assertEqual(symbol.kind_name, "Function")


class TestLSPClient(unittest.TestCase):
    """Test LSPClient class."""

    def setUp(self):
        """Set up test vault."""
        self.temp_dir = TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)
        self.client = LSPClient(self.vault_path)

    def tearDown(self):
        """Clean up test vault."""
        self.temp_dir.cleanup()

    def test_client_initialization(self):
        """Test LSP client initialization."""
        self.assertTrue(self.vault_path.exists())
        self.assertEqual(self.client.vault_path, self.vault_path.resolve())

    def test_file_to_uri_conversion(self):
        """Test file path to URI conversion."""
        test_file = self.vault_path / "test.md"
        uri = self.client._file_to_uri(test_file)
        self.assertTrue(uri.startswith('file://'))
        self.assertTrue(str(test_file.resolve()) in uri)

    def test_uri_to_file_conversion(self):
        """Test URI to file path conversion."""
        test_path = Path("/tmp/test.md")
        uri = f"file://{test_path}"
        file_path = self.client._uri_to_file(uri)
        self.assertEqual(file_path, test_path)

    def test_invalid_vault_path(self):
        """Test client initialization with invalid vault path."""
        with self.assertRaises(ValueError):
            LSPClient(Path("/nonexistent/path"))


class TestMarkdownOxideIntegration(unittest.TestCase):
    """Test MarkdownOxideIntegration class."""

    def setUp(self):
        """Set up test vault with sample files."""
        self.temp_dir = TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)

        # Create sample markdown files
        self.test_file1 = self.vault_path / "note1.md"
        self.test_file1.write_text("""# Note 1

This is a test note with a [[note2|link to note 2]].

## Section 1
Content here.
""")

        self.test_file2 = self.vault_path / "note2.md"
        self.test_file2.write_text("""# Note 2

This links back to [[note1]].

#tag1 #tag2
""")

        self.integration = MarkdownOxideIntegration(self.vault_path, verbose=True)

    def tearDown(self):
        """Clean up test vault."""
        self.temp_dir.cleanup()

    def test_integration_initialization(self):
        """Test integration initialization."""
        self.assertEqual(self.integration.vault_path, self.vault_path)
        self.assertIsInstance(self.integration.client, LSPClient)


class TestRecursiveLSP(unittest.TestCase):
    """Test RecursiveLSP class."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)

        # Create sample network
        (self.vault_path / "a.md").write_text("# A\n[[b]]")
        (self.vault_path / "b.md").write_text("# B\n[[c]]")
        (self.vault_path / "c.md").write_text("# C\n[[a]]")
        (self.vault_path / "orphan.md").write_text("# Orphan\nNo links here.")

        self.integration = MarkdownOxideIntegration(self.vault_path)
        self.recursive_lsp = RecursiveLSP(self.integration)

    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()

    def test_recursive_lsp_initialization(self):
        """Test RecursiveLSP initialization."""
        self.assertEqual(self.recursive_lsp.vault_path, self.vault_path)
        self.assertIsInstance(self.recursive_lsp.integration, MarkdownOxideIntegration)


class TestVaultLSPAnalyzer(unittest.TestCase):
    """Test VaultLSPAnalyzer class."""

    def setUp(self):
        """Set up test vault."""
        self.temp_dir = TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)

        # Create sample files
        (self.vault_path / "main.md").write_text("# Main\n[[sub1]] [[sub2]]")
        (self.vault_path / "sub1.md").write_text("# Sub1\n[[main]]")
        (self.vault_path / "sub2.md").write_text("# Sub2\n[[main]]")
        (self.vault_path / "orphan.md").write_text("# Orphan")

        self.analyzer = VaultLSPAnalyzer(self.vault_path, verbose=True)

    def tearDown(self):
        """Clean up test vault."""
        self.temp_dir.cleanup()

    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        self.assertEqual(self.analyzer.vault_path, self.vault_path)
        self.assertIsInstance(self.analyzer.integration, MarkdownOxideIntegration)
        self.assertIsInstance(self.analyzer.recursive_lsp, RecursiveLSP)

    def test_find_markdown_files(self):
        """Test finding markdown files."""
        files = self.analyzer.find_markdown_files()
        self.assertEqual(len(files), 4)


class TestCLIIntegration(unittest.TestCase):
    """Test CLI interface."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)
        (self.vault_path / "test.md").write_text("# Test\n[[link]]")

    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()

    def test_cli_parser_creation(self):
        """Test CLI parser creation."""
        from lsp_integration import create_parser
        parser = create_parser()
        self.assertIsNotNone(parser)


def run_tests():
    """Run all test suites."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLSPDataStructures))
    suite.addTests(loader.loadTestsFromTestCase(TestLSPClient))
    suite.addTests(loader.loadTestsFromTestCase(TestMarkdownOxideIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestRecursiveLSP))
    suite.addTests(loader.loadTestsFromTestCase(TestVaultLSPAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestCLIIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
