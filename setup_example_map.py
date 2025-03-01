#!/usr/bin/env python3
from main import GameMap, Direction

def setup_example_map(filename: str = "example_map.json") -> None:
    """Create and save an example map based on the example_map_instructions.txt"""
    game_map = GameMap()

    # 1. Create Locations with Initial Resources
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
        game_map.add_location(name, resources)

    # 2. Create Connections
    connections = [
        ("Beach", "Forest", Direction.NORTH),
        ("Beach", "Plains", Direction.EAST),
        ("Forest", "Mountain", Direction.NORTH),
        ("Forest", "Cave", Direction.WEST),
        ("Mountain", "Cave", Direction.WEST),
        ("Mountain", "Lake", Direction.EAST),
        ("Lake", "Village", Direction.SOUTH),
        ("Lake", "Plains", Direction.SOUTH),  # Changed from SOUTHWEST as that's not a valid direction
        ("Plains", "Village", Direction.NORTH),
        ("Plains", "Camp", Direction.EAST),
        ("Village", "Camp", Direction.EAST)
    ]

    for from_loc, to_loc, direction in connections:
        game_map.add_connection(from_loc, to_loc, direction)

    # 3. Add Additional Resources
    additional_resources = {
        "Forest": ["herbs", "vines"],
        "Mountain": ["coal", "gold"],
        "Cave": ["mushrooms", "water"],
        "Beach": ["driftwood", "seashells"],
        "Village": ["medicine", "tools"],
        "Lake": ["lilies", "clay"]
    }

    for location_name, resources in additional_resources.items():
        location = game_map.locations[location_name]
        for resource in resources:
            if resource not in location.resources:
                location.resources.append(resource)
                game_map.resource_locations[resource].append(location_name)

    # Save the map
    game_map.save_to_file(filename)
    print(f"Example map has been created and saved to {filename}")

if __name__ == "__main__":
    setup_example_map()
