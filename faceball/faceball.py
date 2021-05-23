"""Turn a person's face into a ball"""

import cv2
import numpy as np
from os import path
from faceball.ball_mask import mask_face
from faceball.face_detection import get_face
from faceball.hull import convex_hull, get_target_circle
from faceball.image_saver import save_image
from faceball.log import Logger
from faceball.overlay import add_thumbs_up
from faceball.warp import warp_poly_to_circle

def faceball(input_image_path, output_image_path, background = None, debug = False):
	"""faceball(input_image_path, output_image_path, background = None, debug = False)
	Transform an image into a faceball
	input_image_path, output_image_path: string
	background: string representing a colour, or None
	debug: boolean"""
	_, image_name = path.split(input_image_path)
	with Logger(image_name) as logger:
		rgb = cv2.imread(input_image_path)
		logger.log(
			'Load original', 'Original', rgb,
			[ 'Read from: ' + input_image_path ]
		)
		
		face, landmarks = get_face(rgb, logger)
		hull = convex_hull(landmarks)
		target_circle = get_target_circle(hull)
		log_face_hull(rgb, landmarks, hull, target_circle, logger)
		
		if debug:
			mark_image(rgb, landmarks, hull, target_circle)
		warped = warp_poly_to_circle(rgb, hull, target_circle)
		if debug:
			mark_target_circle(warped, target_circle)
		logger.log('Warp to circle', 'Warped', warped)
		
		masked = mask_face(warped, target_circle)
		logger.log('Tint & mask', 'Faceball', masked)
		
		add_thumbs_up(masked)
		logger.log('Add thumbs up', 'Final', masked)
		
		saved = save_image(masked, output_image_path, background)
		logger.log(
			'Save', 'Saved', saved,
			[ 'background: {0}'.format(background), output_image_path ]
		)

def log_face_hull(rgb, landmarks, hull, target_circle, logger):
	log_image = rgb.copy()
	mark_image(log_image, landmarks, hull, target_circle)
	logger.log('Find convex hull of face landmarks', 'Landmarks and hull', log_image)

def mark_image(image, landmarks, hull, target_circle):
	mark_target_circle(image, target_circle)
	cv2.face.drawFacemarks(image, np.array([landmarks]), (255, 255, 255))
	cv2.face.drawFacemarks(image, np.array([hull]), (0, 0, 255))

def mark_target_circle(image, target_circle):
	centre_x, centre_y, radius = target_circle
	cv2.circle(image, (centre_x, centre_y), radius, (0, 255, 0), 2)
