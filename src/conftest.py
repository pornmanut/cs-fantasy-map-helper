"""Shared test fixtures for the project."""
import pytest
from typing import Optional
from src.domain.entities.location import Location
from src.domain.entities.direction import Direction
from src.application.game_map_service import GameMapService
from src.infrastructure.persistence.json_map_repository import JsonMapRepository
from src.infrastructure.cli.game_cli import GameCLI

@pytest.fixture
def basic_map() -> dict[str, Location]:
    """Create a basic map with a few connected locations."""
    locations = {}
    
    # Create locations
    forest = Location("Forest", ["wood", "berries"])
    beach = Location("Beach", ["sand", "shells"])
    mountain = Location("Mountain", ["stone", "iron"])
    
    # Set up connections
    forest.add_connection(Direction.SOUTH, beach.name)
    beach.add_connection(Direction.NORTH, forest.name)
    beach.add_connection(Direction.EAST, mountain.name)
    mountain.add_connection(Direction.WEST, beach.name)
    
    locations.update({
        forest.name: forest,
        beach.name: beach,
        mountain.name: mountain
    })
    
    return locations

@pytest.fixture
def empty_map_service() -> GameMapService:
    """Create an empty GameMapService instance."""
    repository = JsonMapRepository()
    return GameMapService(repository)

@pytest.fixture
def populated_map_service(empty_map_service: GameMapService, basic_map: dict[str, Location]) -> GameMapService:
    """Create a GameMapService populated with basic map data."""
    # Add locations
    for location in basic_map.values():
        empty_map_service.create_location(location.name, location.resources)
    
    # Add connections (only in one direction as create_location handles bidirectional)
    empty_map_service.add_connection("Forest", "Beach", "south")
    empty_map_service.add_connection("Beach", "Mountain", "east")
    
    return empty_map_service

@pytest.fixture
def game_cli(populated_map_service: GameMapService) -> GameCLI:
    """Create a GameCLI instance with populated map."""
    cli = GameCLI()
    cli.game_map = populated_map_service
    return cli

@pytest.fixture
def cli_with_output() -> tuple[GameCLI, list[str]]:
    """Create a GameCLI instance that captures output."""
    cli = GameCLI()
    output: list[str] = []
    
    # Patch print to capture output
    def capture_print(msg: str) -> None:
        output.append(msg)
    
    cli._print = capture_print  # type: ignore
    
    return cli, output
