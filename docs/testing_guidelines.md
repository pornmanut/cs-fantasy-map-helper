# Testing Guidelines

## Test File Structure
- Test files should be placed in the same directory as the code they test
- Name test files as `{module_name}_test.py` (e.g., `location_test.py` for `location.py`)
- Use pytest as the testing framework
- Group related tests into classes named `Test{ComponentName}`

## Test Organization

### Example Test Structure
```python
import pytest
from typing import Optional
from .location import Location

class TestLocation:
    @pytest.fixture
    def sample_location(self) -> Location:
        """Fixture providing a basic location for testing."""
        return Location("Forest", ["wood", "berries"])

    def test_location_creation(self, sample_location: Location) -> None:
        """Test basic location creation and properties."""
        assert sample_location.name == "Forest"
        assert "wood" in sample_location.resources
        assert len(sample_location.connections) == 0

    def test_add_resource(self, sample_location: Location) -> None:
        """Test adding resources to a location."""
        sample_location.add_resource("mushrooms")
        assert "mushrooms" in sample_location.resources
        # Test duplicate addition
        sample_location.add_resource("mushrooms")
        assert sample_location.resources.count("mushrooms") == 1

    def test_invalid_operations(self, sample_location: Location) -> None:
        """Test error handling."""
        with pytest.raises(ValueError):
            sample_location.add_connection(None, "North")
```

## Test Categories

### 1. Unit Tests
- Test individual components in isolation
- Mock dependencies using pytest fixtures
- Focus on single responsibility
- Test both success and failure cases

### 2. Integration Tests
- Test component interactions
- Use actual implementations instead of mocks
- Verify use case workflows
- Test data persistence

### 3. Functional Tests
- Test complete features
- Use CLI interface
- Verify user workflows
- Test data consistency

## Best Practices

### 1. Fixture Usage
```python
@pytest.fixture
def game_map_service() -> GameMapService:
    """Create a fresh GameMapService for testing."""
    repository = JsonMapRepository()
    return GameMapService(repository)

@pytest.fixture
def populated_map(game_map_service: GameMapService) -> GameMapService:
    """Create a GameMapService with sample data."""
    game_map_service.create_location("Forest", ["wood"])
    game_map_service.create_location("Beach", ["sand"])
    game_map_service.add_connection("Forest", "Beach", "south")
    return game_map_service
```

### 2. Error Testing
```python
def test_resource_not_found(populated_map: GameMapService) -> None:
    """Test handling of non-existent resources."""
    result = populated_map.find_resource("gold")
    assert result == []

def test_invalid_connection(populated_map: GameMapService) -> None:
    """Test invalid connection attempts."""
    with pytest.raises(ValueError):
        populated_map.add_connection("Forest", "NonExistent", "north")
```

### 3. Test Independence
- Each test should be independent
- Clean up any modifications after tests
- Don't rely on test execution order
- Use fresh fixtures for each test

## Command Testing

### Example CLI Command Test
```python
class TestLocationCommands:
    def test_add_location(self, cli: GameCLI) -> None:
        """Test adding a new location via CLI."""
        result = cli.onecmd("add_location Forest wood,berries")
        assert "added successfully" in cli.last_output
        assert "Forest" in cli.game_map.list_locations()

    def test_navigation(self, cli: GameCLI) -> None:
        """Test navigation between locations."""
        cli.onecmd("add_location Forest")
        cli.onecmd("goto Forest")
        assert cli.game_map.get_current_location() == "Forest"
```

## Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest src/domain/entities/location_test.py

# Run specific test class
pytest src/domain/entities/location_test.py::TestLocation

# Run with coverage report
pytest --cov=src

# Run with verbose output
pytest -v
```

## Coverage Goals
- Aim for minimum 80% code coverage
- Focus on core business logic
- Include error handling paths
- Test edge cases and boundary conditions
