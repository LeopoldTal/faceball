"""Mask image into a disk with two tinted halves"""

import cv2
import numpy as np

# parameters chosen "empirically"
lightness_exponent = 1.7
saturation_exponent = 1.9
saturation_shrink = 0.5 # dark half only

def tint_region(hls, face_mask, vertices, light):
	"""tint_region(hls, face_mask, vertices, light) -> None
	Makes a polygon lighter or darker
	hls: OpenCV HLS-space image
	face_mask: circular mask of the face
	vertices: np.array of points defining polygon to tint
	light: boolean"""
	im_width, im_height, _ = hls.shape
	
	mask = np.zeros((im_width, im_height), np.uint8)
	points = [vertices.reshape((-1, 1, 2))]
	mask = cv2.fillPoly(mask, points, color = 255)
	
	mask = np.bitwise_and(mask, face_mask)
	
	hls[mask == 255,1] = scale(hls[mask == 255,1], lightness_exponent, light)
	
	max_saturation = 1 if light else saturation_shrink
	hls[mask == 255,2] = max_saturation * scale(hls[mask == 255,2], saturation_exponent, light)

def scale(values, exponent, light):
	norm = values / 255
	if light:
		new_values = 1 - (1 - norm)**exponent
	else:
		new_values = norm**exponent
	return 255 * new_values

def mask_face(bgr, target_circle):
	"""mask_face(bgr, target_circle) -> BGRA image
	bgr: OpenCV BGR-space image
	target_circle: (centre X : int, centre Y : int, radius : int) outer circle of mask"""
	x, y, r = target_circle
	im_width, im_height, _ = bgr.shape
	
	face_mask = np.zeros((im_width, im_height), np.uint8)
	face_mask = cv2.circle(face_mask, (x, y), r, 255, cv2.FILLED)
	
	hls = cv2.cvtColor(bgr, cv2.COLOR_BGR2HLS)
	
	top_vertices = np.array([[x - r, y - r], [x - r, y + r], [x + r, y - r]], np.int32)
	tint_region(hls, face_mask, top_vertices, True)
	
	bottom_vertices = np.array([[x + r, y + r], [x - r, y + r], [x + r, y - r]], np.int32)
	tint_region(hls, face_mask, bottom_vertices, False)
	
	bgra = cv2.cvtColor(cv2.cvtColor(hls, cv2.COLOR_HLS2BGR), cv2.COLOR_BGR2BGRA)
	bgra[face_mask == 0] = 0
	
	# TODO: might leave more room for thumbs up
	bgra = bgra[y-r:y+r, x-r:x+r]
	
	return bgra
