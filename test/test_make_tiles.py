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
	#shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
	#sys.argv = ['make_tiles', 'tmp/cat.jpg', '[-9344.0,5493.0,8756.0,-7379.0]', '18100', '[-294.0,-943.0]', '-a', '3', '-o', 'tmp/maps/cat', '-t']
	#shutil.copy(os.path.join(files_dir, 'cbk1i_mosaic_warped.png'),'tmp')
	#sys.argv = ['make_tiles', 'tmp/cbk1i_mosaic_warped.png', '[-8051.71,6154.39,7031.91,-4714.39]', '15119.55', '[-509.90,720.00]', '-z', '6', '-o', 'tmp/maps/47761', '-t']
	#main()
	shutil.copy(os.path.join(files_dir, 'cbk1i_7256_7274_warped.png'),'tmp')
	sys.argv = ['make_tiles', 'tmp/cbk1i_7256_7274_warped.png', '[1688.26,1660.90,3961.74,-177.30]', '15119.55', '[-509.90,720.00]', '-z', '6', '-o', 'tmp/maps/47762', '-t', '-d']
	main()


def test_tile_ij_at():
  center = [21.28, -110.0]
  length = 7794.012 
  assert tile_ij_at(1, -3808.473, 3787.007, length, center) == (0,0)
  assert tile_ij_at(1, -3808.471, 3787.005, length, center) == (0,0)
  assert tile_ij_at(1, 3851.031, -4007.005, length, center) == (1,1)
  assert tile_ij_at(1, 3851.033, -4007.007, length, center) == (1,1)
  assert tile_ij_at(1, 1440, 2423, length, center) == (1,0)
  assert tile_ij_at(2, 1440, 2423, length, center) == (2,0)
  assert tile_ij_at(3, 1440, 2423, length, center) == (5,1)
  assert tile_ij_at(4, 1440, 2423, length, center) == (10,2)
  assert tile_ij_at(5, 1440, 2423, length, center) == (21,5)
  assert tile_ij_at(6, 1440, 2423, length, center) == (43,11)

