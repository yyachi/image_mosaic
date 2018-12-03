import sys
import os
import shutil
from nose.tools import *
from image_mosaic.make_tiles import *

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
	#shutil.copy(os.path.join(files_dir, 'billboard_for_rent.jpg'),'tmp')
	sys.argv = ['make_tiles', 'tmp/cat.jpg', '[-9344.0,5493.0,8756.0,-7379.0]', '18100', '[-294.0,-943.0]', '-z', '3', '-o', 'tmp/maps/cat', '-t']
	main()

