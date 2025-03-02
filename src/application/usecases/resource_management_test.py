import pytest
from typing import Protocol, Optional
from src.domain.entities.location import Location
from src.domain.entities.direction import Direction
from src.application.usecases.resource_management import ResourceManagement, ResourceRepository

class MockResourceRepository(ResourceRepository):
    """Mock repository for testing resource management."""
    
    def __init__(self) -> None:
        self.locations: dict[str, Location] = {}

    def get_location(self, name: str) -> Optional[Location]:
        return self.locations.get(name)

    def list_locations(self) -> dict[str, Location]:
        return self.locations.copy()

    def update_location(self, location: Location) -> None:
        self.locations[location.name] = location

class TestResourceManagement:
    """Test cases for ResourceManagement use case."""

    @pytest.fixture
    def resource_repo(self) -> MockResourceRepository:
        """Create a mock resource repository."""
        return MockResourceRepository()

    @pytest.fixture
    def manager(self, resource_repo: MockResourceRepository) -> ResourceManagement:
        """Create a resource management instance with mock repository."""
        return ResourceManagement(resource_repo)

    @pytest.fixture
    def populated_repo(self, resource_repo: MockResourceRepository) -> MockResourceRepository:
        """Create a repository with sample locations and resources."""
        forest = Location("Forest", ["wood", "berries"])
        beach = Location("Beach", ["sand", "coconuts"])
        mountain = Location("Mountain", ["stone", "iron"])

        # Set up connections
        forest.add_connection(Direction.SOUTH, beach.name)
        beach.add_connection(Direction.NORTH, forest.name)
        beach.add_connection(Direction.EAST, mountain.name)
        mountain.add_connection(Direction.WEST, beach.name)

        resource_repo.locations.update({
            forest.name: forest,
            beach.name: beach,
            mountain.name: mountain
        })
        return resource_repo

    def test_add_resource(self, manager: ResourceManagement, populated_repo: MockResourceRepository) -> None:
        """Test adding a resource to a location."""
        manager.add_resource("Forest", "mushrooms")
        location = populated_repo.get_location("Forest")
        assert location is not None
        assert "mushrooms" in location.resources

    def test_add_resource_to_nonexistent_location(self, manager: ResourceManagement) -> None:
        """Test error handling when adding resource to non-existent location."""
        with pytest.raises(ValueError):
            manager.add_resource("NonExistent", "gold")

    def test_find_resource(self, manager: ResourceManagement, populated_repo: MockResourceRepository) -> None:
        """Test finding locations with a specific resource."""
        locations = manager.find_resource("wood")
        assert len(locations) == 1
        assert "Forest" in locations

        # Test resource in multiple locations
        manager.add_resource("Beach", "wood")
        locations = manager.find_resource("wood")
        assert len(locations) == 2
        assert "Forest" in locations
        assert "Beach" in locations

    def test_find_nonexistent_resource(self, manager: ResourceManagement, populated_repo: MockResourceRepository) -> None:
        """Test finding a resource that doesn't exist anywhere."""
        locations = manager.find_resource("gold")
        assert len(locations) == 0

    def test_find_path(self, manager: ResourceManagement, populated_repo: MockResourceRepository) -> None:
        """Test finding path between locations."""
        path = manager.find_path("Forest", "Mountain")
        assert path is not None
        assert len(path) == 2
        assert path[0] == Direction.SOUTH  # Forest -> Beach
        assert path[1] == Direction.EAST   # Beach -> Mountain

    def test_find_path_nonexistent_location(self, manager: ResourceManagement, populated_repo: MockResourceRepository) -> None:
        """Test finding path with non-existent location."""
        assert manager.find_path("Forest", "NonExistent") is None
        assert manager.find_path("NonExistent", "Forest") is None

    def test_find_nearest_resource(self, manager: ResourceManagement, populated_repo: MockResourceRepository) -> None:
        """Test finding nearest location with specific resource."""
        # Test from Forest to nearest stone (in Mountain)
        result = manager.find_nearest_resource("stone", "Forest")
        assert result is not None
        location, path = result
        assert location == "Mountain"
        assert len(path) == 2
        assert path[0] == Direction.SOUTH  # Forest -> Beach
        assert path[1] == Direction.EAST   # Beach -> Mountain

        # Test resource in current location
        result = manager.find_nearest_resource("wood", "Forest")
        assert result is not None
        location, path = result
        assert location == "Forest"
        assert len(path) == 0

    def test_find_nearest_nonexistent_resource(self, manager: ResourceManagement, populated_repo: MockResourceRepository) -> None:
        """Test finding nearest location with non-existent resource."""
        result = manager.find_nearest_resource("gold", "Forest")
        assert result is None

    def test_find_nearest_from_nonexistent_location(self, manager: ResourceManagement, populated_repo: MockResourceRepository) -> None:
        """Test finding nearest resource from non-existent location."""
        result = manager.find_nearest_resource("wood", "NonExistent")
        assert result is None

    def test_unreachable_resource(self, manager: ResourceManagement, populated_repo: MockResourceRepository) -> None:
        """Test finding path to resource in unreachable location."""
        # Add an isolated location with a unique resource
        isolated = Location("Isolated", ["diamonds"])
        populated_repo.locations["Isolated"] = isolated

        result = manager.find_nearest_resource("diamonds", "Forest")
        assert result is None
