import numpy as np
from faceball.hull import barycentre, convex_hull

class TestHull:
	def test_already_convex(self):
		points = np.array([(0, 0), (1, 0), (1, 1), (0, 1)])
		assert np.all(convex_hull(points) == points)
	
	def test_removes_inner(self):
		points = np.array([(0, 0), (0, 1), (1, 0), (1, 1), (.5, .5)])
		expected = np.array([(0, 0), (1, 0), (1, 1), (0, 1)])
		assert np.all(convex_hull(points) == expected)

class TestBarycentre:
	def test_barycentre(self):
		points = np.array([(0, 0), (2, 0), (2, 4), (0, 4)])
		expected = 1, 2
		assert barycentre(points) == expected
	
	def test_rounds(self):
		points = np.array([(0, 0), (2, 0), (1.9, 1.1), (0, 1)])
		expected = 1, 1
		assert barycentre(points) == expected
