import pytest
from typing import Optional
from .game_map_service import GameMapService
from ..domain.entities.location import Location
from ..domain.entities.direction import Direction
from .interfaces.map_repository import MapRepository

class MockMapRepository(MapRepository):
    def save_map(self, filename: str, locations: dict[str, Location]) -> None:
        pass

    def load_map(self, filename: str) -> dict[str, Location]:
        return {}

    def list_maps(self) -> list[tuple[str, float, str]]:
        return []
        
    def list_available_maps(self) -> list[str]:
        return []

class TestGameMapService:
    @pytest.fixture
    def game_service(self) -> GameMapService:
        """Create a fresh GameMapService instance for testing."""
        return GameMapService(MockMapRepository())

    @pytest.fixture
    def populated_service(self, game_service: GameMapService) -> GameMapService:
        """Create a GameMapService with sample data."""
        game_service.create_location("Forest", ["wood", "berries"])
        game_service.create_location("Beach", ["sand", "water"])
        game_service.add_connection("Forest", "Beach", "south")
        game_service.set_current_location("Forest")
        return game_service

    def test_create_location(self, game_service: GameMapService) -> None:
        """Test location creation with resources."""
        game_service.create_location("Forest", ["wood", "berries"])
        location = game_service.get_location("Forest")
        
        assert location is not None
        assert location.name == "Forest"
        assert "wood" in location.resources
        assert "berries" in location.resources

    def test_add_resource_to_location(self, populated_service: GameMapService) -> None:
        """Test adding a resource to an existing location."""
        populated_service.add_resource_to_location("Forest", "mushrooms")
        location = populated_service.get_location("Forest")
        
        assert location is not None
        assert "mushrooms" in location.resources

    def test_add_connection(self, populated_service: GameMapService) -> None:
        """Test adding connections between locations."""
        location = populated_service.get_location("Forest")
        assert location is not None
        assert Direction.SOUTH in location.connections
        assert location.connections[Direction.SOUTH] == "Beach"

    def test_find_path_to_resource(self, populated_service: GameMapService) -> None:
        """Test finding path to a resource."""
        result = populated_service.find_path_to_resource("sand")
        assert result is not None
        location, path = result
        assert location == "Beach"
        assert path == [Direction.SOUTH]

    def test_get_location_info(self, populated_service: GameMapService) -> None:
        """Test getting detailed location information."""
        info = populated_service.get_location_info("Forest")
        assert info["name"] == "Forest"
        assert "wood" in info["resources"]
        assert "berries" in info["resources"]
        assert info["connections"]["south"] == "Beach"

    def test_clear_locations(self, populated_service: GameMapService) -> None:
        """Test clearing all locations."""
        populated_service.clear_locations()
        assert len(populated_service.list_locations()) == 0
        assert populated_service.get_current_location() is None

    def test_invalid_operations(self, game_service: GameMapService) -> None:
        """Test error handling for invalid operations."""
        with pytest.raises(ValueError):
            game_service.find_path_to_resource("gold")  # No current location set

        with pytest.raises(ValueError):
            game_service.get_location_info("NonExistent")

    def test_current_location_management(self, populated_service: GameMapService) -> None:
        """Test current location getter and setter."""
        assert populated_service.get_current_location() == "Forest"
        
        populated_service.set_current_location("Beach")
        assert populated_service.get_current_location() == "Beach"
        
        populated_service.set_current_location(None)
        assert populated_service.get_current_location() is None

    def test_resource_tracking(self, populated_service: GameMapService) -> None:
        """Test resource tracking across locations."""
        result = populated_service.find_path_to_resource("water")
        assert result is not None
        location, path = result
        assert location == "Beach"
        
        # Add same resource to another location
        populated_service.add_resource_to_location("Forest", "water")
        result = populated_service.find_path_to_resource("water")
        assert result is not None
        location, path = result
        assert location == "Forest"  # Should find the closest location
        assert len(path) == 0
