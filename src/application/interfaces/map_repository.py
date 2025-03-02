from abc import ABC, abstractmethod
from typing import Optional, Protocol
from ...domain.entities.location import Location
from ...domain.entities.direction import Direction

class MapRepository(Protocol):
    """Protocol defining the contract for map storage and retrieval operations."""
    
    @abstractmethod
    def save_map(self, filename: str, locations: dict[str, Location], current_location: Optional[str]) -> None:
        """Save the map state to persistent storage.
        
        Args:
            filename: Name of the file to save to
            locations: Dictionary mapping location names to Location objects
            current_location: Name of the current location, if any
        """
        ...

    @abstractmethod
    def load_map(self, filename: str) -> tuple[dict[str, Location], Optional[str]]:
        """Load map state from persistent storage.
        
        Args:
            filename: Name of the file to load from
            
        Returns:
            Tuple containing:
            - Dictionary mapping location names to Location objects
            - Name of the current location (if any)
        """
        ...

    @abstractmethod
    def list_available_maps(self) -> list[tuple[str, float, str]]:
        """List all available map files.
        
        Returns:
            List of tuples containing:
            - Filename
            - File size in KB
            - Last modified timestamp
        """
        ...
