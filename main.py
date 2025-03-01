from typing import Dict, List, Optional, Tuple
import json
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import heapq

class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

    @staticmethod
    def get_opposite(direction: 'Direction') -> 'Direction':
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST
        }
        return opposites[direction]

@dataclass
class Location:
    name: str
    resources: List[str]
    connections: Dict[Direction, str]  # Direction -> Location name

class GameMap:
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.resource_locations: Dict[str, List[str]] = defaultdict(list)
        self.current_location: Optional[str] = None

    def add_location(self, name: str, resources: Optional[List[str]] = None) -> None:
        """Add a new location to the map"""
        if name in self.locations:
            raise ValueError(f"Location {name} already exists")
        
        resources_list = resources if resources is not None else []
        self.locations[name] = Location(name, resources_list, {})
        
        # Update resource tracking
        for resource in resources_list:
            self.resource_locations[resource].append(name)

    def add_connection(self, from_loc: str, to_loc: str, direction: Direction) -> None:
        """Add a directional connection between locations"""
        if from_loc not in self.locations or to_loc not in self.locations:
            raise ValueError("One or both locations do not exist")
        
        # Add connection in specified direction
        if from_loc in self.locations and direction not in self.locations[from_loc].connections:
            self.locations[from_loc].connections[direction] = to_loc
            # Add reciprocal connection
            opposite_direction = Direction.get_opposite(direction)
            if to_loc in self.locations and opposite_direction not in self.locations[to_loc].connections:
                self.locations[to_loc].connections[opposite_direction] = from_loc

    def find_path(self, start: str, end: str) -> Optional[List[Direction]]:
        """Find shortest path between two locations using Dijkstra's algorithm"""
        if not start or not end or start not in self.locations or end not in self.locations:
            return None

        distances: Dict[str, float] = {loc: float('inf') for loc in self.locations}
        distances[start] = 0
        previous: Dict[str, Optional[str]] = {loc: None for loc in self.locations}
        path_directions: Dict[str, Optional[Direction]] = {loc: None for loc in self.locations}
        pq = [(0, start)]
        visited = set()

        while pq:
            current_distance, current_location = heapq.heappop(pq)

            if current_location == end:
                # Reconstruct path
                path = []
                current = end
                while current != start:
                    if current is None or previous[current] is None:
                        return None
                    if path_directions[current] is not None:
                        path.append(path_directions[current])
                    current = previous[current]
                return list(reversed(path))

            if current_location in visited:
                continue
            
            visited.add(current_location)

            for direction, neighbor in self.locations[current_location].connections.items():
                if neighbor in visited:
                    continue
                
                distance = current_distance + 1
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_location
                    path_directions[neighbor] = direction
                    heapq.heappush(pq, (distance, neighbor))

        return None

    def find_resource(self, resource: str) -> List[str]:
        """Find all locations containing a specific resource"""
        return self.resource_locations.get(resource, [])

    def find_nearest_resource(self, resource: str, start: str) -> Optional[Tuple[str, List[Direction]]]:
        """Find nearest location containing the specified resource and path to it"""
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

    def get_current_location_info(self) -> Dict:
        """Get information about the current location"""
        if not self.current_location:
            return {}
            
        location = self.locations.get(self.current_location)
        if not location:
            return {}
            
        return {
            "name": location.name,
            "resources": location.resources,
            "connections": {d.value: loc for d, loc in location.connections.items()}
        }

    def save_to_file(self, filename: str) -> None:
        """Save the map data to a JSON file"""
        data = {
            "locations": {
                name: {
                    "name": loc.name,
                    "resources": loc.resources,
                    "connections": {d.value: loc_name for d, loc_name in loc.connections.items()}
                }
                for name, loc in self.locations.items()
            },
            "current_location": self.current_location
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filename: str) -> None:
        """Load map data from a JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)

        self.locations.clear()
        self.resource_locations.clear()

        # Load locations first
        for name, loc_data in data["locations"].items():
            self.add_location(name, loc_data["resources"])

        # Then load connections
        for name, loc_data in data["locations"].items():
            for direction_str, target in loc_data["connections"].items():
                direction = Direction(direction_str)
                # Only add connection if it doesn't exist yet
                if direction not in self.locations[name].connections:
                    self.add_connection(name, target, direction)

        self.current_location = data.get("current_location")

def main():
    game_map = GameMap()
    
    # Example usage:
    game_map.add_location("Forest", ["wood", "berries"])
    game_map.add_location("Beach", ["sand", "shells"])
    game_map.add_location("Mountain", ["stone", "iron"])
    
    game_map.add_connection("Forest", "Beach", Direction.SOUTH)
    game_map.add_connection("Beach", "Mountain", Direction.EAST)
    
    # Save the map
    game_map.save_to_file("map_data.json")
    
    # Find path from Forest to Mountain
    path = game_map.find_path("Forest", "Mountain")
    if path:
        print(f"Path to Mountain: {[d.value for d in path]}")
    
    # Find locations with wood
    wood_locations = game_map.find_resource("wood")
    print(f"Wood can be found in: {wood_locations}")

if __name__ == "__main__":
    main()
