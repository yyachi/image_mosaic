import sys
import os
import shutil
from nose.tools import *
from image_mosaic.warp_image import *

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
  # > %prog --scale 0.6 --center [100,50] --angle=-50.0 imagefile''')
  shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
  sys.argv = ['warp_image', '--scale', '0.6', '--center', '[100,50]' ,'--angle', '-50.0','tmp/cat.jpg', '-o', 'tmp/cat_warped.jpg']
  main()

# @with_setup(setup, teardown)
# def test_main():
#   # > %prog --scale 0.6 --center [100,50] --angle=-50.0 imagefile''')
#   shutil.copy(os.path.join(files_dir, '_305-30Si_accu-1.png'),'tmp')
#   #warp_image _305-30Si_accu-1.png -g [1280,1024] -m [[6.528e+0,-2.137e-1,2.619e+2],[3.284e-1,6.726e+0,-8.650e+1],[0.000e+0,0.000e+0,1.000e+0]] -o output_1.png 
#   sys.argv = ['warp_image','tmp/_305-30Si_accu-1.png', '-g' ,'[1280,1024]', '-m' ,'[[6.528e+0,-2.137e-1,2.619e+2],[3.284e-1,6.726e+0,-8.650e+1],[0.000e+0,0.000e+0,1.000e+0]]', '-o', 'tmp/output_1.png']
#   main()
