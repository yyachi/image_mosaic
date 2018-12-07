import sys
import os
import shutil
from nose.tools import *
from image_mosaic.image_warp import *

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
@raises(RuntimeError)
def test_main_without_affine_xy2vs():
  shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
  shutil.copy(os.path.join(files_dir, 'cat.geo'),'tmp')  
  sys.argv = ['image_warp','tmp/cat.jpg']
  main()

@with_setup(setup, teardown)
@raises(RuntimeError)
def test_main_without_geo():
  shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
  sys.argv = ['image_warp','tmp/cat.jpg']
  main()

@with_setup(setup, teardown)
def test_main_with_affine_xy2vs():
  shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
  shutil.copy(os.path.join(files_dir, 'cat.geo_with_affine'),'tmp/cat.geo')  
  sys.argv = ['image_warp','tmp/cat.jpg']
  #sys.argv = ['image_warp','tmp/cat.jpg', '-s','-r', '-50', '50', '-38.45', '38.45', '-d', '10.24']
  main()

@with_setup(setup, teardown)
def test_with_window():
  shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
  shutil.copy(os.path.join(files_dir, 'cat.geo_with_affine'),'tmp/cat.geo')  
  sys.argv = ['image_warp','tmp/cat.jpg']
  #sys.argv = ['image_warp','tmp/cat.jpg', '-s','-r', '-50', '50', '-38.45', '38.45', '-d', '10.24']
  main()  