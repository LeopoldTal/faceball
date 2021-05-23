from math import cos, sin, pi
from pytest import approx
from faceball.warp import circle_project

class TestCircleProject:
	def test_centre_stays_fixed(self):
		circle = 42, 23, 17
		point = 42, 23
		assert circle_project(point, circle) == (42, 23)
	
	def test_on_circle_stays_fixed(self):
		circle = 100, 100, 10
		point = 100 + 10 * cos(pi / 3), 100 - 10 * sin(pi / 3)
		assert circle_project(point, circle) == approx(point)
	
	def test_projected_along_x(self):
		circle = 0, 0, 10
		point = 5, 0
		assert circle_project(point, circle) == (10, 0)
	
	def test_projected_along_y(self):
		circle = 1, 2, 10
		point = 1, 3
		assert circle_project(point, circle) == (1, 12)
	
	def test_projected_backwards_along_x(self):
		circle = 10, 10, 10
		point = -50, 10
		assert circle_project(point, circle) == (0, 10)
	
	def test_projected_outwards_at_angle(self):
		circle = 0, 0, 1
		point = 0.4 * cos(pi / 6), 0.4 * sin(pi / 6)
		expected = cos(pi / 6), sin(pi / 6)
		assert circle_project(point, circle) == approx(expected)
	
	def test_projected_inwards_at_angle(self):
		circle = 3, -2, 7
		point = 3 + 42 * cos(pi / 4), -2 + 42 * sin(pi / 4)
		expected = 3 + 7*cos(pi / 4), -2 + 7*sin(pi / 4)
		assert circle_project(point, circle) == approx(expected)
