"""Generate all example faceballs"""

from os import listdir, mkdir, path
from faceball.faceball import faceball

EXAMPLES_DIR = 'examples'
EXAMPLES_INPUT_DIR = 'original'
EXAMPLES_OUTPUT_DIR = 'ball'

def gen_examples():
	input_dir = path.join(EXAMPLES_DIR, EXAMPLES_INPUT_DIR)
	output_dir = path.join(EXAMPLES_DIR, EXAMPLES_OUTPUT_DIR)
	if not path.isdir(output_dir):
			mkdir(output_dir)
	
	for fname in listdir(input_dir):
		input_fpath = path.join(input_dir, fname)
		output_fpath = path.join(output_dir, fname)
		faceball(input_fpath, output_fpath, background = 'white')

if __name__ == '__main__':
	gen_examples()
