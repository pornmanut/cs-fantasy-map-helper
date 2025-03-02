import pytest
from unittest.mock import MagicMock, patch
from src.infrastructure.cli.commands.resource_commands import ResourceCommands
from src.domain.entities.direction import Direction
from src.domain.entities.location import Location

class TestResourceCommands:
    @pytest.fixture
    def resource_commands(self):
        """Create ResourceCommands instance with mocked game_map."""
        commands = ResourceCommands()
        commands.game_map = MagicMock()
        return commands

    @pytest.fixture
    def sample_locations(self):
        """Create sample location data for testing."""
        return {
            "Forest": Location("Forest", ["wood", "berries"]),
            "Beach": Location("Beach", ["sand", "fish"]),
            "Mountain": Location("Mountain", ["stone", "wood"])
        }

    def test_get_all_resources(self, resource_commands, sample_locations):
        """Test getting all unique resources."""
        resource_commands.game_map.list_locations.return_value = sample_locations
        resources = resource_commands._get_all_resources()
        assert sorted(resources) == ["berries", "fish", "sand", "stone", "wood"]

    @patch('src.infrastructure.cli.commands.interactive.InteractivePrompt.prompt_selection')
    @patch('builtins.input')
    def test_add_resource_interactive(self, mock_input, mock_prompt, resource_commands, sample_locations, capsys):
        """Test interactive resource addition."""
        # Setup mocks
        resource_commands.game_map.list_locations.return_value = sample_locations
        mock_prompt.return_value = "Forest"
        mock_input.return_value = "mushrooms,herbs"
        
        # Call with empty args to trigger interactive mode
        resource_commands.do_add_resource("")
        
        # Verify prompt was called with correct arguments
        mock_prompt.assert_called_once_with(
            list(sample_locations.keys()),
            "Select location",
            error_handler=resource_commands.error
        )
        
        # Verify resources were added
        assert resource_commands.game_map.add_resource_to_location.call_count == 2
        resource_commands.game_map.add_resource_to_location.assert_any_call("Forest", "mushrooms")
        resource_commands.game_map.add_resource_to_location.assert_any_call("Forest", "herbs")
        
        captured = capsys.readouterr()
        assert "Resources added to 'Forest' successfully" in captured.out

    def test_add_resource_interactive_no_locations(self, resource_commands, capsys):
        """Test interactive resource addition with no locations available."""
        resource_commands.game_map.list_locations.return_value = {}
        
        resource_commands.do_add_resource("")
        
        captured = capsys.readouterr()
        assert "Error: No locations available. Create a location first." in captured.out

    def test_add_resource_success(self, resource_commands, capsys):
        """Test successful resource addition using direct arguments."""
        resource_commands.do_add_resource("Forest mushrooms,herbs")
        
        assert resource_commands.game_map.add_resource_to_location.call_count == 2
        resource_commands.game_map.add_resource_to_location.assert_any_call("Forest", "mushrooms")
        resource_commands.game_map.add_resource_to_location.assert_any_call("Forest", "herbs")
        
        captured = capsys.readouterr()
        assert "Resources added to 'Forest' successfully" in captured.out

    def test_add_resource_error(self, resource_commands, capsys):
        """Test resource addition with error."""
        resource_commands.game_map.add_resource_to_location.side_effect = ValueError("Location not found")
        
        resource_commands.do_add_resource("NonExistent wood")
        captured = capsys.readouterr()
        assert "Error: Location not found" in captured.out

    def test_add_resource_no_resources(self, resource_commands, capsys):
        """Test resource addition with empty resource list."""
        resource_commands.do_add_resource("Forest ,,")  # Empty resources using commas
        captured = capsys.readouterr()
        assert "No valid resources specified" in captured.out

    @patch('src.infrastructure.cli.commands.interactive.InteractivePrompt.prompt_selection')
    def test_find_interactive(self, mock_prompt, resource_commands, sample_locations, capsys):
        """Test interactive resource finding."""
        resource_commands.game_map.list_locations.return_value = sample_locations
        mock_prompt.return_value = "wood"
        resource_commands.game_map.resource_management.find_resource.return_value = ["Forest", "Mountain"]
        
        resource_commands.do_find("")
        
        captured = capsys.readouterr()
        assert "Found 'wood' in: Forest, Mountain" in captured.out

    def test_find_direct(self, resource_commands, capsys):
        """Test direct resource finding."""
        resource_commands.game_map.resource_management.find_resource.return_value = ["Forest"]
        
        resource_commands.do_find("wood")
        captured = capsys.readouterr()
        assert "Found 'wood' in: Forest" in captured.out

    def test_find_not_found(self, resource_commands, capsys):
        """Test finding non-existent resource."""
        resource_commands.game_map.resource_management.find_resource.return_value = []
        
        resource_commands.do_find("gold")
        captured = capsys.readouterr()
        assert "not found in any location" in captured.out

    def test_nearest_success(self, resource_commands, capsys):
        """Test finding nearest resource location."""
        resource_commands.game_map.get_current_location.return_value = "Beach"
        resource_commands.game_map.find_path_to_resource.return_value = (
            "Forest", 
            [Direction.NORTH, Direction.EAST]
        )
        
        resource_commands.do_nearest("wood")
        
        captured = capsys.readouterr()
        assert "Nearest location with 'wood': Forest" in captured.out
        assert "Steps: 2" in captured.out
        assert "Directions: north → east" in captured.out

    def test_nearest_at_current_location(self, resource_commands, capsys):
        """Test finding resource at current location."""
        resource_commands.game_map.get_current_location.return_value = "Forest"
        resource_commands.game_map.find_path_to_resource.return_value = ("Forest", [])
        
        resource_commands.do_nearest("wood")
        
        captured = capsys.readouterr()
        assert "available at your current location" in captured.out

    def test_nearest_not_found(self, resource_commands, capsys):
        """Test nearest when resource doesn't exist."""
        resource_commands.game_map.get_current_location.return_value = "Forest"
        resource_commands.game_map.find_path_to_resource.return_value = None
        
        resource_commands.do_nearest("gold")
        
        captured = capsys.readouterr()
        assert "No location found containing 'gold'" in captured.out

    def test_list_resources(self, resource_commands, sample_locations, capsys):
        """Test listing all resources."""
        resource_commands.game_map.list_locations.return_value = sample_locations
        
        resource_commands.do_list_resources("")
        
        captured = capsys.readouterr()
        assert "Available Resources:" in captured.out
        # Fix: Match the exact case and format from the output
        assert "wood: Forest, Mountain".lower() in captured.out.lower()
        assert "berries: Forest".lower() in captured.out.lower()
        assert "sand: Beach".lower() in captured.out.lower()

    def test_list_resources_empty(self, resource_commands, capsys):
        """Test listing resources when none exist."""
        resource_commands.game_map.list_locations.return_value = {}
        
        resource_commands.do_list_resources("")
        
        captured = capsys.readouterr()
        assert "No resources available" in captured.out
