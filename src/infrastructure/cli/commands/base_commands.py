from typing import Optional, Protocol, Any
from colorama import Fore, Style
from src.domain.entities.direction import Direction
from src.application.game_map_service import GameMapService

class BaseCommands(Protocol):
    """Protocol defining base functionality for CLI commands."""
    game_map: GameMapService
    
    def error(self, message: str) -> None: ...
    def success(self, message: str) -> None: ...
    def info(self, message: str) -> None: ...
    def warning(self, message: str) -> None: ...
    def format_directions(self, directions: list[Direction]) -> str: ...

class CommandMixin:
    """Mixin providing common functionality for CLI commands."""
    game_map: GameMapService

    def error(self, message: str) -> None:
        """Display an error message."""
        print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")

    def success(self, message: str) -> None:
        """Display a success message."""
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    def info(self, message: str) -> None:
        """Display an info message."""
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

    def warning(self, message: str) -> None:
        """Display a warning message."""
        print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

    def format_directions(self, directions: list[Direction]) -> str:
        """Format a list of directions into a readable string."""
        return " → ".join(d.value for d in directions)

    def require_args(self, args: str, count: int, usage: str) -> Optional[list[str]]:
        """Validate and split command arguments."""
        parts = args.split()
        if len(parts) != count:
            self.error(f"Required format: {usage}")
            return None
        return parts

    def parse_resources(self, resources_str: str) -> list[str]:
        """Parse a comma-separated list of resources."""
        if not resources_str:
            return []
        return [r.strip() for r in resources_str.split(",") if r.strip()]

    def show_location_info(self, name: str) -> None:
        """Display information about a location."""
        try:
            info = self.game_map.get_location_info(name)
            print(f"\n{Fore.CYAN}Location: {info['name']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Resources: {', '.join(info['resources']) or 'None'}")
            print(f"Connections:")
            for direction, target in info['connections'].items():
                print(f"  {direction}: {target}{Style.RESET_ALL}")
        except ValueError as e:
            self.error(str(e))

    def require_current_location(self) -> bool:
        """Check if there is a current location set."""
        if not self.game_map.get_current_location():
            self.error("No current location set. Use 'goto' first.")
            return False
        return True
