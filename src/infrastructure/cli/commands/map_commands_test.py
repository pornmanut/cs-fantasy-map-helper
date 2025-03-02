import pytest
from unittest.mock import MagicMock, patch
from src.infrastructure.cli.commands.map_commands import MapCommands

class TestMapCommands:
    @pytest.fixture
    def map_commands(self):
        """Create MapCommands instance with mocked game_map."""
        commands = MapCommands()
        commands.game_map = MagicMock()
        return commands

    def test_save_map_success(self, map_commands, capsys):
        """Test successful map saving."""
        map_commands.do_save("test_map.json")
        
        map_commands.game_map.save_map_to_file.assert_called_with("test_map.json")
        captured = capsys.readouterr()
        assert "Map saved successfully" in captured.out

    def test_save_map_default_filename(self, map_commands):
        """Test map saving with default filename."""
        map_commands.do_save("")
        map_commands.game_map.save_map_to_file.assert_called_with("map_data.json")

    def test_save_map_error(self, map_commands, capsys):
        """Test map saving with error."""
        map_commands.game_map.save_map_to_file.side_effect = Exception("Save failed")
        
        map_commands.do_save("test_map.json")
        captured = capsys.readouterr()
        assert "Failed to save map" in captured.out

    def test_load_map_success(self, map_commands, capsys):
        """Test successful map loading."""
        map_commands.do_load("test_map.json")
        
        map_commands.game_map.load_map_from_file.assert_called_with("test_map.json")
        captured = capsys.readouterr()
        assert "Map loaded successfully" in captured.out

    def test_load_map_no_filename(self, map_commands, capsys):
        """Test map loading without filename."""
        map_commands.do_load("")
        captured = capsys.readouterr()
        assert "Please specify a map file" in captured.out

    def test_load_map_error(self, map_commands, capsys):
        """Test map loading with error."""
        map_commands.game_map.load_map_from_file.side_effect = Exception("Load failed")
        
        map_commands.do_load("test_map.json")
        captured = capsys.readouterr()
        assert "Failed to load map" in captured.out

    def test_list_maps_success(self, map_commands, capsys):
        """Test successful map listing."""
        test_maps = [
            ("map1.json", 1.5, "2024-01-01"),
            ("map2.json", 2.0, "2024-01-02")
        ]
        map_commands.game_map.get_available_maps.return_value = test_maps
        
        map_commands.do_list_maps("")
        captured = capsys.readouterr()
        assert "map1.json" in captured.out
        assert "map2.json" in captured.out

    def test_list_maps_empty(self, map_commands, capsys):
        """Test map listing with no maps."""
        map_commands.game_map.get_available_maps.return_value = []
        
        map_commands.do_list_maps("")
        captured = capsys.readouterr()
        assert "No map files found" in captured.out

    def test_list_maps_error(self, map_commands, capsys):
        """Test map listing with error."""
        map_commands.game_map.get_available_maps.side_effect = Exception("List failed")
        
        map_commands.do_list_maps("")
        captured = capsys.readouterr()
        assert "Failed to list maps" in captured.out

    def test_quit_command(self, map_commands, capsys):
        """Test quit command."""
        result = map_commands.do_quit("")
        assert result is True
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_help_command_general(self, map_commands, capsys):
        """Test general help command."""
        map_commands.do_help("")
        captured = capsys.readouterr()
        assert "Command Categories" in captured.out
        assert "navigation" in captured.out
        assert "locations" in captured.out

    @pytest.mark.parametrize("category", ["navigation", "locations", "resources", "maps", "general"])
    def test_help_categories(self, map_commands, capsys, category):
        """Test help command for each category."""
        map_commands.do_help(category)
        captured = capsys.readouterr()
        assert captured.out  # Verify some output was produced

    def test_help_specific_command(self, map_commands, capsys):
        """Test help for specific command."""
        map_commands.do_help("save")
        captured = capsys.readouterr()
        assert "Save the current map" in captured.out

    def test_help_invalid_command(self, map_commands, capsys):
        """Test help for invalid command."""
        map_commands.do_help("invalid_command")
        captured = capsys.readouterr()
        assert "No help available" in captured.out
