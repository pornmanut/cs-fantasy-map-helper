import pytest
from unittest.mock import patch
from src.infrastructure.cli.commands.interactive import InteractivePrompt

class TestInteractivePrompt:
    """Test cases for InteractivePrompt class."""

    @pytest.fixture
    def prompt(self) -> InteractivePrompt:
        """Create an interactive prompt instance."""
        return InteractivePrompt()

    def test_format_options(self) -> None:
        """Test formatting list of options."""
        items = ["apple", "banana", "orange"]
        result = InteractivePrompt.format_options(items)
        expected = "1. apple\n2. banana\n3. orange"
        assert result == expected

    def test_format_options_with_formatter(self) -> None:
        """Test formatting options with custom formatter."""
        items = [1, 2, 3]
        formatter = lambda x: f"Item {x}"
        result = InteractivePrompt.format_options(items, formatter)
        expected = "1. Item 1\n2. Item 2\n3. Item 3"
        assert result == expected

    def test_get_close_matches(self) -> None:
        """Test finding close matches for a word."""
        possibilities = ["forest", "beach", "mountain"]
        
        # Exact match
        matches = InteractivePrompt.get_close_matches("forest", possibilities)
        assert matches == ["forest"]

        # Close match
        matches = InteractivePrompt.get_close_matches("forst", possibilities)
        assert "forest" in matches

        # Multiple close matches
        matches = InteractivePrompt.get_close_matches("mountan", possibilities)
        assert "mountain" in matches

        # No close matches
        matches = InteractivePrompt.get_close_matches("xyz", possibilities)
        assert len(matches) == 0

    @patch('builtins.input')
    def test_prompt_selection_by_number(self, mock_input) -> None:
        """Test selecting option by number."""
        items = ["forest", "beach", "mountain"]
        mock_input.return_value = "2"
        
        result = InteractivePrompt.prompt_selection(
            items,
            "Select location",
            error_handler=lambda msg: None
        )
        assert result == "beach"

    @patch('builtins.input')
    def test_prompt_selection_by_name(self, mock_input) -> None:
        """Test selecting option by name."""
        items = ["forest", "beach", "mountain"]
        mock_input.return_value = "forest"
        
        result = InteractivePrompt.prompt_selection(
            items,
            "Select location",
            error_handler=lambda msg: None
        )
        assert result == "forest"

    @patch('builtins.input')
    def test_prompt_selection_with_fuzzy_match(self, mock_input) -> None:
        """Test selecting option with fuzzy matching."""
        items = ["forest", "beach", "mountain"]
        
        # First input is misspelled, second input selects from suggestions
        mock_input.side_effect = ["forst", "1"]
        
        result = InteractivePrompt.prompt_selection(
            items,
            "Select location",
            error_handler=lambda msg: None
        )
        assert result == "forest"

    @patch('builtins.input')
    def test_prompt_selection_cancel(self, mock_input) -> None:
        """Test cancelling selection."""
        items = ["forest", "beach", "mountain"]
        mock_input.return_value = ""
        
        result = InteractivePrompt.prompt_selection(
            items,
            "Select location",
            error_handler=lambda msg: None
        )
        assert result is None

    @patch('builtins.input')
    def test_prompt_selection_invalid_input(self, mock_input) -> None:
        """Test handling invalid input."""
        items = ["forest", "beach", "mountain"]
        
        # First try invalid number, then valid
        mock_input.side_effect = ["99", "1"]
        
        errors = []
        def error_handler(msg: str) -> None:
            errors.append(msg)

        result = InteractivePrompt.prompt_selection(
            items,
            "Select location",
            error_handler=error_handler
        )
        
        assert result == "forest"
        assert len(errors) == 1
        assert "Invalid selection" in errors[0]

    def test_prompt_selection_empty_list(self) -> None:
        """Test handling empty list of items."""
        errors = []
        def error_handler(msg: str) -> None:
            errors.append(msg)

        result = InteractivePrompt.prompt_selection(
            [],
            "Select location",
            error_handler=error_handler
        )
        
        assert result is None
        assert len(errors) == 1
        assert "No items available" in errors[0]
