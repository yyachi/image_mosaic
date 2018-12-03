import sys
import os
import shutil
from nose.tools import *
from image_mosaic.affine_from_points import *

files_dir = os.path.join(os.path.dirname(__file__), 'files')
saved = None

def setup_tmp():
  pass

def setup():
  global saved
  saved = sys.argv

def teardown():
  sys.argv = saved

@with_setup(setup, teardown)
def test_main():
  sys.argv = ['affine_from_points', '-f', 'yaml']
  main()