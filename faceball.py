"""faceball

Turn a person's face into a ball representing their ideology."""

import argparse
from os import path
from sys import argv
from faceball.faceball import faceball

parser = argparse.ArgumentParser(description = "Turn a person's face into a ball representing their ideology.")
parser.add_argument('in_path', help = 'path to input image')
parser.add_argument('out_path', nargs = '?', help = 'path to output image (defaut: ball_[in_path])')
parser.add_argument('--debug', action = 'store_true', help = 'add debug marks on image')
parser.add_argument('-b', '--background', help = '''background colour.
	Supports "black", "white", "discord" (Discord dark theme), comma-separated RGB (e.g. "255,255,255"), hex (e.g. "ff00ff").
	Default is transparent for png, "discord" otherwise.'''
)

def main(in_path, out_path, background = None, debug = False):
	if not out_path:
		out_path = get_default_out_path(in_path)
	faceball(in_path, out_path, background, debug)

def get_default_out_path(in_path):
	dir, fname = path.split(in_path)
	return path.join(dir, 'ball_' + fname)

if __name__ == '__main__':
	args = parser.parse_args(argv[1:])
	main(**vars(args))
