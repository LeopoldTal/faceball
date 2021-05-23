"""Save image with optional background fill"""

import cv2
import numpy as np

NAMED_COLOURS = {
	'discord': (41, 43, 48),
	'white': (255, 255, 255),
	'black': (0, 0, 0)
}

def get_rgb(colour_name):
	"""get_rgb(colour_name : string) -> (int, int, int)
	Get RGB colour. Supports named colour, decimal RGB, hex."""
	if not colour_name:
		return NAMED_COLOURS['discord']
	
	colour_name = colour_name.lower()
	
	if colour_name in NAMED_COLOURS:
		return NAMED_COLOURS[colour_name]
	
	if ',' in colour_name:
		return tuple(map(int, colour_name.split(',')))
	
	r, g, b = colour_name[:2], colour_name[2:4], colour_name[4:]
	return tuple(int(c, 16) for c in (r, g, b))

def set_background(rgba, background_rgb):
	"""set_background(rgba, background_rgb) -> rgb
	Fills all transparent pixes with background_rgb and drops alpha channel
	rgba: OpenCV RGBA image
	background_rgb: (int, int, int) RGB triplet
	rgb: OpenCV RGB image"""
	alpha = rgba[:,:,3] / 255
	
	for colour in range(0, 3):
		rgba[:, :, colour] = (
			alpha * rgba[:, :, colour]
			+ (1 - alpha) * background_rgb[colour]
		)
	
	return cv2.cvtColor(rgba, cv2.COLOR_RGBA2RGB)

def save_image(rgba, to_path, background):
	"""save_image(rgba, to_path, background) -> saved image
	Save image to file
	Replaces transparent pixels with background colour if background is not None or transparency is unsupported
	rgba: OpenCV RGBA image
	to_path: path to save to
	background: string defining background fill, or None"""
	if background is None and to_path.lower().endswith('.png'):
		cv2.imwrite(to_path, rgba)
		return rgba
	
	background_rgb = get_rgb(background)
	rgb = set_background(rgba, background_rgb)
	cv2.imwrite(to_path, rgb)
	return rgb
