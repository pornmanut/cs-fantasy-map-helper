import pytest
from unittest.mock import MagicMock
from src.infrastructure.cli.commands.base_commands import CommandMixin
from src.domain.entities.direction import Direction
from src.application.game_map_service import GameMapService

class TestCommandMixin:
    @pytest.fixture
    def command_mixin(self):
        """Create a CommandMixin instance with mocked game_map."""
        class TestCommands(CommandMixin):
            def __init__(self):
                self.game_map = MagicMock(spec=GameMapService)
        return TestCommands()

    def test_format_directions(self, command_mixin):
        """Test formatting of direction list."""
        directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST]
        result = command_mixin.format_directions(directions)
        assert result == "north → south → east"

    def test_require_args_valid(self, command_mixin):
        """Test argument validation with valid input."""
        result = command_mixin.require_args("arg1 arg2", 2, "command arg1 arg2")
        assert result == ["arg1", "arg2"]

    def test_require_args_invalid(self, command_mixin, capsys):
        """Test argument validation with invalid input."""
        result = command_mixin.require_args("arg1", 2, "command arg1 arg2")
        captured = capsys.readouterr()
        assert result is None
        assert "Required format: command arg1 arg2" in captured.out

    def test_parse_resources_empty(self, command_mixin):
        """Test parsing empty resource string."""
        result = command_mixin.parse_resources("")
        assert result == []

    def test_parse_resources_valid(self, command_mixin):
        """Test parsing valid resource string."""
        result = command_mixin.parse_resources("wood,stone, water")
        assert result == ["wood", "stone", "water"]

    def test_show_location_info_success(self, command_mixin, capsys):
        """Test showing location info for existing location."""
        command_mixin.game_map.get_location_info.return_value = {
            "name": "Forest",
            "resources": ["wood", "berries"],
            "connections": {"North": "Mountain"}
        }
        
        command_mixin.show_location_info("Forest")
        captured = capsys.readouterr()
        assert "Location: Forest" in captured.out
        assert "Resources: wood, berries" in captured.out
        assert "North: Mountain" in captured.out

    def test_show_location_info_error(self, command_mixin, capsys):
        """Test showing location info for non-existent location."""
        command_mixin.game_map.get_location_info.side_effect = ValueError("Location not found")
        
        command_mixin.show_location_info("NonExistent")
        captured = capsys.readouterr()
        assert "Error: Location not found" in captured.out

    def test_require_current_location_set(self, command_mixin):
        """Test current location check when location is set."""
        command_mixin.game_map.get_current_location.return_value = "Forest"
        assert command_mixin.require_current_location() is True

    def test_require_current_location_not_set(self, command_mixin, capsys):
        """Test current location check when no location is set."""
        command_mixin.game_map.get_current_location.return_value = None
        assert command_mixin.require_current_location() is False
        captured = capsys.readouterr()
        assert "Error: No current location set" in captured.out

    def test_message_output(self, command_mixin, capsys):
        """Test various message output methods."""
        command_mixin.error("Error message")
        command_mixin.success("Success message")
        command_mixin.info("Info message")
        command_mixin.warning("Warning message")
        
        captured = capsys.readouterr()
        assert "Error: Error message" in captured.out
        assert "Success message" in captured.out
        assert "Info message" in captured.out
        assert "Warning message" in captured.out
