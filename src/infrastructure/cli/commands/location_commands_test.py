import pytest
from unittest.mock import MagicMock, patch
from src.infrastructure.cli.commands.location_commands import LocationCommands
from src.domain.entities.direction import Direction

class TestLocationCommands:
    @pytest.fixture
    def location_commands(self):
        """Create LocationCommands instance with mocked game_map."""
        commands = LocationCommands()
        commands.game_map = MagicMock()
        return commands

    def test_add_location_success(self, location_commands, capsys):
        """Test successful location addition."""
        location_commands.do_add_location("Forest wood,berries")
        
        location_commands.game_map.create_location.assert_called_with("Forest", ["wood", "berries"])
        captured = capsys.readouterr()
        assert "Location 'Forest' added successfully" in captured.out

    def test_add_location_no_resources(self, location_commands, capsys):
        """Test location addition without resources."""
        location_commands.do_add_location("Forest")
        location_commands.game_map.create_location.assert_called_once_with("Forest", [])
        captured = capsys.readouterr()
        assert "Location 'Forest' added successfully" in captured.out

    def test_add_location_error(self, location_commands, capsys):
        """Test location addition with error."""
        location_commands.game_map.create_location.side_effect = ValueError("Location exists")
        
        location_commands.do_add_location("Forest")
        captured = capsys.readouterr()
        assert "Error: Location exists" in captured.out

    @patch('src.infrastructure.cli.commands.interactive.InteractivePrompt.prompt_selection')
    def test_add_connection_interactive(self, mock_prompt, location_commands, capsys):
        """Test successful interactive connection addition."""
        # Setup mock locations
        location_commands.game_map.list_locations.return_value = {
            "Forest": MagicMock(),
            "Beach": MagicMock(),
            "Mountain": MagicMock()
        }
        
        # Mock the three selection prompts (source, destination, direction)
        mock_prompt.side_effect = ["Forest", "Beach", "south"]
        
        # Call with empty args to trigger interactive mode
        location_commands.do_add_connection("")
        
        # Verify the selection prompts
        assert mock_prompt.call_count == 3
        calls = mock_prompt.call_args_list
        
        # Check source location prompt
        assert list(location_commands.game_map.list_locations().keys()) == \
               calls[0][0][0]  # First call, first argument (locations list)
        assert calls[0][0][1] == "Select source location"  # First call, second argument (prompt)
        
        # Check destination location prompt (should exclude source)
        assert sorted(["Beach", "Mountain"]) == \
               sorted(calls[1][0][0])  # Second call, first argument (filtered locations)
        assert calls[1][0][1] == "Select destination location"
        
        # Check direction prompt
        assert [d.value for d in Direction] == \
               calls[2][0][0]  # Third call, first argument (directions list)
        assert calls[2][0][1] == "Select direction"
        
        # Verify connection was added
        location_commands.game_map.add_connection.assert_called_with("Forest", "Beach", "south")
        captured = capsys.readouterr()
        assert "Connection added from 'Forest' to 'Beach' in direction 'south'" in captured.out
    
    def test_add_connection_interactive_no_locations(self, location_commands, capsys):
        """Test interactive connection addition with no locations available."""
        location_commands.game_map.list_locations.return_value = {}
        
        location_commands.do_add_connection("")
        
        captured = capsys.readouterr()
        assert "Error: No locations available. Create a location first." in captured.out

    @patch('src.infrastructure.cli.commands.interactive.InteractivePrompt.prompt_selection')
    def test_add_connection_interactive_cancel(self, mock_prompt, location_commands):
        """Test canceling interactive connection addition."""
        location_commands.game_map.list_locations.return_value = {
            "Forest": MagicMock(),
            "Beach": MagicMock()
        }
        
        # Mock user canceling at the first prompt
        mock_prompt.return_value = None
        
        location_commands.do_add_connection("")
        
        # Verify only first prompt was shown
        mock_prompt.assert_called_once()
        # Verify no connection was added
        location_commands.game_map.add_connection.assert_not_called()

    def test_add_connection_success(self, location_commands, capsys):
        """Test successful connection addition using direct arguments."""
        location_commands.do_add_connection("Forest Beach south")
        
        location_commands.game_map.add_connection.assert_called_with("Forest", "Beach", "south")
        captured = capsys.readouterr()
        assert "Connection added from 'Forest' to 'Beach' in direction 'south'" in captured.out

    def test_add_connection_error(self, location_commands, capsys):
        """Test connection addition with error."""
        location_commands.game_map.add_connection.side_effect = ValueError("Invalid location")
        
        location_commands.do_add_connection("Forest Beach south")
        captured = capsys.readouterr()
        assert "Error: Invalid location" in captured.out

    @patch('src.infrastructure.cli.commands.interactive.InteractivePrompt.prompt_selection')
    def test_goto_interactive(self, mock_prompt, location_commands, capsys):
        """Test interactive goto command."""
        location_commands.game_map.list_locations.return_value = {"Forest": MagicMock(), "Beach": MagicMock()}
        mock_prompt.return_value = "Forest"
        
        location_commands.do_goto("")
        
        mock_prompt.assert_called_once()
        location_commands.game_map.set_current_location.assert_called_with("Forest")

    def test_goto_direct(self, location_commands):
        """Test direct goto command."""
        location_commands.do_goto("Forest")
        location_commands.game_map.set_current_location.assert_called_with("Forest")

    def test_look_with_location(self, location_commands):
        """Test look command with current location."""
        location_commands.game_map.get_current_location.return_value = "Forest"
        location_commands.game_map.get_location_info.return_value = {
            "name": "Forest",
            "resources": ["wood"],
            "connections": {"North": "Mountain"}
        }
        
        location_commands.do_look("")
        location_commands.game_map.get_location_info.assert_called_with("Forest")

    def test_look_without_location(self, location_commands, capsys):
        """Test look command without current location."""
        location_commands.game_map.get_current_location.return_value = None
        
        location_commands.do_look("")
        captured = capsys.readouterr()
        assert "not at any location" in captured.out

    def test_list_locations(self, location_commands, capsys):
        """Test listing locations."""
        mock_location = MagicMock()
        mock_location.resources = ["wood"]
        mock_location.connections = {Direction.NORTH: "Mountain"}
        
        location_commands.game_map.list_locations.return_value = {"Forest": mock_location}
        
        location_commands.do_list_locations("")
        captured = capsys.readouterr()
        assert "Forest:" in captured.out
        assert "Resources: wood" in captured.out

    def test_path_success(self, location_commands, capsys):
        """Test successful path finding."""
        location_commands.game_map.get_current_location.return_value = "Forest"
        location_commands.game_map.resource_management.find_path.return_value = [Direction.NORTH, Direction.EAST]
        
        location_commands.do_path("Mountain")
        
        captured = capsys.readouterr()
        assert "Steps: 2" in captured.out
        assert "north → east" in captured.out

    def test_path_not_found(self, location_commands, capsys):
        """Test path finding when no path exists."""
        location_commands.game_map.get_current_location.return_value = "Forest"
        location_commands.game_map.resource_management.find_path.return_value = []
        
        location_commands.do_path("Mountain")
        
        captured = capsys.readouterr()
        assert "No path found" in captured.out

    @patch('src.infrastructure.cli.commands.interactive.InteractivePrompt.prompt_selection')
    def test_path_interactive(self, mock_prompt, location_commands):
        """Test interactive path finding."""
        location_commands.game_map.get_current_location.return_value = "Forest"
        location_commands.game_map.list_locations.return_value = {"Forest": MagicMock(), "Mountain": MagicMock()}
        mock_prompt.return_value = "Mountain"
        
        location_commands.do_path("")
        
        mock_prompt.assert_called_once()
        location_commands.game_map.resource_management.find_path.assert_called_with("Forest", "Mountain")
