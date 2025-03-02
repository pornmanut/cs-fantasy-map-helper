import json
import os
from datetime import datetime
from typing import Optional
from ...domain.entities.location import Location
from ...domain.entities.direction import Direction
from ...application.interfaces.map_repository import MapRepository

class JsonMapRepository(MapRepository):
    """Implementation of MapRepository using JSON file storage."""

    def save_map(self, filename: str, locations: dict[str, Location], current_location: Optional[str]) -> None:
        """Save the map state to a JSON file."""
        data = {
            "locations": {
                name: {
                    "name": loc.name,
                    "resources": loc.resources,
                    "connections": {d.value: loc_name for d, loc_name in loc.connections.items()}
                }
                for name, loc in locations.items()
            },
            "current_location": current_location
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_map(self, filename: str) -> tuple[dict[str, Location], Optional[str]]:
        """Load map state from a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        locations: dict[str, Location] = {}
        
        # First pass: Create all locations with their resources
        for name, loc_data in data["locations"].items():
            location = Location(name, loc_data["resources"])
            locations[name] = location

        # Second pass: Set up connections
        for name, loc_data in data["locations"].items():
            location = locations[name]
            for direction_str, target in loc_data["connections"].items():
                direction = Direction(direction_str)
                location.add_connection(direction, target)

        current_location = data.get("current_location")
        return locations, current_location

    def list_available_maps(self) -> list[tuple[str, float, str]]:
        """List all available JSON map files in the current directory."""
        map_files = []
        for filename in os.listdir('.'):
            if filename.endswith('.json'):
                stats = os.stat(filename)
                size_kb = stats.st_size / 1024
                modified_time = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                map_files.append((filename, size_kb, modified_time))
        return map_files
