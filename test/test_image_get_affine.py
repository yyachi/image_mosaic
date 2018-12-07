import sys
import os
import shutil
from nose.tools import *
from image_mosaic.image_get_affine import *


files_dir = os.path.join(os.path.dirname(__file__), 'files')
saved = None

class MyOptions():
  def __init__(self):
    self.answer_yes = False

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

# @with_setup(setup, teardown)
def test_is_answer_yes():
  options = MyOptions()
  options.answer_yes = True
  answer_yes = True
  is_answer_yes("Are you sure? (YES/no) ", True, options.answer_yes)

@with_setup(setup, teardown)
@raises(RuntimeError)
def test_main_without_geo():
  shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
  sys.argv = ['calc_affine','tmp/cat.jpg', '-y', '-v']
  main()

@with_setup(setup, teardown)
@raises(SystemExit)
def test_help():
  # > %prog --scale 0.6 --center [100,50] --angle=-50.0 imagefile''')
  sys.argv = ['calc_affine','-h']
  main()

@with_setup(setup, teardown)
def test_main_with_geo():
  shutil.copy(os.path.join(files_dir, 'cat.jpg'),'tmp')
  shutil.copy(os.path.join(files_dir, 'cat.geo'),'tmp')
  sys.argv = ['calc_affine','tmp/cat.jpg', '-y', '-v']
  main()