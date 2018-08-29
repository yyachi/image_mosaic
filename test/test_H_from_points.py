import sys
import os
import shutil
from nose.tools import *
from image_mosaic.H_from_points import *

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
	sys.argv = ['H_from_points', '[[100,50],[100,0],[0,0],[0,50]]','[[-50,100],[0,100],[0,0],[-50,0]]']
	main()

