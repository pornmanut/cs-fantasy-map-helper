import pytest
from src.domain.entities.direction import Direction

class TestDirection:
    """Test cases for Direction enum."""
    
    def test_direction_values(self) -> None:
        """Test that direction values are correct."""
        assert Direction.NORTH.value == "north"
        assert Direction.SOUTH.value == "south"
        assert Direction.EAST.value == "east"
        assert Direction.WEST.value == "west"

    def test_get_opposite(self) -> None:
        """Test getting opposite directions."""
        assert Direction.get_opposite(Direction.NORTH) == Direction.SOUTH
        assert Direction.get_opposite(Direction.SOUTH) == Direction.NORTH
        assert Direction.get_opposite(Direction.EAST) == Direction.WEST
        assert Direction.get_opposite(Direction.WEST) == Direction.EAST

    def test_all_directions_have_opposites(self) -> None:
        """Test that every direction has an opposite."""
        for direction in Direction:
            opposite = Direction.get_opposite(direction)
            assert isinstance(opposite, Direction)
            assert Direction.get_opposite(opposite) == direction

    def test_direction_from_string(self) -> None:
        """Test creating Direction from string values."""
        assert Direction("north") == Direction.NORTH
        assert Direction("south") == Direction.SOUTH
        assert Direction("east") == Direction.EAST
        assert Direction("west") == Direction.WEST

    def test_invalid_direction(self) -> None:
        """Test that invalid direction values raise ValueError."""
        with pytest.raises(ValueError):
            Direction("invalid")
        with pytest.raises(ValueError):
            Direction("up")
