import os
import shutil
from nose.tools import *
from nose.plugins.skip import SkipTest
from mock import patch
from mock import Mock
from image_mosaic.image_warp_click import *

files_dir = os.path.join(os.path.dirname(__file__), 'files')
saved = None

def setUpModule():
  raise SkipTest

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
  sys.argv = ['image_warp_click','tmp/cat.jpg']
  anchor_on_image = [(216, 216), (315, 198), (287, 280)]
  anchor_on_stage = [(-50,50),(50,50),(50,-50)]
  gui = Gui('tmp/cat.jpg', [500,500])
  mock_get_anchor_on_image = Mock()
  mock_get_anchor_on_image.return_value = anchor_on_image
  gui.get_anchor_on_image = mock_get_anchor_on_image

  mock_get_anchor_on_stage = Mock()
  mock_get_anchor_on_stage.return_value = anchor_on_stage
  gui.get_anchor_on_stage = mock_get_anchor_on_stage

  with patch('image_mosaic.image_warp_click.get_gui') as mock:
    mock.return_value = gui
    with patch('image_mosaic.image_warp_click.show_image')  as mock2:
      mock2.return_value = None
      main()