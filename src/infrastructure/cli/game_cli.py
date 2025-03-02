import cmd
from typing import Optional
from colorama import init as colorama_init
from ...application.game_map_service import GameMapService
from ...infrastructure.persistence.json_map_repository import JsonMapRepository
from .commands.base_commands import CommandMixin
from .commands.location_commands import LocationCommands
from .commands.resource_commands import ResourceCommands
from .commands.map_commands import MapCommands

class GameCLI(cmd.Cmd, LocationCommands, ResourceCommands, MapCommands):
    """Main CLI class that combines all command modules."""

    def __init__(self):
        super().__init__()
        colorama_init()
        
        # Initialize game map service
        map_repository = JsonMapRepository()
        self.game_map = GameMapService(map_repository)
        
        # Set initial prompt
        self.prompt = self.get_prompt()
        
        # Show available maps when starting
        self.do_list_maps("")
        self.info("Type 'load <filename>' to load a map, or start creating a new one.\n")

    def get_prompt(self) -> str:
        """Generate the prompt string based on current location"""
        if not self.game_map.get_current_location():
            return f'[no location]> '
        return f'[{self.game_map.get_current_location()}]> '

    def postcmd(self, stop: bool, line: str) -> bool:
        """Update prompt after each command"""
        self.prompt = self.get_prompt()
        return stop

    def emptyline(self) -> bool:
        """Do nothing on empty line"""
        return False

def main() -> None:
    try:
        GameCLI().cmdloop()
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt, exiting...")
        import sys
        sys.exit(0)

if __name__ == "__main__":
    main()
