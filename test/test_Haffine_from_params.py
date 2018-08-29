import sys
import os
import shutil
from nose.tools import *
from image_mosaic.Haffine_from_params import *

files_dir = os.path.join(os.path.dirname(__file__), 'files')
saved = None

def setup_tmp():
	pass
	# if os.path.exists('tmp'):
	# 	shutil.rmtree('tmp')
	# os.mkdir('tmp')

def setup():
#	setup_tmp()
	global saved
	saved = sys.argv

def teardown():
	sys.argv = saved

@with_setup(setup, teardown)
def test_main():
	# > %prog --scale 0.6 --center [100,50] --angle=-50.0''')
	sys.argv = ['Haffine_from_params', '--scale', '0.6', '--center', '[100,50]', '--angle', '50.0']
	main()

