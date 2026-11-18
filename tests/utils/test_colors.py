import pytest

from src.utils.colors import random_color


def test_random_color_within_range():
    for _ in range(100):
        color = random_color(180, 255)
        assert len(color) == 3
        assert all(180 <= channel <= 255 for channel in color)


def test_random_color_invalid_range():
    with pytest.raises(ValueError):
        random_color(200, 100)
