# Card Survival Map Navigator

A CLI tool to help players navigate and manage locations in Card Survival game. This project was primarily developed with the assistance of AI (specifically, using Anthropic's Claude).

## Why This Tool?

Card Survival is a game of exploration and discovery, where uncovering new locations and resources is a key part of the experience. This tool was created to enhance that experience by:

- Letting you document your own journey without spoilers
- Helping you remember locations and resources you've personally discovered
- Creating your own personalized map as you explore the game world
- Maintaining the excitement of discovery while having a reliable way to track your findings

Instead of looking up complete maps online that might spoil the game, this tool lets you build your knowledge gradually. As you explore in-game, you can:

1. Add new locations as you discover them
2. Note down resources you find at each location
3. Track connections between areas you've explored
4. Find your way back to resources you've previously discovered

## Features

- 📍 **Location Management**: Create, manage, and connect game locations
- 🎯 **Resource Tracking**: Track and find resources across locations
- 🗺️ **Navigation**: Interactive CLI with pathfinding between locations
- 💾 **Data Management**: Save, load, and manage multiple map configurations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pornmanut/card-survival-map-navigator.git
cd card-survival-map-navigator
```

2. Install the package in development mode:
```bash
# Install with all development dependencies
pip install -e ".[dev]"

# Or install only runtime dependencies
pip install -e .
```

## Usage

1. Start the program:
```bash
card-survival-map
```

2. Create a new map or load the example map:
```bash
# Create example map
python -m src.infrastructure.cli.example_setup

# Then in CLI:
load example_map.json
```

3. Basic commands:
```bash
help                 # List all commands
add_location        # Create a new location
goto               # Move to a location
look               # See current location info
nearest            # Find nearest resource
find               # Find resource locations
path               # Find path to location
save               # Save your map
```

## Command Reference

### Navigation Commands
```
goto <location>      Move to a specific location
look                 Show information about current location
path <dest>         Find path to target location
nearest <resource>   Find nearest location with specified resource
```

### Location Management Commands
```
add_location <name> [resource1,resource2,...]   Create a new location
add_connection <from> <to> <direction>          Connect two locations
list_locations                                  Show all locations and details
```

### Resource Management Commands
```
add_resource <location> <resource1,resource2,...>   Add resources to location
find <resource>                                     Find all locations with resource
list_resources                                      Show all resources and locations
```

### Map Management Commands
```
save [filename]      Save current map to file (default: map_data.json)
load <filename>      Load map from file
list_maps           Show available map files
```

## Project Structure

The project follows Clean Architecture principles with clear separation of concerns:

```
cs-fantasy-map-helper/
├── src/
│   ├── domain/          # Business entities
│   ├── application/     # Business logic & use cases
│   └── infrastructure/  # CLI & persistence
├── pyproject.toml
└── requirements.txt
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
