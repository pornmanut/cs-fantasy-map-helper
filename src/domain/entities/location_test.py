import pytest
from typing import Optional
from src.domain.entities.location import Location
from src.domain.entities.direction import Direction

class TestLocation:
    """Test cases for Location class."""

    @pytest.fixture
    def empty_location(self) -> Location:
        """Create a location with no resources."""
        return Location("Empty")

    @pytest.fixture
    def forest(self) -> Location:
        """Create a forest location with initial resources."""
        return Location("Forest", ["wood", "berries"])

    @pytest.fixture
    def connected_locations(self) -> tuple[Location, Location]:
        """Create two connected locations."""
        forest = Location("Forest", ["wood"])
        beach = Location("Beach", ["sand"])
        forest.add_connection(Direction.SOUTH, beach.name)
        beach.add_connection(Direction.NORTH, forest.name)
        return forest, beach

    def test_location_creation(self, forest: Location) -> None:
        """Test basic location creation and properties."""
        assert forest.name == "Forest"
        assert "wood" in forest.resources
        assert "berries" in forest.resources
        assert len(forest.resources) == 2
        assert len(forest.connections) == 0

    def test_location_without_resources(self, empty_location: Location) -> None:
        """Test creating location without resources."""
        assert empty_location.name == "Empty"
        assert len(empty_location.resources) == 0
        assert isinstance(empty_location.resources, list)

    def test_add_resource(self, empty_location: Location) -> None:
        """Test adding resources to a location."""
        empty_location.add_resource("gold")
        assert "gold" in empty_location.resources
        assert len(empty_location.resources) == 1

        # Test adding duplicate resource
        empty_location.add_resource("gold")
        assert empty_location.resources.count("gold") == 1

    def test_remove_resource(self, forest: Location) -> None:
        """Test removing resources from a location."""
        forest.remove_resource("wood")
        assert "wood" not in forest.resources
        assert "berries" in forest.resources
        
        # Test removing non-existent resource
        forest.remove_resource("gold")  # Should not raise error
        assert len(forest.resources) == 1

    def test_add_connection(self, forest: Location) -> None:
        """Test adding connections between locations."""
        forest.add_connection(Direction.SOUTH, "Beach")
        assert Direction.SOUTH in forest.connections
        assert forest.connections[Direction.SOUTH] == "Beach"

    def test_get_connection(self, connected_locations: tuple[Location, Location]) -> None:
        """Test getting connections between locations."""
        forest, beach = connected_locations
        assert forest.get_connection(Direction.SOUTH) == beach.name
        assert beach.get_connection(Direction.NORTH) == forest.name
        
        # Test getting non-existent connection
        assert forest.get_connection(Direction.EAST) is None

    def test_has_resource(self, forest: Location) -> None:
        """Test checking for resource existence."""
        assert forest.has_resource("wood")
        assert forest.has_resource("berries")
        assert not forest.has_resource("stone")

    def test_invalid_connection(self, forest: Location) -> None:
        """Test error handling for invalid connections."""
        with pytest.raises(ValueError):
            forest.add_connection(Direction.NORTH, "")

        with pytest.raises(ValueError):
            forest.add_connection(None, "Beach")  # type: ignore

    def test_connection_overwrite(self, forest: Location) -> None:
        """Test that connections can be overwritten."""
        forest.add_connection(Direction.SOUTH, "Beach")
        forest.add_connection(Direction.SOUTH, "Plains")
        assert forest.connections[Direction.SOUTH] == "Plains"
