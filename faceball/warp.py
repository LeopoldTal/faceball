"""Warp an image to project a polygon onto a circle"""

import cv2
import numpy as np
from math import isclose, sqrt

def circle_project(point, circle):
	"""circle_project(point, circle) -> point
	Project point onto circle, preserving direction from centre
	point: (x : float, y : float)
	circle: (centre x : float, centre y : float, radius : float)"""
	point_x, point_y = point
	centre_x, centre_y, radius = circle
	
	if isclose(point_x, centre_x) and isclose(point_y, centre_y):
		return point
	
	dx, dy = point_x - centre_x, point_y - centre_y
	norm = radius / sqrt(dx**2 + dy**2)
	return centre_x + norm * dx, centre_y + norm * dy

# TODO: all this stuff wants tests but not sure how

def warp_triangle_to_circle(image, point1, point2, circle):
	"""warp_triangle_to_circle(image, point1, point2, circle) -> image with same size
	Affine warp an image to send two points onto a circle and leave the circle's centre fixed
	image: OpenCV image
	point1, point2: (x : float, y : float)
	circle: (centre x : float, centre y : float, radius : float)"""
	centre = circle[:2]
	start_triangle = np.float32((point1, point2, centre))
	end_triangle = np.float32((circle_project(point1, circle), circle_project(point2, circle), centre))
	matrix = cv2.getAffineTransform(start_triangle, end_triangle)
	
	im_width, im_height, _ = image.shape
	warped = cv2.warpAffine(image, matrix, (im_height, im_width))
	
	return warped

def ints(l):
	return [ int(x) for x in l ]

def angular_mask(src_image, dst_image, point1, point2, centre):
	"""angular_mask(src_image, dst_image, point1, point2, centre) -> None
	Replace an angular region of dst_image with the contents of src_image
	The region is a wedge, where centre defines the tip; point1 and point2 define the two directions.
	src_image, dst_image: OpenCV images
	point1, point2, centre: (x : float, y : float)"""
	im_width, im_height, _ = dst_image.shape
	big_circle = centre + (im_width + im_height,)
	distant1 = ints(circle_project(point1, big_circle))
	distant2 = ints(circle_project(point2, big_circle))
	
	vertices = np.array([centre, distant1, distant2], np.int32)
	points = [vertices.reshape((-1, 1, 2))]
	
	mask = np.zeros((im_width, im_height), np.uint8)
	mask = cv2.fillPoly(mask, points, color = 255)
	
	dst_image[mask == 255] = src_image[mask == 255]

def warp_poly_to_circle(image, poly_points, circle):
	"""warp_poly_to_circle(image, poly_points, circle) -> image with same size
	Piecewise affine warp an image, sending the polygon defined by poly_points onto a circle
	image: OpenCV image
	poly_points: list of (x : float, y : float)
	circle: (centre x : float, centre y : float, radius : float)"""
	centre = circle[0], circle[1]
	warped = np.zeros(image.shape, np.uint8)
	for ii, cur_point in enumerate(poly_points):
		next_point = poly_points[(ii + 1) % len(poly_points)]
		warped_piece = warp_triangle_to_circle(image, cur_point, next_point, circle)
		angular_mask(warped_piece, warped, cur_point, next_point, centre)
	return warped
