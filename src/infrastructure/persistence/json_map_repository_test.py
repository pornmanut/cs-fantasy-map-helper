import pytest
import os
import json
from typing import Optional
from datetime import datetime
from src.domain.entities.location import Location
from src.domain.entities.direction import Direction
from src.infrastructure.persistence.json_map_repository import JsonMapRepository

class TestJsonMapRepository:
    """Test cases for JsonMapRepository."""

    @pytest.fixture
    def repo(self, tmp_path) -> JsonMapRepository:
        """Create a repository instance using temporary directory."""
        # Change to temp directory for file operations
        os.chdir(tmp_path)
        return JsonMapRepository()

    @pytest.fixture
    def sample_locations(self) -> dict[str, Location]:
        """Create sample locations for testing."""
        forest = Location("Forest", ["wood", "berries"])
        beach = Location("Beach", ["sand"])
        forest.add_connection(Direction.SOUTH, beach.name)
        beach.add_connection(Direction.NORTH, forest.name)
        
        return {
            forest.name: forest,
            beach.name: beach
        }

    def test_save_map(self, repo: JsonMapRepository, sample_locations: dict[str, Location], tmp_path) -> None:
        """Test saving map to JSON file."""
        filename = "test_map.json"
        current_location = "Forest"
        
        repo.save_map(filename, sample_locations, current_location)
        
        # Verify file exists
        assert os.path.exists(filename)
        
        # Verify file content
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "locations" in data
        assert "current_location" in data
        assert data["current_location"] == current_location
        assert "Forest" in data["locations"]
        assert "Beach" in data["locations"]
        
        # Verify location data
        forest_data = data["locations"]["Forest"]
        assert forest_data["name"] == "Forest"
        assert "wood" in forest_data["resources"]
        assert "berries" in forest_data["resources"]
        assert forest_data["connections"]["south"] == "Beach"

    def test_load_map(self, repo: JsonMapRepository, sample_locations: dict[str, Location], tmp_path) -> None:
        """Test loading map from JSON file."""
        filename = "test_map.json"
        current_location = "Forest"
        
        # Save map first
        repo.save_map(filename, sample_locations, current_location)
        
        # Load map
        loaded_locations, loaded_current = repo.load_map(filename)
        
        # Verify loaded data
        assert loaded_current == current_location
        assert len(loaded_locations) == len(sample_locations)
        
        # Verify location data
        forest = loaded_locations["Forest"]
        assert forest.name == "Forest"
        assert "wood" in forest.resources
        assert "berries" in forest.resources
        assert forest.get_connection(Direction.SOUTH) == "Beach"
        
        beach = loaded_locations["Beach"]
        assert beach.name == "Beach"
        assert "sand" in beach.resources
        assert beach.get_connection(Direction.NORTH) == "Forest"

    def test_load_nonexistent_map(self, repo: JsonMapRepository) -> None:
        """Test error handling when loading non-existent file."""
        with pytest.raises(FileNotFoundError):
            repo.load_map("nonexistent.json")

    def test_load_invalid_json(self, repo: JsonMapRepository, tmp_path) -> None:
        """Test error handling when loading invalid JSON file."""
        # Create invalid JSON file
        filename = "invalid.json"
        with open(filename, 'w') as f:
            f.write("invalid json content")
        
        with pytest.raises(json.JSONDecodeError):
            repo.load_map(filename)

    def test_list_available_maps(self, repo: JsonMapRepository, sample_locations: dict[str, Location], tmp_path) -> None:
        """Test listing available map files."""
        # Create some map files
        repo.save_map("map1.json", sample_locations, "Forest")
        repo.save_map("map2.json", sample_locations, "Beach")
        
        # Create some non-JSON files
        with open("not_a_map.txt", 'w') as f:
            f.write("not a map file")
        
        maps = repo.list_available_maps()
        
        # Should only list JSON files
        assert len(maps) == 2
        assert any(name == "map1.json" for name, _, _ in maps)
        assert any(name == "map2.json" for name, _, _ in maps)
        
        # Check file info format
        for name, size, modified in maps:
            assert isinstance(name, str)
            assert isinstance(size, float)
            assert isinstance(modified, str)
            # Try parsing the date string
            datetime.strptime(modified, '%Y-%m-%d %H:%M:%S')

    def test_save_map_without_current_location(self, repo: JsonMapRepository, 
                                             sample_locations: dict[str, Location]) -> None:
        """Test saving map without current location."""
        filename = "test_map.json"
        repo.save_map(filename, sample_locations, None)
        
        loaded_locations, loaded_current = repo.load_map(filename)
        assert loaded_current is None
        assert len(loaded_locations) == len(sample_locations)
