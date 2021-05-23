import pytest
from faceball.image_saver import get_rgb

COLOURS = [
	(None, (54, 57, 63)),
	('discord', (54, 57, 63)),
	('white', (255, 255, 255)),
	('black', (0, 0, 0)),
	('BLACK', (0, 0, 0)),
	('1,128,42', (1, 128, 42)),
	('ff0042', (255, 0, 66))
]

@pytest.mark.parametrize('name,expected', COLOURS)
def test_get_rgb(name, expected):
	assert get_rgb(name) == expected
