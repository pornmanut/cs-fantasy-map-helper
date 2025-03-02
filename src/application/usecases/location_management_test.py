import pytest
from typing import Protocol
from src.domain.entities.location import Location
from src.domain.entities.direction import Direction
from src.application.usecases.location_management import LocationManagement, LocationRepository

class MockLocationRepository(LocationRepository):
    """Mock repository for testing location management."""
    
    def __init__(self) -> None:
        self.locations: dict[str, Location] = {}

    def add_location(self, location: Location) -> None:
        self.locations[location.name] = location

    def get_location(self, name: str) -> Location | None:
        return self.locations.get(name)

    def update_location(self, location: Location) -> None:
        self.locations[location.name] = location

    def list_locations(self) -> dict[str, Location]:
        return self.locations.copy()

class TestLocationManagement:
    """Test cases for LocationManagement use case."""

    @pytest.fixture
    def location_repo(self) -> MockLocationRepository:
        """Create a mock location repository."""
        return MockLocationRepository()

    @pytest.fixture
    def manager(self, location_repo: MockLocationRepository) -> LocationManagement:
        """Create a location management instance with mock repository."""
        return LocationManagement(location_repo)

    def test_add_location(self, manager: LocationManagement) -> None:
        """Test adding a new location."""
        manager.add_location("Forest", ["wood", "berries"])
        location = manager._repository.get_location("Forest")
        assert location is not None
        assert location.name == "Forest"
        assert "wood" in location.resources
        assert "berries" in location.resources

    def test_add_duplicate_location(self, manager: LocationManagement) -> None:
        """Test adding a location with a name that already exists."""
        manager.add_location("Forest")
        with pytest.raises(ValueError):
            manager.add_location("Forest")

    def test_add_connection(self, manager: LocationManagement) -> None:
        """Test connecting two locations."""
        manager.add_location("Forest")
        manager.add_location("Beach")
        manager.add_connection("Forest", "Beach", Direction.SOUTH)

        forest = manager._repository.get_location("Forest")
        beach = manager._repository.get_location("Beach")
        assert forest is not None and beach is not None

        # Check bidirectional connection
        assert forest.get_connection(Direction.SOUTH) == "Beach"
        assert beach.get_connection(Direction.NORTH) == "Forest"

    def test_invalid_connection(self, manager: LocationManagement) -> None:
        """Test error handling for invalid connections."""
        manager.add_location("Forest")
        
        # Non-existent target location
        with pytest.raises(ValueError):
            manager.add_connection("Forest", "NonExistent", Direction.SOUTH)

        # Non-existent source location
        with pytest.raises(ValueError):
            manager.add_connection("NonExistent", "Forest", Direction.SOUTH)

    def test_get_current_location(self, manager: LocationManagement) -> None:
        """Test getting and setting current location."""
        assert manager.get_current_location() is None

        manager.add_location("Forest")
        manager.set_current_location("Forest")
        
        location = manager.get_current_location()
        assert location is not None
        assert location.name == "Forest"

    def test_set_invalid_current_location(self, manager: LocationManagement) -> None:
        """Test setting current location to non-existent location."""
        with pytest.raises(ValueError):
            manager.set_current_location("NonExistent")

    def test_get_connected_locations(self, manager: LocationManagement) -> None:
        """Test getting connections for a location."""
        manager.add_location("Forest")
        manager.add_location("Beach")
        manager.add_location("Mountain")

        manager.add_connection("Forest", "Beach", Direction.SOUTH)
        manager.add_connection("Forest", "Mountain", Direction.NORTH)

        connections = manager.get_connected_locations("Forest")
        assert connections[Direction.SOUTH] == "Beach"
        assert connections[Direction.NORTH] == "Mountain"

    def test_get_connections_nonexistent_location(self, manager: LocationManagement) -> None:
        """Test getting connections for non-existent location."""
        with pytest.raises(ValueError):
            manager.get_connected_locations("NonExistent")

    def test_location_exists(self, manager: LocationManagement) -> None:
        """Test checking location existence."""
        manager.add_location("Forest")
        assert manager.location_exists("Forest")
        assert not manager.location_exists("NonExistent")

    def test_list_locations(self, manager: LocationManagement) -> None:
        """Test listing all locations."""
        manager.add_location("Forest")
        manager.add_location("Beach")
        
        locations = manager.list_locations()
        assert len(locations) == 2
        assert "Forest" in locations
        assert "Beach" in locations
