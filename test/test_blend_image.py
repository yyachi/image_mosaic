import sys
import os
import shutil
from nose.tools import *
from image_mosaic.blend_image import *

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
  shutil.copy(os.path.join(files_dir, 'billboard_for_rent.jpg'),'tmp')  
  sys.argv = ['blend_image', 'tmp/billboard_for_rent.jpg', 'tmp/cat.jpg', '10', '200', '600', '400', '0.5', '0.3', '-o', 'tmp/blend.jpg']
  main()

# @with_setup(setup, teardown)
# def test_main():
#   shutil.copy(os.path.join(files_dir, '_305.jpg'),'tmp')
#   shutil.copy(os.path.join(files_dir, 'output_1.png'),'tmp')  
#   sys.argv = ['blend_image', 'tmp/_305.jpg', 'tmp/output_1.png', '0', '0', '1280', '1024', '0.5', '0.5', '-o', 'tmp/output_2.png']
#   main()
