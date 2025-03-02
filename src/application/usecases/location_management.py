from typing import Optional, Protocol
from ...domain.entities.location import Location
from ...domain.entities.direction import Direction

class LocationRepository(Protocol):
    """Protocol for location storage operations."""
    def add_location(self, location: Location) -> None: ...
    def get_location(self, name: str) -> Optional[Location]: ...
    def update_location(self, location: Location) -> None: ...
    def list_locations(self) -> dict[str, Location]: ...

class LocationManagement:
    """Use case for managing locations and their connections."""

    def __init__(self, location_repository: LocationRepository):
        self._repository = location_repository
        self._current_location: Optional[str] = None

    def add_location(self, name: str, resources: Optional[list[str]] = None) -> None:
        """Add a new location with optional resources."""
        if self._repository.get_location(name):
            raise ValueError(f"Location {name} already exists")
        
        location = Location(name, resources)
        self._repository.add_location(location)

    def add_connection(self, from_loc: str, to_loc: str, direction: Direction) -> None:
        """Add a bidirectional connection between two locations."""
        source = self._repository.get_location(from_loc)
        target = self._repository.get_location(to_loc)

        if not source or not target:
            raise ValueError("One or both locations do not exist")

        # Add connection in specified direction
        source.add_connection(direction, to_loc)
        self._repository.update_location(source)

        # Add reciprocal connection
        opposite = Direction.get_opposite(direction)
        target.add_connection(opposite, from_loc)
        self._repository.update_location(target)

    def get_current_location(self) -> Optional[Location]:
        """Get the current location if one is set."""
        if not self._current_location:
            return None
        return self._repository.get_location(self._current_location)

    def set_current_location(self, location_name: str) -> None:
        """Set the current location."""
        if not self._repository.get_location(location_name):
            raise ValueError(f"Location {location_name} does not exist")
        self._current_location = location_name

    def get_connected_locations(self, location_name: str) -> dict[Direction, str]:
        """Get all locations connected to the specified location."""
        location = self._repository.get_location(location_name)
        if not location:
            raise ValueError(f"Location {location_name} does not exist")
        return location.connections

    def list_locations(self) -> dict[str, Location]:
        """Get all available locations."""
        return self._repository.list_locations()

    def location_exists(self, name: str) -> bool:
        """Check if a location exists."""
        return self._repository.get_location(name) is not None
