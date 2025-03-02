from typing import Optional, Protocol
from collections import defaultdict
import heapq
from ...domain.entities.location import Location
from ...domain.entities.direction import Direction

class ResourceRepository(Protocol):
    """Protocol for resource tracking operations."""
    def get_location(self, name: str) -> Optional[Location]: ...
    def list_locations(self) -> dict[str, Location]: ...
    def update_location(self, location: Location) -> None: ...

class ResourceManagement:
    """Use case for managing resources and finding paths to resources."""

    def __init__(self, resource_repository: ResourceRepository):
        self._repository = resource_repository
        self._resource_locations: dict[str, list[str]] = defaultdict(list)

    def add_resource(self, location_name: str, resource: str) -> None:
        """Add a resource to a location."""
        location = self._repository.get_location(location_name)
        if not location:
            raise ValueError(f"Location {location_name} does not exist")

        if resource not in location.resources:
            location.add_resource(resource)
            self._resource_locations[resource].append(location_name)
            self._repository.update_location(location)

    def find_resource(self, resource: str) -> list[str]:
        """Find all locations containing a specific resource."""
        locations = []
        for loc_name, location in self._repository.list_locations().items():
            if resource in location.resources:
                locations.append(loc_name)
        return locations

    def find_path(self, start: str, end: str) -> Optional[list[Direction]]:
        """Find shortest path between two locations using Dijkstra's algorithm."""
        if not start or not end:
            return None

        locations = self._repository.list_locations()
        if start not in locations or end not in locations:
            return None

        distances: dict[str, float] = {loc: float('inf') for loc in locations}
        distances[start] = 0
        previous: dict[str, Optional[str]] = {loc: None for loc in locations}
        path_directions: dict[str, Optional[Direction]] = {loc: None for loc in locations}
        pq = [(0, start)]
        visited = set()

        while pq:
            current_distance, current = heapq.heappop(pq)

            if current == end:
                # Reconstruct path
                path = []
                while current != start:
                    if current is None or previous[current] is None:
                        return None
                    if path_directions[current] is not None:
                        path.append(path_directions[current])
                    current = previous[current]
                return list(reversed(path))

            if current in visited:
                continue
            
            visited.add(current)
            location = locations[current]

            for direction, neighbor in location.connections.items():
                if neighbor in visited:
                    continue
                
                distance = current_distance + 1
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    path_directions[neighbor] = direction
                    heapq.heappush(pq, (distance, neighbor))

        return None

    def find_nearest_resource(self, resource: str, start: str) -> Optional[tuple[str, list[Direction]]]:
        """Find nearest location containing the specified resource and path to it."""
        if not start:
            return None
            
        locations_with_resource = self.find_resource(resource)
        if not locations_with_resource:
            return None

        # Check if current location has the resource
        if start in locations_with_resource:
            return (start, [])

        shortest_path = None
        nearest_location = None
        shortest_length = float('inf')

        for location in locations_with_resource:
            path = self.find_path(start, location)
            if path and len(path) < shortest_length:
                shortest_path = path
                nearest_location = location
                shortest_length = len(path)

        if nearest_location is None or shortest_path is None:
            return None
            
        return (nearest_location, shortest_path)
