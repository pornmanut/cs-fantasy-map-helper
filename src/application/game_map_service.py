from typing import Optional, Protocol
from collections import defaultdict
from ..domain.entities.location import Location
from ..domain.entities.direction import Direction
from .interfaces.map_repository import MapRepository
from .usecases.location_management import LocationManagement, LocationRepository
from .usecases.resource_management import ResourceManagement, ResourceRepository
from .usecases.map_management import MapManagement, LocationProvider

class GameMapService(LocationRepository, ResourceRepository, LocationProvider):
    """Service that coordinates all map-related operations."""

    def __init__(self, map_repository: MapRepository):
        self.locations: dict[str, Location] = {}
        self.resource_locations: dict[str, list[str]] = defaultdict(list)
        self.current_location: Optional[str] = None
        
        # Initialize use cases
        self.location_management = LocationManagement(self)
        self.resource_management = ResourceManagement(self)
        self.map_management = MapManagement(map_repository, self)

    # LocationRepository implementation
    def add_location(self, location: Location) -> None:
        self.locations[location.name] = location
        for resource in location.resources:
            self.resource_locations[resource].append(location.name)

    def get_location(self, name: str) -> Optional[Location]:
        return self.locations.get(name)

    def update_location(self, location: Location) -> None:
        self.locations[location.name] = location

    def list_locations(self) -> dict[str, Location]:
        return self.locations

    # LocationProvider implementation
    def get_current_location(self) -> Optional[str]:
        return self.current_location

    def set_current_location(self, location_name: Optional[str]) -> None:
        self.current_location = location_name

    def clear_locations(self) -> None:
        self.locations.clear()
        self.resource_locations.clear()
        self.current_location = None

    def add_connection(self, from_loc: str, to_loc: str, direction: str) -> None:
        direction_enum = Direction(direction.lower())
        self.location_management.add_connection(from_loc, to_loc, direction_enum)

    # High-level operations
    def create_location(self, name: str, resources: Optional[list[str]] = None) -> None:
        """Create a new location with optional resources."""
        self.location_management.add_location(name, resources)

    def add_resource_to_location(self, location_name: str, resource: str) -> None:
        """Add a resource to an existing location."""
        self.resource_management.add_resource(location_name, resource)

    def find_path_to_resource(self, resource: str) -> Optional[tuple[str, list[Direction]]]:
        """Find the nearest location with a specific resource from current location."""
        if not self.current_location:
            raise ValueError("No current location set")
        return self.resource_management.find_nearest_resource(resource, self.current_location)

    def get_location_info(self, location_name: str) -> dict:
        """Get detailed information about a location."""
        location = self.get_location(location_name)
        if not location:
            raise ValueError(f"Location {location_name} does not exist")
            
        return {
            "name": location.name,
            "resources": location.resources,
            "connections": {d.value: loc for d, loc in location.connections.items()}
        }

    # Map management operations
    def save_map_to_file(self, filename: str) -> None:
        """Save the current map state to a file."""
        self.map_management.save_map(filename)

    def load_map_from_file(self, filename: str) -> None:
        """Load a map state from a file."""
        self.map_management.load_map(filename)

    def get_available_maps(self) -> list[tuple[str, float, str]]:
        """List all available map files."""
        return self.map_management.list_available_maps()
