import sys
import os
import shutil
from nose.tools import *
from image_mosaic.crop_image import *

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
def test_main():
	shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
	sys.argv = ['crop_image', 'tmp/cat.jpg', '-o', 'tmp/cat_cropped.jpg', '-g', '600x400+40+28']
	main()

