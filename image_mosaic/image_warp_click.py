#!/usr/bin/env python
import os
import sys
import cv2
import yaml
from image_mosaic.stage import *
from image_mosaic.gui import *
from optparse import OptionParser

def get_gui(image_path):
  return Gui(image_path,[500,500])

def show_image(name, image):
  print("activate %s window and type escape to terminate." % (name))
  while True:
    cv2.imshow(name, image)
    if cv2.waitKey(15) == 27:
      break

def main():
  argvs = sys.argv
  argc = len(argvs)
  if (argc != 2):
      print('Usage: # python %s filename' % argvs[0])
      quit()

  parser = OptionParser("""usage: %prog [options] imagefile

SYNOPSIS AND USAGE
  python %prog [options] imagefile.jpg

DESCRIPTION
  Transform imagefile by matching three coordinates.  This will
  creates rotated and distorted image, and image-info files with
  Affine matrix for original and newly created images.  This requires
  image libraries and very likey you have to inovke this from CMD
  prompt on MS Windows.  With graphical interface, %prog asks you to
  click three anchors on imagefile then type in their VS's
  coordinates.

  As a result, imagefile will be accompanied with three files.
  - imagefile.jpg
  - imagefile.geo     contains Affine matrix of imagefile.jpg
  - imagefile_.jpg    rotate and distorted one to be pasted to VS's wall
  - imagefile_.geo    contains Affine matrix of imagefile_.jpg

  This program offers similar functionality to image-warp. User can create
  imageometry file with clicking image and typing stage coordinates.
  This command cannot accept --range and --density options unlike image-warp.

EXAMPLE
  DOS> dir
  Suiton.jpg
  DOS> python %XTREEML%/python/%prog imagefile.jpg
  ...
  DOS> dir
  imagefile.jpg  imagefile.geo  imagefile_.jpg  imagefile_.geo

SEE ALSO
  image-warp
  blend-image
  https://github.com/misasa/image_mosaic
  https://github.com/misasa/image_mosaic/blob/master/image_mosaic/image_warp_click.py

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014-2020 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  May 27, 2015: TK adds documentation
""")
  (options, args) = parser.parse_args()

  image_path = argvs[1]
  root, ext = os.path.splitext(image_path)
  default_ofile_name = os.path.basename(root) + '_' + ext
  #default_ofile_name = os.path.basename(root) + '_VS' + ext
  default_yfile_name = os.path.basename(root) + '.geo'
  warped_yfile_name = os.path.basename(root) + '_.geo'

  target_dir = os.path.dirname(image_path)
  default_ofile_path = os.path.join(target_dir, default_ofile_name)
  default_yfile_path = os.path.join(target_dir, default_yfile_name)
  warped_yfile_path = os.path.join(target_dir, warped_yfile_name)

  gui = get_gui(image_path)
  original_height, original_width, original_channels = gui.original_image.shape
  original_aspect = float(original_width) / original_height
  
  if os.path.isfile(default_yfile_path):
    print("%s loading..." % default_yfile_path)
    yf = open(default_yfile_path).read().decode('utf8')
    config = yaml.load(yf)
    if 'affine_xy2vs' in config:
      affine_input = list_to_affine(config['affine_xy2vs'])
      print("Input affine matrix to stage is %s." % (affine_to_str(affine_input)))
      image_rect = [(0,0),(original_width,0),(original_width,original_height),(0,original_height)]
      image_rect_coord = [image_pixel_to_coord(p, original_width, original_height) for p in image_rect]
      image_rect_on_stage = transform_points(image_rect_coord, affine_input)
      affine_image2stage = get_affine_matrix(image_rect, image_rect_on_stage)
      print("%s %dx%d pix was calibrated based on %s. It's affine matrix to stage is %s." % (os.path.basename(image_path), original_width, original_height, os.path.basename(default_yfile_name), affine_to_str(affine_input)))
  else:
    anchors_on_image = gui.get_anchor_on_image()
    anchors_on_stage = gui.get_anchor_on_stage()

    gui.set_anchors(anchors_on_image)
    gui.draw_points(gui.temp)
  
    anchors_on_image_coord = [image_pixel_to_coord(p, original_width, original_height) for p in anchors_on_image]
    print("#\tx(pix)\ty(pix)\tx(um)\ty(um)")
    for idx in range(len(anchors_on_image)):
      print("%d\t%.3f\t%.3f\t%.3f\t%.3f" % (idx+1,anchors_on_image_coord[idx][0], anchors_on_image_coord[idx][1],anchors_on_stage[idx][0],anchors_on_stage[idx][1]))

    affine_image2stage = get_affine_matrix(anchors_on_image, anchors_on_stage)
    affine_for_output = get_affine_matrix(anchors_on_image_coord, anchors_on_stage)

    f = open(default_yfile_path, 'w')
    yaml.dump({'affine_xy2vs': affine_to_list(affine_for_output) }, f, encoding='utf8', allow_unicode=True)
    print("%s %dx%d pix was calibrated. It's affine matrix to stage was %s." % (os.path.basename(image_path), original_width, original_height, affine_to_str(affine_for_output)))

  win_view = Stage()
  win_view.set_image(image_path, affine_image2stage)

  cv2.imwrite(default_ofile_path, win_view.output_image)

  warped_rect_coord = [image_pixel_to_coord(p, win_view.output_size[0], win_view.output_size[1]) for p in win_view.output_rect]
  affine_warped = get_affine_matrix(warped_rect_coord[0:3], win_view.output_rect_on_stage[0:3])

  f = open(warped_yfile_path, 'w')
  yaml.dump({ 'affine_xy2vs': affine_to_list(affine_warped) }, f, encoding='utf8', allow_unicode=True)

  print("Calibrated image was saved as %s %dx%d pix. " % (default_ofile_path, win_view.output_image.shape[0], win_view.output_image.shape[1]))
  print("Please use the following parameters to place the calibrated image.")
  print("Locate:\t(%7.3f, %7.3f) um" % (win_view.output_rect_on_stage[0][0], win_view.output_rect_on_stage[0][1]))
  print("Center:\t(%7d, %7d) dot" % (0, 0))
  print("Size:\t(%7.3f, %7.3f) um" % (win_view.stage_width, win_view.stage_height))

  show_image(default_ofile_name, cv2.imread(default_ofile_path))
if __name__ == '__main__':
  main()
