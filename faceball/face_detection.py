"""Detect faces and face landmarks in an image"""

import cv2
import importlib.resources
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
facemarks_model = 'lbfmodel.yaml'

_FACEMARK = None # poor man's memoisation

def get_facemark():
	"""get_facemark() -> face landmark detector"""
	global _FACEMARK
	if not _FACEMARK:
		facemark = cv2.face.createFacemarkLBF()
		with importlib.resources.path('faceball.resources', facemarks_model) as model_path:
			facemark.loadModel(str(model_path))
		_FACEMARK = facemark
	return _FACEMARK

def get_face(bgr, logger):
	"""get_facemark(bgr, logger) -> (face, landmarks)
	Find face in image and its landmarks
	Throws if no face is found. Chooses the largest face if multiple are found.
	bgr: OpenCV BGR-space image
	logger: HTML image logger
	face: (x : int, y : int, width : int, height : int) rectangle containing detected face
	landmarks: 2D np.array of face landmark points"""
	greyscale = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
	
	faces = face_cascade.detectMultiScale(greyscale)
	
	if len(faces) == 0:
		raise ValueError('No faces found')
	
	log_faces(bgr, faces, logger)
	# Use largest-area face if multiple are found
	face = max(faces, key = lambda face: face[2] * face[3])
	
	ok, landmarks = get_facemark().fit(bgr, faces = np.array([face]))
	
	return face, landmarks[0][0]

def log_faces(bgr, faces, logger):
	log_image = bgr.copy()
	for x, y, w, h in faces:
		cv2.rectangle(log_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
	
	# TODO: onerous facemark detection, could remove
	ok, landmarks = get_facemark().fit(bgr, faces = faces)
	for marks in landmarks:
		cv2.face.drawFacemarks(log_image, marks, (255, 255, 255))
	
	logger.log(
		'Face detection', 'Detected faces', log_image,
		[ 'Found {0} faces'.format(len(faces)) ]
	)
