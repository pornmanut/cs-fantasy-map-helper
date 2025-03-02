"""Script to set up an example map for demonstration purposes."""

from typing import Optional
from ...application.game_map_service import GameMapService
from ...infrastructure.persistence.json_map_repository import JsonMapRepository
from ...domain.entities.direction import Direction

def setup_example_map(filename: str = "example_map.json") -> None:
    """Create and save an example map with locations and connections."""
    # Initialize services
    repository = JsonMapRepository()
    game_map = GameMapService(repository)

    # Create locations with initial resources
    locations = {
        "Beach": ["sand", "shells", "coconuts"],
        "Forest": ["wood", "berries", "mushrooms"],
        "Mountain": ["stone", "iron", "crystals"],
        "Cave": ["gems", "iron", "stone"],
        "Lake": ["fish", "water", "reeds"],
        "Camp": ["wood", "water", "tools"],
        "Plains": ["herbs", "grass", "flowers"],
        "Village": ["tools", "food", "water"]
    }

    for name, resources in locations.items():
        game_map.create_location(name, resources)

    # Create connections between locations
    connections = [
        ("Beach", "Forest", Direction.NORTH),
        ("Beach", "Plains", Direction.EAST),
        ("Forest", "Mountain", Direction.NORTH),
        ("Forest", "Cave", Direction.WEST),
        ("Mountain", "Cave", Direction.WEST),
        ("Mountain", "Lake", Direction.EAST),
        ("Lake", "Village", Direction.SOUTH),
        ("Lake", "Plains", Direction.SOUTH),
        ("Plains", "Village", Direction.NORTH),
        ("Plains", "Camp", Direction.EAST),
        ("Village", "Camp", Direction.EAST)
    ]

    for from_loc, to_loc, direction in connections:
        game_map.location_management.add_connection(from_loc, to_loc, direction)

    # Add additional resources to existing locations
    additional_resources = {
        "Forest": ["herbs", "vines"],
        "Mountain": ["coal", "gold"],
        "Cave": ["mushrooms", "water"],
        "Beach": ["driftwood", "seashells"],
        "Village": ["medicine", "tools"],
        "Lake": ["lilies", "clay"]
    }

    for location_name, resources in additional_resources.items():
        for resource in resources:
            game_map.add_resource_to_location(location_name, resource)

    # Save the map
    game_map.save_map_to_file(filename)
    print(f"Example map has been created and saved to {filename}")

if __name__ == "__main__":
    setup_example_map()
