import sys
import os
import shutil
import numpy as np
from nose.tools import *
from image_mosaic.util import *

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
def test_str2array():
  str = "[[1,1],[2,2]]"
  str2array(str)

def test_array2str():
  a = [[1,1],[2,2]]
  array2str(a)

def test_array2cvmat2D():
  a = np.array([[1,1],[2,2],[3,3]])
  m = array2cvmat2D(a)

def test_getRotationOffsetMatrix2D():
  offset = (10, 10)
  angle = 80
  scale = 0.9
  m = getRotationOffsetMatrix2D(offset, angle, scale)
