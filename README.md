# Card Survival Map Navigator

A CLI tool to help players navigate and manage locations in Card Survival game. This project was primarily developed with the assistance of AI (specifically, using Anthropic's Claude).

## Features

### 📍 Location Management
- Create and manage game locations
- Set up directional connections (north, south, east, west)
- Track current location and available paths
- View detailed information about each location

### 🎯 Resource Tracking
- Add and manage resources at each location
- Find all locations containing specific resources
- Locate nearest source of any resource
- Automatic resource synchronization across locations

### 🗺️ Navigation Features
- Interactive command-line interface
- Pathfinding between locations
- Display shortest routes with step-by-step directions
- Find optimal paths to needed resources

### 💾 Data Management
- Save and load maps
- List available map files
- Support for multiple map configurations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/card-survival-map-navigator.git
cd card-survival-map-navigator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the program:
```bash
python cli.py
```

2. Create a new map or load the example map:
```bash
# Load example map
python setup_example_map.py
# Then in CLI:
load example_map.json
```

3. Basic commands:
```bash
# List all commands and categories
help

# Create a new location
add_location Forest wood,berries

# Move to a location
goto Forest

# See current location info
look

# Find nearest resource
nearest wood

# Save your map
save my_map.json
```

## Command Categories

### Navigation Commands
- `goto` - Move to a specific location
- `look` - Show current location info
- `path` - Find route to destination
- `nearest` - Find closest resource

### Location Management
- `add_location` - Create new locations
- `add_connection` - Connect locations
- `list_locations` - Show all locations

### Resource Management
- `add_resource` - Add resources to locations
- `find` - Find resource locations
- `list_resources` - Show all resources

### Map Management
- `save` - Save map to file
- `load` - Load map from file
- `list_maps` - Show available maps

## AI Contribution

This project was created with the assistance of Anthropic's Claude AI. The AI helped with:
- Initial project planning and structure
- Implementation of core features
- Command-line interface design
- Documentation and example creation
- Code organization and best practices

Human oversight and testing were used to ensure the quality and functionality of the final product.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Created with assistance from Anthropic's Claude AI
- Inspired by the Card Survival game
- Built for the Card Survival gaming community
