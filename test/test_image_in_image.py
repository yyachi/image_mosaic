import sys
import os
import shutil
from nose.tools import *
from opencvtool.image_in_image import *

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
	# Hint
	# > %prog data/cat.jpg data/billboad_for_rent.jpg [[40,264],[605,264],[605,540],[36,538]]
	# > %prog data/cat.jpg data/billboad_for_rent.jpg [[55,675],[277,677],[281,826],[52,826]]''')	
	shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
	shutil.copy(os.path.join(files_dir, 'billboard_for_rent.jpg'),'tmp')
	sys.argv = ['image_in_image', 'tmp/cat.jpg', 'tmp/billboard_for_rent.jpg', '[[55,675],[277,677],[281,826],[52,826]]', '-o', 'tmp/cat_on_billboard_for_rent.jpg']
	main()

