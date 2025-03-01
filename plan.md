# Card Survival Fantasy Map Helper CLI Program Specification

## Game Overview
The CLI tool will assist players in navigating a complex game map where:
- Locations are connected via directional paths (north, west, south, east)
- Path availability is restricted by environmental factors (mountains, rivers, etc.)
- Resources are location-specific and collectible

## Core Requirements

### 1. Location Management
- Display current location's:
  - Available resources
  - Accessible routes with direction labels
  - Connected locations through valid paths
- Path navigation maintains directional reciprocity (e.g., north path to location B implies south return path to A)

### 2. Resource System
- Track resource availability per location
- Automatic resource synchronization:
  - Adding resource to location removes it from others
  - Updating resource propagates changes to all instances

### 3. Search & Navigation
- Resource search: Show all locations containing specified resource
- Pathfinding:
  - Calculate shortest path between current location and target
  - Display step count and directional instructions
  - Find nearest location with specified resource + optimal path

### 4. Management Features
CRUD operations for game elements:
- **Locations**:
  - Add/Remove locations
  - Update existing locations
  - Initial resource assignment during creation

- **Routes**:
  - Create/Delete directional paths
  - Modify existing connections
  - Validate path reciprocity

- **Resources**:
  - Add/Remove resources
  - Update resource properties
  - Bulk management operations

## Technical Specifications
- **Language**: Python 3.10+
- **Data Structures**:
  - Graph-based location system
  - Directional adjacency lists
  - Resource-location mapping
- **CLI Features**:
  - Interactive menu system
  - Color-coded output
  - Persistent data storage (JSON/YAML)
