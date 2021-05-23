"""HTML logger"""

import cv2
import importlib.resources
import re
from datetime import datetime
from html import escape
from os import mkdir, path

LOG_FOLDER = importlib.resources.files('faceball').parent.joinpath('log')

class Logger:
	"""Logger(name) -> HTML and images logger"""
	def __init__(self, name):
		if not path.isdir(LOG_FOLDER):
			mkdir(LOG_FOLDER)
		
		now = datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
		self.log_name = name + now
	
	def __enter__(self):
		fpath = path.join(LOG_FOLDER, self.log_name + '.html')
		print('Logging to', fpath)
		self.log_file = open(fpath, 'w+')
		self.log_file.write(to_html('h1', 'faceball log ' + self.log_name))
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.log_file.close()
	
	def log(self, title, image_desc, image, messages = []):
		"""logger.log(title : string, image_desc : string, image : OpenCV image, messages : string[] = [])
		Logs a new section with title, image, and optional text paragraphs"""
		self.log_file.write(to_html('h2', title))
		self.log_file.writelines([ to_html('p', message) for message in messages ])
		
		image_name = self.log_name + '_' + sanitise(image_desc) + '.png'
		image_path = path.join(LOG_FOLDER, image_name)
		cv2.imwrite(image_path, image)
		self.log_file.write(
			'<p><img alt="{0}" src="{1}" /></p>\n'.format(image_desc, image_name)
		)

def to_html(tag_name, text):
	return '<{0}>{1}</{0}>\n'.format(tag_name, escape(text))

def sanitise(s):
	s = s.lower().replace(' ', '_')
	return re.sub('[^a-z0-9_]', '', s)
