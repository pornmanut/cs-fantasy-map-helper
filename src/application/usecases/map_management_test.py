import pytest
from typing import Protocol, Optional, List, Tuple
from src.domain.entities.location import Location
from src.domain.entities.direction import Direction
from src.application.interfaces.map_repository import MapRepository
from src.application.usecases.map_management import MapManagement, LocationProvider

class MockMapRepository(MapRepository):
    """Mock repository for testing map persistence."""
    
    def __init__(self) -> None:
        self.stored_data: dict[str, tuple[dict[str, Location], Optional[str]]] = {}

    def save_map(self, filename: str, locations: dict[str, Location], current_location: Optional[str]) -> None:
        self.stored_data[filename] = (locations.copy(), current_location)

    def load_map(self, filename: str) -> tuple[dict[str, Location], Optional[str]]:
        if filename not in self.stored_data:
            raise FileNotFoundError(f"Map file '{filename}' not found")
        locations, current = self.stored_data[filename]
        return locations.copy(), current

    def list_available_maps(self) -> list[tuple[str, float, str]]:
        return [(name, 1.0, "2024-01-01 00:00:00") for name in self.stored_data.keys()]

class MockLocationProvider(LocationProvider):
    """Mock location provider for testing map management."""
    
    def __init__(self) -> None:
        self.locations: dict[str, Location] = {}
        self.current_location: Optional[str] = None

    def list_locations(self) -> dict[str, Location]:
        return self.locations.copy()

    def get_current_location(self) -> Optional[str]:
        return self.current_location

    def set_current_location(self, location_name: Optional[str]) -> None:
        self.current_location = location_name

    def clear_locations(self) -> None:
        self.locations.clear()
        self.current_location = None

    def add_location(self, location: Location) -> None:
        self.locations[location.name] = location

    def add_connection(self, from_loc: str, to_loc: str, direction: str) -> None:
        if from_loc in self.locations and to_loc in self.locations:
            dir_enum = Direction(direction.lower())
            self.locations[from_loc].add_connection(dir_enum, to_loc)

class TestMapManagement:
    """Test cases for MapManagement use case."""

    @pytest.fixture
    def map_repo(self) -> MockMapRepository:
        """Create a mock map repository."""
        return MockMapRepository()

    @pytest.fixture
    def location_provider(self) -> MockLocationProvider:
        """Create a mock location provider."""
        return MockLocationProvider()

    @pytest.fixture
    def manager(self, map_repo: MockMapRepository, location_provider: MockLocationProvider) -> MapManagement:
        """Create a map management instance with mocks."""
        return MapManagement(map_repo, location_provider)

    @pytest.fixture
    def sample_map(self, location_provider: MockLocationProvider) -> None:
        """Set up a sample map in the location provider."""
        forest = Location("Forest", ["wood", "berries"])
        beach = Location("Beach", ["sand"])
        forest.add_connection(Direction.SOUTH, beach.name)
        beach.add_connection(Direction.NORTH, forest.name)
        
        location_provider.add_location(forest)
        location_provider.add_location(beach)
        location_provider.set_current_location("Forest")

    def test_save_map(self, manager: MapManagement, sample_map: None, map_repo: MockMapRepository) -> None:
        """Test saving map state."""
        manager.save_map("test_map.json")
        
        # Verify saved data
        assert "test_map.json" in map_repo.stored_data
        locations, current = map_repo.stored_data["test_map.json"]
        
        assert len(locations) == 2
        assert "Forest" in locations
        assert "Beach" in locations
        assert current == "Forest"

    def test_load_map(self, manager: MapManagement, map_repo: MockMapRepository, location_provider: MockLocationProvider) -> None:
        """Test loading map state."""
        # Create and save a sample map
        forest = Location("Forest", ["wood"])
        map_repo.stored_data["test_map.json"] = ({"Forest": forest}, "Forest")

        # Load the map
        manager.load_map("test_map.json")

        # Verify loaded state
        assert len(location_provider.locations) == 1
        assert "Forest" in location_provider.locations
        assert location_provider.get_current_location() == "Forest"

    def test_load_nonexistent_map(self, manager: MapManagement) -> None:
        """Test error handling when loading non-existent map."""
        with pytest.raises(RuntimeError):
            manager.load_map("nonexistent.json")

    def test_list_available_maps(self, manager: MapManagement, map_repo: MockMapRepository) -> None:
        """Test listing available maps."""
        # Set up some sample maps
        forest = Location("Forest", ["wood"])
        beach = Location("Beach", ["sand"])
        map_repo.stored_data.update({
            "map1.json": ({"Forest": forest}, None),
            "map2.json": ({"Beach": beach}, None)
        })

        # List maps
        map_list = manager.list_available_maps()
        assert len(map_list) == 2
        assert any(name == "map1.json" for name, _, _ in map_list)
        assert any(name == "map2.json" for name, _, _ in map_list)

    def test_clear_locations_on_load(self, manager: MapManagement, map_repo: MockMapRepository, 
                                   location_provider: MockLocationProvider, sample_map: None) -> None:
        """Test that loading a map clears existing locations."""
        # Verify initial state
        assert len(location_provider.locations) == 2
        
        # Create and load a different map
        new_location = Location("Mountain", ["stone"])
        map_repo.stored_data["new_map.json"] = ({"Mountain": new_location}, "Mountain")
        
        manager.load_map("new_map.json")
        
        # Verify old state was cleared
        assert len(location_provider.locations) == 1
        assert "Mountain" in location_provider.locations
        assert "Forest" not in location_provider.locations
