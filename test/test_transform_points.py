import sys
import os
import shutil
from nose.tools import *
from image_mosaic.transform_points import *

files_dir = os.path.join(os.path.dirname(__file__), 'files')
saved = None

def setup_tmp():
	if os.path.exists('tmp'):
		shutil.rmtree('tmp')
	os.mkdir('tmp')

def setup():
	setup_tmp()
	global saved
	saved = sys.argv

def teardown():
	sys.argv = saved

@with_setup(setup, teardown)
def test_with_params():
	# > %prog --scale 0.6 --center [100,50] --angle=-50.0 [[0,0],[100,100]]
	shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
	sys.argv = ['transform_points', '--scale', '0.6', '--center', '[100,50]' ,'--angle', '-50.0','[[0,0],[100,100]]']
	main()

def test_with_matrix():
	# > %prog --matrix=[[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]] [[0,0],[100,100]]''')
	shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
	sys.argv = ['transform_points', '--matrix', '[[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]', '[[0,0],[100,100]]']
	main()
