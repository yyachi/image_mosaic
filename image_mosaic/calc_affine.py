#!/usr/bin/env python
from optparse import OptionParser
import os
import sys
import cv2
import numpy as np
import time
import math
import yaml
from opencv_util import *

def main():
  parser = OptionParser("""usage: image-get-affine [options] image

SYNOPSIS AND USAGE
  python image-get-affine [options] imagefile.jpg

DESCRIPTION
  Return affine_xy2vs (also affine_ij2vs and anchors_xy) estimated
  from anchors and anchors_ij in imageometry file that comes with
  imagefile.jpg. For example, when imageilfe.jpg is `raman.jpg',
  this will look for imageometry file `raman.geo'.  Very likly you
  have to invoke this program from CMD prompt on MS Windows.

  This command also reads anchors_ij via GUI and anchors via stdin.
  This command is subset of image-warp, without image manipulation.

EXAMPLE
  CMD> dir
  raman.jpg  raman.geo
  CMD> type raman.geo
  anchors:
  - [X1 X2 X3]
  - [Y1 Y2 Y3]
  - [1  1  1 ]
  anchors_ij:
  - [x1 x2 x3]
  - [y1 y2 y3]
  - [1  1  1 ]
  CMD> python C:/Users/ims/xtreeml/imgtools/bin/vs-calc-affine.py raman.jpg
  ... <affine_xy2vs> and <affine_ij2vs> inserted in |raman.geo|

SEE ALSO
  blend-image
  image-warp
  https://github.com/misasa/image_mosaic

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  May 24, 2015: TK adds documentation
""")
  parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="make lots of noise")
  parser.add_option("-y", "--yes",
                  action="store_true", dest="answer_yes", default=False,
                  help="answer yes for all questions")

  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.error("incorrect number of arguments")

  image_path = args[0]

  original_image = cv2.imread(image_path)
  original_height = original_image.shape[0]
  original_width = original_image.shape[1]
  original_aspect = float(original_width) / original_height

  root, ext = os.path.splitext(image_path)
  default_ofile_name = os.path.basename(root) + '_' + ext #  _VS
  default_yfile_name = os.path.basename(root) + '.geo'    # .yaml
  warped_yfile_name = os.path.basename(root) + '_.geo'    # _warped.yaml

  target_dir = os.path.dirname(image_path)
  default_ofile_path = os.path.join(target_dir, default_ofile_name)
  default_yfile_path = os.path.join(target_dir, default_yfile_name)
  warped_yfile_path = os.path.join(target_dir, warped_yfile_name)

  config = None

  if os.path.isfile(default_yfile_path):
    print "%s loading..." % default_yfile_path
    yf = open(default_yfile_path).read().decode('utf8')
    config = yaml.load(yf)
    if 'affine_ij2vs' in config:
      print config['affine_ij2vs']
      affine_input = list_to_affine(config['affine_ij2vs'])
      print affine_input
      print "Input affine matrix to stage is %s." % (affine_to_str(affine_input))
      image_rect = [(0,0),(original_width,0),(original_width,original_height),(0,original_height)]
      image_rect_coord = [image_pixel_to_coord(p, original_width, original_height) for p in image_rect]
      image_rect_on_stage = transform_points(image_rect_coord, affine_input)
      affine_image2stage = get_affine_matrix(image_rect, image_rect_on_stage)
      print "%s %dx%d pix was calibrated based on %s. It's affine matrix to stage is %s." % (os.path.basename(image_path), original_width, original_height, os.path.basename(default_yfile_name), affine_to_str(affine_input))
  else:
    raise RuntimeError("%s not found" % default_yfile_path)

  if config != None and ('anchors_ij' in config) and is_answer_yes("Anchors for image <anchors_ij> found.  Do you use them? (YES/no) ", True, options.answer_yes):
    anchors_on_image = list_to_points(config['anchors_ij'])
  else:
    anchors_on_image = get_anchor_on_image()

  if config != None and ('anchors' in config) and is_answer_yes("Anchors for stage <anchors> found.  Do you use them? (YES/no) ", True, options.answer_yes):
    anchors_on_stage = list_to_points(config['anchors'])
  else:
    if options.flag_window:
      anchors_on_stage = get_anchor_on_stage_from_window(win)
    else:
      anchors_on_stage = get_anchor_on_stage()

  anchors_on_image_coord = [image_pixel_to_coord(p, original_width, original_height) for p in anchors_on_image]

  print "#\tx(pix)\ty(pix)\tx(um)\ty(um)"
  for idx in range(len(anchors_on_image)):
    print "%d\t%.3f\t%.3f\t%.3f\t%.3f" % (idx+1,anchors_on_image_coord[idx][0], anchors_on_image_coord[idx][1],anchors_on_stage[idx][0],anchors_on_stage[idx][1])

  affine_image2stage = get_affine_matrix(anchors_on_image, anchors_on_stage)
  affine_for_output = get_affine_matrix(anchors_on_image_coord, anchors_on_stage)

  f = open(default_yfile_path, 'w')
  yaml.dump({ 'anchors': points_to_list(anchors_on_stage), 'anchors_xy': points_to_list(anchors_on_image_coord), 'anchors_ij': points_to_list(anchors_on_image), 'affine_xy2vs': affine_for_output.tolist(), 'affine_ij2vs': affine_image2stage.tolist() }, f, encoding='utf8', allow_unicode=True)
  print "%s %dx%d pix was calibrated. Its affine matrix to stage was %s." % (os.path.basename(image_path), original_width, original_height, affine_to_str(affine_for_output))

if __name__ == "__main__":
  main()
