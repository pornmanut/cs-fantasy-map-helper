from typing import Optional, Protocol, Tuple
from ...domain.entities.location import Location
from ...application.interfaces.map_repository import MapRepository

class LocationProvider(Protocol):
    """Protocol for accessing location data."""
    def list_locations(self) -> dict[str, Location]: ...
    def get_current_location(self) -> Optional[str]: ...
    def set_current_location(self, location_name: Optional[str]) -> None: ...
    def clear_locations(self) -> None: ...
    def add_location(self, location: Location) -> None: ...
    def add_connection(self, from_loc: str, to_loc: str, direction: str) -> None: ...

class MapManagement:
    """Use case for managing map persistence."""

    def __init__(self, map_repository: MapRepository, location_provider: LocationProvider):
        self._repository = map_repository
        self._location_provider = location_provider

    def save_map(self, filename: str) -> None:
        """Save the current map state to a file."""
        locations = self._location_provider.list_locations()
        current_location = self._location_provider.get_current_location()
        
        try:
            self._repository.save_map(filename, locations, current_location)
        except Exception as e:
            raise RuntimeError(f"Failed to save map: {str(e)}") from e

    def load_map(self, filename: str) -> None:
        """Load a map state from a file."""
        try:
            locations, current_location = self._repository.load_map(filename)
            
            # Clear existing state
            self._location_provider.clear_locations()
            
            # Restore loaded state
            for location in locations.values():
                self._location_provider.add_location(location)
            
            # Set current location
            self._location_provider.set_current_location(current_location)
            
        except Exception as e:
            raise RuntimeError(f"Failed to load map: {str(e)}") from e

    def list_available_maps(self) -> list[tuple[str, float, str]]:
        """List all available map files."""
        try:
            return self._repository.list_available_maps()
        except Exception as e:
            raise RuntimeError(f"Failed to list maps: {str(e)}") from e
