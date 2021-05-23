"""Convex hull, barycentre, mean circle of points"""

import numpy as np
from math import sqrt

def convex_hull(points):
	"""convex_hull(points : 2D np.array with 2 cols) -> 2D np.array with 2 cols
	Convex hull of a list of points on the plane"""
	start_point = min(list(points), key = lambda point: point[0])
	
	current_point = start_point
	current_dir = np.array([ 0, -1 ])
	hull = []
	done = False
	while not done:
		hull.append(current_point)
		
		def turn_cos_angle(point):
			if np.all(point == current_point):
				return -np.Infinity
			return cos_angle(current_dir, point - current_point)
		
		next_point = max(list(points), key = turn_cos_angle)
		
		current_dir = next_point - current_point
		current_point = next_point
		
		if np.all(current_point == start_point):
			done = True
	return np.array(hull)

def cos_angle(u, v):
	return np.dot(u, v) / sqrt( np.dot(u, u) * np.dot(v, v) )

def barycentre(points):
	"""barycentre(points : 2D np.array with 2 cols) -> (X : int, Y : int)
	Centroid of a list of 2D points, rounded to integer coordinates"""
	bary_x, bary_y = np.mean(points, axis = 0)
	return round(bary_x), round(bary_y)

def get_target_circle(points):
	"""get_target_circle(points : 2D np.array with 2 cols) -> (centre X : int, centre Y : int, radius : int)
	Circle to deform face edge onto"""
	centre_x, centre_y = barycentre(points)
	
	min_x = np.min(points[:,0])
	max_x = np.max(points[:,0])
	dx = max_x - min_x
	
	min_y = np.min(points[:,1])
	max_y = np.max(points[:,1])
	dy = max_y - min_y
	
	face_radius = (dx + dy) / 4
	return round(centre_x), round(centre_y), round(face_radius)
