"""Overlay a thumbs-up on an image"""

import cv2
import importlib.resources
import numpy as np

# TODO: would sunglasses and other hand be gilding the lily?

def add_thumbs_up(bgra):
	"""add_thumbs_up(bgra: OpenCV BGRA image) -> image
	Overlay a thumbs-up at the bottom right of the image"""
	with importlib.resources.path('faceball.resources', 'thumbs_up.png') as thumb_path:
		thumbs_up = cv2.imread(str(thumb_path), cv2.IMREAD_UNCHANGED)
	
	im_width, im_height, _ = bgra.shape
	orig_thumb_width, orig_thumb_height, _ = thumbs_up.shape
	thumb_height = round(im_height / 4)
	thumb_width = round(thumb_height / orig_thumb_height * orig_thumb_width)
	
	thumbs_up = cv2.resize(thumbs_up, (thumb_height, thumb_width))
	
	alpha_thumb = thumbs_up[:,:,3] / 255
	alpha_face = 1 - alpha_thumb
	
	y1, y2, x1, x2 = im_width-thumb_width, im_width, im_height-thumb_height, im_height
	for colour in range(0, 3):
		bgra[y1:y2, x1:x2, colour] = (
			alpha_face * bgra[y1:y2, x1:x2, colour]
			+ alpha_thumb * thumbs_up[:,:,colour]
		)
	bgra[y1:y2, x1:x2, 3] = np.bitwise_or(bgra[y1:y2, x1:x2, 3], thumbs_up[:,:,3])
	
	return bgra
