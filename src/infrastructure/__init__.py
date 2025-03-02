"""Infrastructure layer implementing external interfaces."""

from .persistence.json_map_repository import JsonMapRepository
from .cli.game_cli import GameCLI

__all__ = ['JsonMapRepository', 'GameCLI']
