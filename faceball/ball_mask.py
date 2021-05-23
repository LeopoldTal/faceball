"""Mask image into a disk with two tinted halves"""

import cv2
import numpy as np

# parameters chosen "empirically"
lightness_exponent = 1.7
saturation_coeff = .25

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
	
	lightness = hls[mask == 255,1] / 255
	if light:
		new_lightness = 1 - (1 - lightness)**lightness_exponent
	else:
		new_lightness = lightness**lightness_exponent
	hls[mask == 255,1] = 255 * new_lightness
	
	target_saturation = 255 * saturation_coeff if light else 0
	hls[mask == 255,2] = (1 - saturation_coeff) * hls[mask == 255,2] + target_saturation

def mask_face(rgb, target_circle):
	"""mask_face(rgb, target_circle) -> RGBA image
	rgb: OpenCV RGB-space image
	target_circle: (centre X : int, centre Y : int, radius : int) outer circle of mask"""
	x, y, r = target_circle
	im_width, im_height, _ = rgb.shape
	
	face_mask = np.zeros((im_width, im_height), np.uint8)
	face_mask = cv2.circle(face_mask, (x, y), r, 255, cv2.FILLED)
	
	hls = cv2.cvtColor(rgb, cv2.COLOR_BGR2HLS)
	
	top_vertices = np.array([[x - r, y - r], [x - r, y + r], [x + r, y - r]], np.int32)
	tint_region(hls, face_mask, top_vertices, True)
	
	bottom_vertices = np.array([[x + r, y + r], [x - r, y + r], [x + r, y - r]], np.int32)
	tint_region(hls, face_mask, bottom_vertices, False)
	
	rgba = cv2.cvtColor(cv2.cvtColor(hls, cv2.COLOR_HLS2BGR), cv2.COLOR_RGB2RGBA)
	rgba[face_mask == 0] = 0
	
	# TODO: might leave more room for thumbs up
	rgba = rgba[y-r:y+r, x-r:x+r]
	
	return rgba
