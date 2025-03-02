from dataclasses import dataclass
from typing import Optional
from .direction import Direction

@dataclass
class Location:
    """A location in the game world with resources and connections to other locations."""
    name: str
    resources: list[str]
    connections: dict[Direction, str]  # Direction -> Location name

    def __init__(self, name: str, resources: Optional[list[str]] = None) -> None:
        """Initialize a location with a name and optional resources."""
        self.name = name
        self.resources = resources or []
        self.connections = {}

    def add_resource(self, resource: str) -> None:
        """Add a resource to the location if it doesn't already exist."""
        if resource not in self.resources:
            self.resources.append(resource)

    def remove_resource(self, resource: str) -> None:
        """Remove a resource from the location if it exists."""
        if resource in self.resources:
            self.resources.remove(resource)

    def add_connection(self, direction: Direction, target_location: str) -> None:
        """Add a directional connection to another location."""
        if not direction or not target_location:
            raise ValueError("Direction and target location must be provided")
        self.connections[direction] = target_location

    def get_connection(self, direction: Direction) -> Optional[str]:
        """Get the connected location in the specified direction."""
        return self.connections.get(direction)

    def has_resource(self, resource: str) -> bool:
        """Check if the location has a specific resource."""
        return resource in self.resources
