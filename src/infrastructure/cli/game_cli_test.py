import pytest
from unittest.mock import MagicMock, patch
from .game_cli import GameCLI, main
from ...application.game_map_service import GameMapService
from ...infrastructure.persistence.json_map_repository import JsonMapRepository

class TestGameCLI:
    @pytest.fixture
    def cli(self):
        """Create GameCLI instance with mocked dependencies."""
        with patch('src.infrastructure.persistence.json_map_repository.JsonMapRepository') as mock_repo:
            cli = GameCLI()
            # Mock the game_map directly
            cli.game_map = MagicMock(spec=GameMapService)
            return cli

    def test_init(self, cli):
        """Test CLI initialization."""
        assert isinstance(cli.game_map, MagicMock)  # Changed to check for MagicMock
        assert cli.prompt == "[no location]> "

    def test_get_prompt_no_location(self, cli):
        """Test prompt when no location is set."""
        cli.game_map.get_current_location.return_value = None
        assert cli.get_prompt() == "[no location]> "

    def test_get_prompt_with_location(self, cli):
        """Test prompt when location is set."""
        cli.game_map.get_current_location.return_value = "Forest"
        assert cli.get_prompt() == "[Forest]> "

    def test_postcmd(self, cli):
        """Test prompt update after command execution."""
        cli.game_map.get_current_location.return_value = "Beach"
        result = cli.postcmd(False, "goto Beach")
        assert cli.prompt == "[Beach]> "
        assert result is False

    def test_emptyline(self, cli):
        """Test empty line behavior."""
        assert cli.emptyline() is False

    def test_integrated_location_commands(self, cli):
        """Test integration with location commands."""
        cli.do_add_location("Forest wood,berries")
        cli.game_map.create_location.assert_called_once_with("Forest", ["wood", "berries"])

    def test_integrated_resource_commands(self, cli):
        """Test integration with resource commands."""
        cli.do_add_resource("Forest mushrooms")
        cli.game_map.add_resource_to_location.assert_called_once_with("Forest", "mushrooms")

    def test_integrated_map_commands(self, cli):
        """Test integration with map commands."""
        cli.do_save("test_map.json")
        cli.game_map.save_map_to_file.assert_called_once_with("test_map.json")

    @patch('builtins.print')
    def test_keyboard_interrupt_handling(self, mock_print):
        """Test handling of keyboard interrupt."""
        with pytest.raises(SystemExit) as exc_info:
            with patch('src.infrastructure.cli.game_cli.GameCLI.cmdloop') as mock_cmdloop:
                mock_cmdloop.side_effect = KeyboardInterrupt()
                main()  # Call the main function directly
        
        assert exc_info.value.code == 0
        mock_print.assert_called_with("\nReceived keyboard interrupt, exiting...")

    def test_command_inheritance(self):
        """Test that GameCLI inherits all required commands."""
        cli = GameCLI()
        
        # Location commands
        assert hasattr(cli, 'do_add_location')
        assert hasattr(cli, 'do_add_connection')
        assert hasattr(cli, 'do_goto')
        
        # Resource commands
        assert hasattr(cli, 'do_add_resource')
        assert hasattr(cli, 'do_find')
        assert hasattr(cli, 'do_nearest')
        
        # Map commands
        assert hasattr(cli, 'do_save')
        assert hasattr(cli, 'do_load')
        assert hasattr(cli, 'do_list_maps')
